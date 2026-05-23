#!/usr/bin/env python3
"""
One-time script to:
1. Fix k-murthy author typo: அ.க. மூர்த்தி → அ.கி. மூர்த்தி
2. Analyze ai-tamil-glossary ↔ sollaaayvu overlap
3. Report which ai-tamil-glossary terms are new coins (காங்கேயன் பசுபதி only)
   vs. shared with sollaaayvu (சொல்லாய்வு குழு)

Usage:
    python3 scripts/update-authors.py          # analyze + fix typo
    python3 scripts/update-authors.py --export # also re-export md/csv
"""

import os
import sqlite3
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "glossary.db")


def main():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: {DB_PATH} not found.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)

    # ---------------------------------------------------------------
    # 1. Fix k-murthy author typo
    # ---------------------------------------------------------------
    print("=== Fix k-murthy author typo ===")
    old = conn.execute("SELECT author FROM sources WHERE short_name='k-murthy'").fetchone()
    print(f"  Before: {old[0]!r}")
    conn.execute("UPDATE sources SET author='அ.கி. மூர்த்தி' WHERE short_name='k-murthy'")
    conn.commit()
    new = conn.execute("SELECT author FROM sources WHERE short_name='k-murthy'").fetchone()
    print(f"  After:  {new[0]!r}")
    print()

    # ---------------------------------------------------------------
    # 2. Overlap analysis: ai-tamil-glossary vs sollaaayvu vs others
    # ---------------------------------------------------------------
    print("=== ai-tamil-glossary overlap analysis ===")

    ai_terms = set(r[0] for r in conn.execute("""
        SELECT DISTINCT t.english_normalized FROM terms t
        JOIN translations tr ON t.id = tr.term_id
        JOIN sources s ON tr.source_id = s.id
        WHERE s.short_name = 'ai-tamil-glossary'
    """))

    sol_terms = set(r[0] for r in conn.execute("""
        SELECT DISTINCT t.english_normalized FROM terms t
        JOIN translations tr ON t.id = tr.term_id
        JOIN sources s ON tr.source_id = s.id
        WHERE s.short_name = 'sollaaayvu'
    """))

    other_terms = set(r[0] for r in conn.execute("""
        SELECT DISTINCT t.english_normalized FROM terms t
        JOIN translations tr ON t.id = tr.term_id
        JOIN sources s ON tr.source_id = s.id
        WHERE s.short_name NOT IN ('ai-tamil-glossary')
    """))

    overlap_sol = ai_terms & sol_terms
    only_ai = ai_terms - other_terms
    shared = ai_terms & other_terms

    print(f"  ai-tamil-glossary total terms: {len(ai_terms)}")
    print(f"  sollaaayvu total terms:        {len(sol_terms)}")
    print(f"  ai ∩ sollaaayvu:               {len(overlap_sol)}")
    print(f"  ai ∩ any-other-source:         {len(shared)}")
    print(f"  New coins (ONLY in ai):        {len(only_ai)}")
    print()

    print("--- Terms in ai ∩ sollaaayvu (should credit சொல்லாய்வு குழு) ---")
    for t in sorted(overlap_sol):
        print(f"  {t}")
    print()

    print("--- New coins (only in ai-tamil-glossary → காங்கேயன் பசுபதி) ---")
    for t in sorted(only_ai):
        print(f"  {t}")
    print()

    # ---------------------------------------------------------------
    # 3. Current sources table
    # ---------------------------------------------------------------
    print("=== Current sources ===")
    for r in conn.execute("SELECT short_name, author, priority FROM sources ORDER BY priority"):
        print(f"  {r[0]:20s} author={r[1]!r:30s} priority={r[2]}")

    conn.close()

    # ---------------------------------------------------------------
    # 4. Optionally re-export
    # ---------------------------------------------------------------
    if "--export" in sys.argv:
        print("\n=== Re-exporting... ===")
        # Import and call export from build script
        sys.path.insert(0, SCRIPT_DIR)
        from importlib import import_module
        build = import_module("build-glossary-db")
        build.export_all()


if __name__ == "__main__":
    main()
