#!/usr/bin/env python3
"""
De-duplicate plural forms from consolidated-glossary.csv.

For each pair where both "X" and "Xs" (or "X" and "Xes", "Xies") exist:
- Keep the singular form
- Merge any unique Tamil translations and sources from the plural into the singular
- Remove the plural row

Also handles common plural patterns:
  - word → words
  - address → addresses (es suffix)
  - entry → entries (ies suffix)
  - index → indices / indexes
  - matrix → matrices
  - bus → buses

Usage:
    python3 scripts/dedup-plurals.py              # dry-run (report only)
    python3 scripts/dedup-plurals.py --apply      # write cleaned CSV
"""

import csv
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(PROJECT_ROOT, "docs-glossary", "consolidated-glossary.csv")
CSV_BACKUP = CSV_PATH + ".bak"


# Terms that should NEVER be singularized (abbreviations, proper names, etc.)
# Checked against the full normalized term
EXCLUDE_TERMS = {
    "bbs", "cals", "caps", "cts", "des", "gps", "https", "ipcs",
    "kbs", "kcs", "mus", "sos", "ups", "eds", "ibis", "ices",
    "flops", "perts", "specs", "stats", "win32s",
    "computer graphics", "electronics", "diagnostics",
    "windows",
}


def to_singular_candidates(plural):
    """Given a normalized term, return possible singular forms.
    Candidates ordered from most likely to least likely."""
    candidates = []
    words = plural.split()
    if not words:
        return candidates

    last = words[-1]

    # Don't try to singularize very short words (likely abbreviations)
    if len(last) <= 3:
        return candidates

    # Skip if the full term is in the exclusion list
    if plural in EXCLUDE_TERMS:
        return candidates

    # ies → y (e.g. entries → entry, directories → directory)
    if last.endswith("ies") and len(last) > 4:
        candidates.append(" ".join(words[:-1] + [last[:-3] + "y"]))

    # ices → ix (e.g. indices → index, matrices → matrix)
    if last.endswith("ices") and len(last) > 5:
        candidates.append(" ".join(words[:-1] + [last[:-4] + "ix"]))

    # ses, xes, ches, shes → remove es (e.g. addresses → address, buses → bus)
    if last.endswith("ses") or last.endswith("xes") or last.endswith("ches") or last.endswith("shes"):
        candidates.append(" ".join(words[:-1] + [last[:-2]]))

    # For -es words: try removing just -s FIRST (tapes→tape), then -es (caches→cach)
    # This ensures 'tape' is tried before 'tap'
    if last.endswith("es") and not last.endswith("ies"):
        candidates.append(" ".join(words[:-1] + [last[:-1]]))  # -s: tapes→tape
        candidates.append(" ".join(words[:-1] + [last[:-2]]))  # -es: tapes→tap

    # s → remove s (e.g. networks → network)
    if last.endswith("s") and not last.endswith("ss") and not last.endswith("es"):
        candidates.append(" ".join(words[:-1] + [last[:-1]]))

    return candidates


def merge_translations(singular_row, plural_row):
    """Merge plural row's translations and sources into singular row."""
    # Parse existing translations
    s_primary = singular_row["primary_tamil"]
    s_all = singular_row["all_alternatives"]
    s_sources = singular_row["sources"]

    p_all = plural_row["all_alternatives"]
    p_sources = plural_row["sources"]

    # Merge alternatives (deduplicate)
    existing = set(t.strip() for t in s_all.split(",") if t.strip()) if s_all else set()
    new_terms = set(t.strip() for t in p_all.split(",") if t.strip()) if p_all else set()
    merged_terms = list(existing)
    for t in new_terms:
        if t not in existing:
            merged_terms.append(t)

    # Merge sources (deduplicate)
    existing_src = set(s.strip() for s in s_sources.split(",") if s.strip()) if s_sources else set()
    new_src = set(s.strip() for s in p_sources.split(",") if s.strip()) if p_sources else set()
    merged_src = list(existing_src)
    for s in new_src:
        if s not in existing_src:
            merged_src.append(s)

    singular_row["all_alternatives"] = ",".join(merged_terms)
    singular_row["sources"] = ",".join(merged_src)
    return singular_row


def main():
    dry_run = "--apply" not in sys.argv

    if not os.path.exists(CSV_PATH):
        print(f"ERROR: {CSV_PATH} not found.")
        sys.exit(1)

    # Read CSV
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Read {len(rows)} rows from CSV")

    # Index by normalized english
    by_norm = {}
    for i, row in enumerate(rows):
        norm = row["english_normalized"].strip().lower()
        by_norm[norm] = i

    # Find plural → singular pairs
    to_remove = set()  # indices to remove
    merge_log = []

    for i, row in enumerate(rows):
        if i in to_remove:
            continue
        norm = row["english_normalized"].strip().lower()

        # Try to find if this is a plural of an existing singular
        singular_candidates = to_singular_candidates(norm)
        for sing in singular_candidates:
            if sing in by_norm and by_norm[sing] != i:
                sing_idx = by_norm[sing]
                if sing_idx not in to_remove:
                    # Found: this row (plural) has a singular counterpart
                    merge_log.append((norm, sing, rows[sing_idx]["english"]))
                    if not dry_run:
                        rows[sing_idx] = merge_translations(rows[sing_idx], row)
                    to_remove.add(i)
                    break  # only merge once

    # Report
    print(f"\nFound {len(merge_log)} plural → singular merges:\n")
    for plural, singular, eng in sorted(merge_log):
        print(f"  {plural:40s} → {singular}")

    if dry_run:
        print(f"\n{'='*60}")
        print(f"DRY RUN — {len(merge_log)} rows would be removed.")
        print(f"Run with --apply to write changes.")
        print(f"{'='*60}")
    else:
        # Backup original
        import shutil
        shutil.copy2(CSV_PATH, CSV_BACKUP)
        print(f"\nBackup saved: {CSV_BACKUP}")

        # Write cleaned CSV
        cleaned = [row for i, row in enumerate(rows) if i not in to_remove]
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cleaned)

        print(f"Wrote {len(cleaned)} rows (removed {len(to_remove)} plurals)")
        print(f"CSV updated: {CSV_PATH}")


if __name__ == "__main__":
    main()
