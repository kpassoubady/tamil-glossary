#!/usr/bin/env python3
"""
Fix duplicate terms and attribution in glossary.db:

1. Fix normalizer: strip trailing parenthetical abbreviations
   e.g. "Artificial Intelligence (AI)" → "artificial intelligence"
   This merges duplicate terms that differ only by abbreviation.

2. Auto-remove காங்கேயன் பசுபதி (ai-tamil-glossary) as source for terms
   that also exist in sollaaayvu — those should credit சொல்லாய்வு குழு.

3. Re-export consolidated-glossary.md and .csv

Usage:
    python3 scripts/fix-duplicates-and-attribution.py            # dry-run (report only)
    python3 scripts/fix-duplicates-and-attribution.py --apply    # apply changes + re-export
"""

import os
import re
import sqlite3
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "glossary.db")

AI_SOURCE = "ai-tamil-glossary"
SOL_SOURCE = "sollaaayvu"


def normalize_english(text):
    """Improved normalizer — strips trailing parenthetical abbreviations."""
    text = text.strip()
    text = text.rstrip(".:")
    # Strip trailing parenthetical abbreviation: (AI), (AGI), (ANN), (NLP), etc.
    text = re.sub(r"\s*\([A-Za-z0-9/\.\-\s]+\)\s*$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


def find_duplicate_terms(conn):
    """Find terms whose english_normalized would merge under the new normalizer."""
    rows = conn.execute(
        "SELECT id, english, english_normalized FROM terms ORDER BY english_normalized"
    ).fetchall()

    # Group by new normalized form
    groups = {}
    for term_id, english, old_norm in rows:
        new_norm = normalize_english(english)
        if new_norm not in groups:
            groups[new_norm] = []
        groups[new_norm].append((term_id, english, old_norm))

    # Find groups where multiple term IDs map to same new_norm
    duplicates = {k: v for k, v in groups.items() if len(v) > 1}
    return duplicates


def find_attribution_issues(conn):
    """
    Find terms where ai-tamil-glossary translations should be removed
    because the same term (by normalized key) also has a sollaaayvu translation.
    """
    ai_src_id = conn.execute(
        "SELECT id FROM sources WHERE short_name=?", (AI_SOURCE,)
    ).fetchone()[0]
    sol_src_id = conn.execute(
        "SELECT id FROM sources WHERE short_name=?", (SOL_SOURCE,)
    ).fetchone()[0]

    # Terms that have translations from BOTH ai-tamil-glossary and sollaaayvu
    overlap_terms = conn.execute("""
        SELECT DISTINCT t.id, t.english, t.english_normalized
        FROM terms t
        JOIN translations tr_ai ON t.id = tr_ai.term_id AND tr_ai.source_id = ?
        JOIN translations tr_sol ON t.id = tr_sol.term_id AND tr_sol.source_id = ?
        ORDER BY t.english_normalized
    """, (ai_src_id, sol_src_id)).fetchall()

    return overlap_terms, ai_src_id, sol_src_id


def merge_duplicate_terms(conn, duplicates, dry_run=True):
    """Merge duplicate terms: keep the one without parenthetical, move translations."""
    merged_count = 0
    for new_norm, group in sorted(duplicates.items()):
        # Prefer the shorter english form (without parenthetical) as canonical
        group.sort(key=lambda x: len(x[1]))
        keep_id, keep_eng, _ = group[0]
        to_merge = group[1:]

        print(f"\n  Merge → '{keep_eng}' (id={keep_id})")
        for merge_id, merge_eng, _ in to_merge:
            print(f"    ← '{merge_eng}' (id={merge_id})")

            if not dry_run:
                # Move translations from merge_id to keep_id
                # First check for conflicts (same tamil_term + source_id)
                existing = set(conn.execute(
                    "SELECT tamil_term, source_id FROM translations WHERE term_id=?",
                    (keep_id,)
                ).fetchall())

                to_move = conn.execute(
                    "SELECT id, tamil_term, source_id, is_primary, definition FROM translations WHERE term_id=?",
                    (merge_id,)
                ).fetchall()

                for tr_id, tamil, src_id, is_primary, defn in to_move:
                    if (tamil, src_id) in existing:
                        # Duplicate — just delete
                        conn.execute("DELETE FROM translations WHERE id=?", (tr_id,))
                    else:
                        # Move to keep_id
                        conn.execute(
                            "UPDATE translations SET term_id=? WHERE id=?",
                            (keep_id, tr_id)
                        )

                # Update the kept term's normalized form
                conn.execute(
                    "UPDATE terms SET english_normalized=? WHERE id=?",
                    (new_norm, keep_id)
                )
                # Delete the merged term
                conn.execute("DELETE FROM terms WHERE id=?", (merge_id,))

            merged_count += 1

    return merged_count


def remove_ai_attribution_for_overlap(conn, overlap_terms, ai_src_id, sol_src_id, dry_run=True):
    """
    For terms in both ai-tamil-glossary and sollaaayvu:
    remove the ai-tamil-glossary translation rows (சொல்லாய்வு குழு gets credit).
    """
    removed = 0
    for term_id, english, en_norm in overlap_terms:
        # Get the ai-tamil-glossary translations for this term
        ai_translations = conn.execute(
            "SELECT id, tamil_term FROM translations WHERE term_id=? AND source_id=?",
            (term_id, ai_src_id)
        ).fetchall()

        # Get the sollaaayvu translations for comparison
        sol_translations = conn.execute(
            "SELECT tamil_term FROM translations WHERE term_id=? AND source_id=?",
            (term_id, sol_src_id)
        ).fetchall()
        sol_tamil = set(r[0] for r in sol_translations)

        for tr_id, tamil in ai_translations:
            print(f"  Remove ai-tamil-glossary: '{english}' → '{tamil}'  (sollaaayvu has: {sol_tamil})")
            if not dry_run:
                conn.execute("DELETE FROM translations WHERE id=?", (tr_id,))
            removed += 1

    return removed


def main():
    dry_run = "--apply" not in sys.argv

    if not os.path.exists(DB_PATH):
        print(f"ERROR: {DB_PATH} not found.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)

    if dry_run:
        print("=" * 60)
        print("DRY RUN — no changes will be made. Use --apply to commit.")
        print("=" * 60)

    # -----------------------------------------------------------
    # Step 1: Fix k-murthy typo (idempotent)
    # -----------------------------------------------------------
    print("\n=== Step 1: Fix k-murthy author typo ===")
    if not dry_run:
        conn.execute("UPDATE sources SET author='அ.கி. மூர்த்தி' WHERE short_name='k-murthy'")
        conn.commit()
    cur = conn.execute("SELECT author FROM sources WHERE short_name='k-murthy'").fetchone()
    print(f"  k-murthy author: {cur[0]!r}" + (" → will fix to 'அ.கி. மூர்த்தி'" if dry_run and cur[0] != "அ.கி. மூர்த்தி" else ""))

    # -----------------------------------------------------------
    # Step 2: Find and merge duplicate terms
    # -----------------------------------------------------------
    print("\n=== Step 2: Find duplicate terms (parenthetical variants) ===")
    duplicates = find_duplicate_terms(conn)
    print(f"  Found {len(duplicates)} groups of duplicates to merge:")
    merged = merge_duplicate_terms(conn, duplicates, dry_run)
    print(f"\n  Total merges: {merged}")

    # -----------------------------------------------------------
    # Step 3: Remove ai-tamil-glossary attribution for sollaaayvu overlap
    # -----------------------------------------------------------
    print("\n=== Step 3: Remove ai-tamil-glossary attribution for sollaaayvu overlap ===")
    overlap_terms, ai_src_id, sol_src_id = find_attribution_issues(conn)
    print(f"  Terms in both ai-tamil-glossary and sollaaayvu: {len(overlap_terms)}")
    removed = remove_ai_attribution_for_overlap(conn, overlap_terms, ai_src_id, sol_src_id, dry_run)
    print(f"\n  Translations to remove: {removed}")

    # -----------------------------------------------------------
    # Step 4: Re-set primaries and re-export
    # -----------------------------------------------------------
    if not dry_run:
        conn.commit()

        print("\n=== Step 4: Re-setting primary terms ===")
        # Re-run primary selection
        conn.execute("UPDATE translations SET is_primary = 0")
        conn.execute("""
            UPDATE translations SET is_primary = 1
            WHERE id IN (
                SELECT t.id FROM translations t
                JOIN sources s ON t.source_id = s.id
                WHERE t.id = (
                    SELECT t2.id FROM translations t2
                    JOIN sources s2 ON t2.source_id = s2.id
                    WHERE t2.term_id = t.term_id
                    ORDER BY s2.priority ASC, t2.id ASC
                    LIMIT 1
                )
            )
        """)
        conn.commit()

        # Delete orphan terms (terms with no translations left)
        orphans = conn.execute(
            "SELECT COUNT(*) FROM terms t WHERE NOT EXISTS (SELECT 1 FROM translations tr WHERE tr.term_id = t.id)"
        ).fetchone()[0]
        if orphans > 0:
            conn.execute(
                "DELETE FROM terms WHERE id NOT IN (SELECT DISTINCT term_id FROM translations)"
            )
            conn.commit()
            print(f"  Removed {orphans} orphan terms (no translations left)")

        unique = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
        translations = conn.execute("SELECT COUNT(*) FROM translations").fetchone()[0]
        print(f"  Unique terms: {unique}")
        print(f"  Total translations: {translations}")

        print("\n=== Step 5: Re-exporting ===")
        conn.close()
        sys.path.insert(0, SCRIPT_DIR)
        from importlib import import_module
        build = import_module("build-glossary-db")
        build.export_all()
    else:
        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY (dry run)")
        print(f"  Duplicate groups to merge: {len(duplicates)}")
        print(f"  Term merges: {merged}")
        print(f"  ai-tamil-glossary translations to remove: {removed}")
        print(f"\nRun with --apply to commit changes and re-export.")
        print("=" * 60)
        conn.close()


if __name__ == "__main__":
    main()
