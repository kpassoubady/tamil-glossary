#!/usr/bin/env python3
"""
Regenerate consolidated-glossary.md and db/glossary.db from the
canonical consolidated-glossary.csv.

Usage:
    python3 scripts/regenerate-from-csv.py          # regenerate MD only
    python3 scripts/regenerate-from-csv.py --db     # also rebuild DB from CSV
"""

import csv
import os
import sqlite3
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CSV_PATH = os.path.join(PROJECT_ROOT, "docs-glossary", "consolidated-glossary.csv")
MD_PATH = os.path.join(PROJECT_ROOT, "docs-glossary", "consolidated-glossary.md")
DB_DIR = os.path.join(PROJECT_ROOT, "db")
DB_PATH = os.path.join(DB_DIR, "glossary.db")

# Source priority for the header (author names)
SOURCE_PRIORITY = [
    "காங்கேயன் பசுபதி",
    "சொல்லாய்வு குழு",
    "அண்ணா பல்கலைக்கழகம்",
    "மு.சிவலிங்கம்",
    "அ.கி. மூர்த்தி",
    "மணவை முஸ்தபா",
    "aangilam.org",
    "இந்திய அரசு",
]


def read_csv():
    """Read the canonical CSV."""
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"Read {len(rows)} rows from {CSV_PATH}")
    return rows


def generate_md(rows):
    """Generate markdown from CSV rows."""
    priority_str = " > ".join(SOURCE_PRIORITY)

    lines = [
        "# Consolidated Tamil Computing & AI Glossary",
        "",
        f"> Total unique terms: {len(rows)}",
        "> Auto-generated from consolidated-glossary.csv",
        f"> Primary term (★) chosen by source priority: {priority_str}",
        "",
        "| # | English | Primary Tamil (★) | All Alternatives | Domain | Sources |",
        "|---|---------|-------------------|------------------|--------|---------|",
    ]

    for i, row in enumerate(rows, 1):
        eng = row["english"].replace("|", "\\|")
        primary = (row.get("primary_tamil") or "").replace("|", "\\|")
        domain = row.get("domain", "general")
        sources = (row.get("sources") or "").replace("|", "\\|")

        # Build alternatives (all_alternatives minus primary)
        all_alt = row.get("all_alternatives", "")
        if all_alt:
            alt_terms = []
            seen = set()
            for t in all_alt.split(","):
                t = t.strip()
                if t and t not in seen and t != row.get("primary_tamil", "").strip():
                    seen.add(t)
                    alt_terms.append(t)
            alt_str = " / ".join(alt_terms) if alt_terms else "—"
        else:
            alt_str = "—"
        alt_str = alt_str.replace("|", "\\|")

        lines.append(f"| {i} | {eng} | {primary} | {alt_str} | {domain} | {sources} |")

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Markdown exported: {MD_PATH} ({len(rows)} terms)")


def rebuild_db(rows):
    """Rebuild glossary.db from CSV rows."""
    os.makedirs(DB_DIR, exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            short_name TEXT NOT NULL UNIQUE,
            author TEXT DEFAULT '',
            priority INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS terms (
            id INTEGER PRIMARY KEY,
            english TEXT NOT NULL,
            english_normalized TEXT NOT NULL UNIQUE,
            domain TEXT DEFAULT 'general',
            primary_tamil TEXT DEFAULT '',
            all_alternatives TEXT DEFAULT '',
            sources TEXT DEFAULT ''
        );

        CREATE INDEX IF NOT EXISTS idx_terms_norm ON terms(english_normalized);
        CREATE INDEX IF NOT EXISTS idx_terms_domain ON terms(domain);
    """)

    # Insert source metadata
    for i, author in enumerate(SOURCE_PRIORITY, 1):
        conn.execute(
            "INSERT OR IGNORE INTO sources (name, short_name, author, priority) VALUES (?, ?, ?, ?)",
            (author, author, author, i),
        )

    # Insert terms from CSV
    for row in rows:
        conn.execute(
            """INSERT OR IGNORE INTO terms
               (english, english_normalized, domain, primary_tamil, all_alternatives, sources)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                row["english"],
                row["english_normalized"],
                row.get("domain", "general"),
                row.get("primary_tamil", ""),
                row.get("all_alternatives", ""),
                row.get("sources", ""),
            ),
        )

    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
    print(f"DB rebuilt: {DB_PATH} ({count} terms)")
    conn.close()


def main():
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: {CSV_PATH} not found.")
        sys.exit(1)

    rows = read_csv()
    generate_md(rows)

    if "--db" in sys.argv:
        rebuild_db(rows)
        # Remove old glossary.db from project root if it exists
        old_db = os.path.join(PROJECT_ROOT, "glossary.db")
        if os.path.exists(old_db):
            print(f"\nNote: old {old_db} still exists. You can remove it:")
            print(f"  rm {old_db}")

    print("\nDone.")


if __name__ == "__main__":
    main()
