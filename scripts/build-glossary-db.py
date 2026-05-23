#!/usr/bin/env python3
"""
Consolidate all Tamil glossary sources into a single SQLite database.

Sources are parsed, normalized, deduplicated, and stored with:
- Source attribution per translation
- Priority-based primary term selection
- Heuristic domain tagging

Exports: consolidated-glossary.md and consolidated-glossary.csv

Usage:
    python3 scripts/build-glossary-db.py          # build DB + export
    python3 scripts/build-glossary-db.py --export  # export only (DB must exist)
    python3 scripts/build-glossary-db.py --stats   # print statistics
"""

import csv
import os
import re
import sqlite3
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
GLOSSARY_DIR = os.path.join(PROJECT_ROOT, "docs-glossary")
DB_PATH = os.path.join(PROJECT_ROOT, "glossary.db")
EXPORT_MD = os.path.join(GLOSSARY_DIR, "consolidated-glossary.md")
EXPORT_CSV = os.path.join(GLOSSARY_DIR, "consolidated-glossary.csv")

# ---------------------------------------------------------------------------
# Source definitions: (short_name, filename, year, priority, parser_key, url, author)
# Lower priority number = higher authority
# ---------------------------------------------------------------------------
SOURCES = [
    ("ai-tamil-glossary", "ai-tamil-glossary.md", 2025, 1,
     "ai_glossary", "", "காங்கேயன் பசுபதி"),
    ("sollaaayvu", "docs-glossary/ai-glossary-facebook-sollaivu.md", 2024, 2,
     "sollaaayvu", "https://www.facebook.com/groups/col.aayvu", "சொல்லாய்வு குழு"),
    ("anna-univ", "docs-glossary/computing-glossary.md", 1998, 3,
     "computing_glossary", "", "அண்ணா பல்கலைக்கழகம்"),
    ("sivalingam-csv", "docs-glossary/m-sivalingam-collection.md", 2020, 4,
     "sivalingam_csv", "", "மு.சிவலிங்கம்"),
    ("k-murthy", "docs-glossary/computing-k-murthy.md", 2000, 5,
     "k_murthy", "", "அ.கி. மூர்த்தி"),
    ("wikisource", "docs-glossary/wikisource-computer-glossary.md", 2010, 6,
     "wikisource", "https://ta.wikisource.org", "மணவை முஸ்தபா"),
    ("aangilam", "docs-glossary/aangilam-computer-terms.md", 2010, 7,
     "aangilam", "https://www.aangilam.org", "aangilam.org"),
    ("sivalingam-txt", "docs-glossary/computer-terms-m-sivalingam.txt", 2020, 8,
     "sivalingam_domain_txt", "", "மு.சிவலிங்கம்"),
    ("sivalingam-md", "docs-glossary/m-sivalingam-collction.md", 2020, 8,
     "sivalingam_md", "", "மு.சிவலிங்கம்"),
    ("india-gov", "docs-glossary/computer-terms-india-gov.txt", 2020, 9,
     "tab_separated", "", "இந்திய அரசு"),
]

# ---------------------------------------------------------------------------
# Domain tagging heuristics (keyword → domain)
# ---------------------------------------------------------------------------
DOMAIN_KEYWORDS = {
    "ai": [
        "neural", "network", "learning", "model", "inference", "training",
        "token", "prompt", "embedding", "transformer", "attention", "agent",
        "hallucination", "fine-tun", "rlhf", "rag", "llm", "nlp",
        "generative", "diffusion", "autoencoder", "backpropagation",
        "classification", "clustering", "regression", "reinforcement",
        "supervised", "unsupervised", "activation", "gradient", "epoch",
        "batch", "dropout", "overfitting", "underfitting", "benchmark",
        "distillation", "quantization", "pruning", "alignment",
        "reasoning", "chatgpt", "deepseek", "gpt", "bert", "gemini",
        "copilot", "chatbot", "ai ", "artificial intelligence",
    ],
    "networking": [
        "network", "server", "client", "router", "firewall", "protocol",
        "lan", "wan", "vpn", "intranet", "extranet", "gateway", "hub",
        "switch", "bridge", "proxy", "bandwidth", "broadband", "modem",
        "cable", "wireless", "topology", "packet", "broadcast",
        "multicast", "unicast", "connector", "baseband", "wideband",
    ],
    "database": [
        "database", "sql", "query", "record", "field", "table",
        "index", "primary key", "foreign key", "normalization",
        "relational", "data warehouse", "data mine", "data bank",
        "redundancy", "commit", "trigger", "schema",
    ],
    "programming": [
        "program", "code", "compiler", "interpreter", "debug",
        "variable", "function", "class", "object", "array", "stack",
        "loop", "pointer", "inheritance", "polymorphism", "encapsulation",
        "expression", "operator", "routine", "subroutine", "module",
        "thread", "exception", "binary", "decimal", "hexadecimal",
        "algorithm", "flow chart", "statement", "command",
    ],
    "internet": [
        "internet", "web", "browser", "email", "e-mail", "url",
        "download", "upload", "bookmark", "cookie", "blog", "online",
        "offline", "domain", "portal", "hyperlink", "hypertext",
        "e-commerce", "e-govern", "spam", "cyber",
    ],
    "hardware": [
        "cpu", "processor", "memory", "ram", "rom", "disk", "printer",
        "monitor", "keyboard", "mouse", "scanner", "motherboard",
        "chip", "cache", "port", "bus", "socket", "slot",
        "hard disk", "floppy", "dvd", "cd", "plotter", "hardware",
    ],
    "office": [
        "word processor", "spreadsheet", "document", "format",
        "header", "footer", "margin", "indent", "font", "bold",
        "italic", "underline", "template", "macro", "chart",
        "presentation", "table", "cell", "row", "column",
    ],
    "mobile": [
        "phone", "call", "message", "sms", "sim", "ringtone",
        "gallery", "camera", "alarm", "calendar", "contact",
        "smart phone", "cellphone",
    ],
    "security": [
        "security", "encryption", "decryption", "cryptography",
        "password", "firewall", "authentication", "virus", "malware",
        "spyware", "antivirus", "login", "logout",
    ],
}


def normalize_english(text):
    """Normalize English term for deduplication."""
    text = text.strip()
    # Remove trailing periods, colons
    text = text.rstrip(".:")
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


def guess_domain(english_term):
    """Heuristic domain tagging based on keywords."""
    en_lower = english_term.lower()
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in en_lower)
        if score > 0:
            scores[domain] = score
    if not scores:
        return "general"
    return max(scores, key=scores.get)


# ---------------------------------------------------------------------------
# Parsers for each source format
# ---------------------------------------------------------------------------

def parse_ai_glossary(filepath):
    """Parse ai-tamil-glossary.md: | English | Primary Tamil | Alt Tamil | Notes |"""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            # parts[0] is empty (before first |), parts[-1] is empty (after last |)
            parts = [p for p in parts if p]
            if len(parts) < 3:
                continue
            eng = parts[0]
            if eng in ("English", "---", ""):
                continue
            if eng.startswith("---"):
                continue
            primary_tamil = parts[1]
            alt_tamil = parts[2] if len(parts) > 2 else ""
            definition = parts[3] if len(parts) > 3 else ""

            # Add primary term
            if primary_tamil and primary_tamil != "—":
                entries.append((eng, primary_tamil, definition))
            # Add alternate as separate entry
            if alt_tamil and alt_tamil != "—":
                # May contain multiple separated by /
                for alt in re.split(r"\s*/\s*", alt_tamil):
                    alt = alt.strip()
                    if alt:
                        entries.append((eng, alt, ""))
    return entries


def parse_sollaaayvu(filepath):
    """Parse ai-glossary-facebook-sollaivu.md: | English | Tamil |"""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            parts = [p for p in parts if p]
            if len(parts) < 2:
                continue
            eng = parts[0].strip("*")
            tam = parts[1].strip("*")
            if eng.lower() in ("english", "---", ""):
                continue
            if eng.startswith("---") or eng.startswith("-"):
                continue
            # Tamil may have multiple: "மேகக் கணிமை/முகில் கணிமை"
            for t in re.split(r"[,/]", tam):
                t = t.strip()
                if t:
                    entries.append((eng, t, ""))
    return entries


def parse_computing_glossary(filepath):
    """Parse computing-glossary.md: | ஆங்கிலம் | தமிழ் |"""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            parts = [p for p in parts if p]
            if len(parts) < 2:
                continue
            eng = parts[0]
            tam = parts[1]
            if eng in ("ஆங்கிலம்", "---", "") or eng.startswith("---"):
                continue
            # Tamil field may contain definition after colon or comma
            # e.g. "Analog-to-Digital -என்பதன் குறுக்கம்: ஒப்பு-லக்க மா"
            # Try to split: if it contains both Tamil and a description
            # For this source, the Tamil field is the whole thing
            # Some have comma-separated alternatives
            for t in re.split(r",\s*", tam):
                t = t.strip()
                if t:
                    entries.append((eng, t, ""))
    return entries


def parse_sivalingam_csv(filepath):
    """Parse m-sivalingam-collection.md: CSV format English,Tamil"""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line == "English,Tamil":
                continue
            # CSV-like: first comma splits English from Tamil
            parts = line.split(",", 1)
            if len(parts) < 2:
                continue
            eng = parts[0].strip()
            tam = parts[1].strip()
            if not eng or not tam:
                continue
            for t in re.split(r"\s*/\s*", tam):
                t = t.strip()
                if t:
                    entries.append((eng, t, ""))
    return entries


def parse_k_murthy(filepath):
    """Parse computing-k-murthy.md: | English | Tamil | Definition |"""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            parts = [p for p in parts if p]
            if len(parts) < 2:
                continue
            eng = parts[0]
            tam = parts[1]
            defn = parts[2] if len(parts) > 2 else ""
            if eng in ("English Term", "---", "") or eng.startswith("---"):
                continue
            entries.append((eng, tam, defn))
    return entries


def parse_wikisource(filepath):
    """Parse wikisource-computer-glossary.md: | # | English | Tamil |"""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            parts = [p for p in parts if p]
            if len(parts) < 3:
                continue
            # First column is row number
            eng = parts[1]
            tam = parts[2]
            if eng in ("English", "#", "---", "") or eng.startswith("---"):
                continue
            try:
                int(parts[0])  # verify first col is a number
            except ValueError:
                continue
            tam = tam.strip().rstrip(".")
            if eng and tam:
                entries.append((eng, tam, ""))
    return entries


def parse_aangilam(filepath):
    """Parse aangilam-computer-terms.md: | # | English | Tamil |"""
    return parse_wikisource(filepath)  # same format


def parse_dash_separated(filepath):
    """Parse simple dash-separated files: English --- Tamil (no domain headers)."""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "---" not in line:
                continue
            parts = line.split("---", 1)
            if len(parts) < 2:
                continue
            eng = parts[0].strip()
            tam = parts[1].strip()
            if not eng or not tam:
                continue
            for t in re.split(r"\s*/\s*", tam):
                t = t.strip()
                if t:
                    entries.append((eng, t, ""))
    return entries


# Map Tamil/English section names to domain tags
_SECTION_DOMAIN_MAP = {
    "general": "general",
    "பொது": "general",
    "office": "office",
    "அலுவலகப் பயன்பாடுகள்": "office",
    "internet": "internet",
    "இணையம்": "internet",
    "network": "networking",
    "பிணையம்": "networking",
    "database": "database",
    "தரவுத்தளம்": "database",
    "programming": "programming",
    "நிரலாக்கம்": "programming",
    "cellphone": "mobile",
    "செல்பேசி": "mobile",
}


def _section_to_domain(header):
    """Extract domain from a section header like '(3) இணையம் (Internet)'."""
    # Try English name in parens
    m = re.search(r"\(([A-Za-z ]+)\)\s*$", header)
    if m:
        key = m.group(1).strip().lower()
        if key in _SECTION_DOMAIN_MAP:
            return _SECTION_DOMAIN_MAP[key]
    # Try Tamil name
    for tamil_key, domain in _SECTION_DOMAIN_MAP.items():
        if tamil_key in header:
            return domain
    return "general"


def parse_sivalingam_domain_txt(filepath):
    """Parse computer-terms-m-sivalingam.txt: domain headers + English --- Tamil."""
    entries = []  # (eng, tam, defn, domain)
    current_domain = "general"
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Section header like (1) பொது (General) or (6) நிரலாக்கம் (Programming) ---
            if re.match(r"^\(\d+\)\s+", line):
                current_domain = _section_to_domain(line)
                continue
            if "---" not in line:
                continue
            parts = line.split("---", 1)
            if len(parts) < 2:
                continue
            eng = parts[0].strip()
            tam = parts[1].strip()
            if not eng or not tam:
                continue
            for t in re.split(r"\s*/\s*", tam):
                t = t.strip()
                if t:
                    entries.append((eng, t, "", current_domain))
    return entries


def parse_sivalingam_md(filepath):
    """Parse m-sivalingam-collction.md: markdown table | English | Tamil |."""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|")]
            parts = [p for p in parts if p]
            if len(parts) < 2:
                continue
            eng = parts[0]
            tam = parts[1]
            if eng.startswith("---") or eng.startswith("ஆங்கிலம்"):
                continue
            # Handle combined entries like "Portable Computer / Tablet PC"
            eng_parts = re.split(r"\s*/\s*", eng)
            tam_parts = re.split(r"\s*/\s*", tam)
            if len(eng_parts) == len(tam_parts):
                for e, t in zip(eng_parts, tam_parts):
                    e, t = e.strip(), t.strip()
                    if e and t:
                        entries.append((e, t, ""))
            else:
                # Just add all tamil terms for the first english term
                for t in tam_parts:
                    t = t.strip()
                    if t and eng.strip():
                        entries.append((eng.strip(), t, ""))
    return entries


def parse_tab_separated(filepath):
    """Parse computer-terms2.txt: English\tTamil"""
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "\t" not in line:
                continue
            parts = line.split("\t", 1)
            if len(parts) < 2:
                continue
            eng = parts[0].strip()
            tam = parts[1].strip()
            if eng in ("ஆங்கிலச் சொற்கள்", ""):
                continue
            if eng and tam:
                entries.append((eng, tam, ""))
    return entries


PARSERS = {
    "ai_glossary": parse_ai_glossary,
    "sollaaayvu": parse_sollaaayvu,
    "computing_glossary": parse_computing_glossary,
    "sivalingam_csv": parse_sivalingam_csv,
    "k_murthy": parse_k_murthy,
    "wikisource": parse_wikisource,
    "aangilam": parse_aangilam,
    "dash_separated": parse_dash_separated,
    "sivalingam_domain_txt": parse_sivalingam_domain_txt,
    "sivalingam_md": parse_sivalingam_md,
    "tab_separated": parse_tab_separated,
}


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------

def create_db(conn):
    """Create tables."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            short_name TEXT NOT NULL UNIQUE,
            year INTEGER,
            url TEXT,
            author TEXT DEFAULT '',
            priority INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS terms (
            id INTEGER PRIMARY KEY,
            english TEXT NOT NULL,
            english_normalized TEXT NOT NULL UNIQUE,
            domain TEXT DEFAULT 'general'
        );

        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY,
            term_id INTEGER NOT NULL REFERENCES terms(id),
            tamil_term TEXT NOT NULL,
            source_id INTEGER NOT NULL REFERENCES sources(id),
            is_primary BOOLEAN DEFAULT 0,
            definition TEXT DEFAULT '',
            UNIQUE(term_id, tamil_term, source_id)
        );

        CREATE INDEX IF NOT EXISTS idx_terms_norm ON terms(english_normalized);
        CREATE INDEX IF NOT EXISTS idx_translations_term ON translations(term_id);
        CREATE INDEX IF NOT EXISTS idx_translations_primary ON translations(is_primary);
    """)


def insert_source(conn, name, short_name, year, url, author, priority):
    """Insert or update a source."""
    conn.execute(
        """INSERT OR REPLACE INTO sources (name, short_name, year, url, author, priority)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (name, short_name, year, url, author, priority),
    )


def get_source_id(conn, short_name):
    row = conn.execute(
        "SELECT id FROM sources WHERE short_name = ?", (short_name,)
    ).fetchone()
    return row[0] if row else None


def get_or_create_term(conn, english, english_normalized, domain):
    """Get existing term or create new one."""
    row = conn.execute(
        "SELECT id FROM terms WHERE english_normalized = ?",
        (english_normalized,),
    ).fetchone()
    if row:
        return row[0]
    cur = conn.execute(
        "INSERT INTO terms (english, english_normalized, domain) VALUES (?, ?, ?)",
        (english, english_normalized, domain),
    )
    return cur.lastrowid


def insert_translation(conn, term_id, tamil_term, source_id, definition=""):
    """Insert a translation, ignoring duplicates."""
    try:
        conn.execute(
            """INSERT OR IGNORE INTO translations
               (term_id, tamil_term, source_id, is_primary, definition)
               VALUES (?, ?, ?, 0, ?)""",
            (term_id, tamil_term, source_id, definition),
        )
    except sqlite3.IntegrityError:
        pass


def set_primary_terms(conn):
    """
    For each term, mark the translation from the highest-priority source
    as primary. If multiple translations from the same source, pick the first.
    """
    # Reset all
    conn.execute("UPDATE translations SET is_primary = 0")

    # For each term, find the translation with the lowest source priority
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


def build_db():
    """Main build: parse all sources, insert into DB, set primaries."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    create_db(conn)

    total_entries = 0
    for (short_name, rel_path, year, priority, parser_key, url, author) in SOURCES:
        filepath = os.path.join(PROJECT_ROOT, rel_path)
        if not os.path.exists(filepath):
            print(f"  SKIP {short_name}: file not found ({rel_path})")
            continue

        insert_source(conn, short_name, short_name, year, url, author, priority)
        source_id = get_source_id(conn, short_name)

        parser = PARSERS[parser_key]
        entries = parser(filepath)
        count = 0
        for entry in entries:
            # Parsers return 3-tuple (eng, tam, defn) or 4-tuple (eng, tam, defn, domain)
            eng, tam, defn = entry[0], entry[1], entry[2]
            source_domain = entry[3] if len(entry) > 3 else ""
            eng = eng.strip()
            tam = tam.strip()
            if not eng or not tam:
                continue
            en_norm = normalize_english(eng)
            if not en_norm:
                continue
            domain = source_domain if source_domain else guess_domain(eng)
            term_id = get_or_create_term(conn, eng, en_norm, domain)
            insert_translation(conn, term_id, tam, source_id, defn)
            count += 1

        total_entries += count
        print(f"  {short_name}: {count} entries from {rel_path}")

    conn.commit()
    print(f"\nTotal raw entries ingested: {total_entries}")

    # Set primary terms based on source priority
    set_primary_terms(conn)
    conn.commit()

    # Stats
    term_count = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
    trans_count = conn.execute("SELECT COUNT(*) FROM translations").fetchone()[0]
    primary_count = conn.execute(
        "SELECT COUNT(*) FROM translations WHERE is_primary = 1"
    ).fetchone()[0]
    print(f"Unique English terms: {term_count}")
    print(f"Total translations: {trans_count}")
    print(f"Primary terms set: {primary_count}")

    conn.close()
    print(f"\nDatabase written to: {DB_PATH}")


def print_stats():
    """Print database statistics."""
    conn = sqlite3.connect(DB_PATH)

    print("=== Glossary Database Statistics ===\n")

    term_count = conn.execute("SELECT COUNT(*) FROM terms").fetchone()[0]
    trans_count = conn.execute("SELECT COUNT(*) FROM translations").fetchone()[0]
    print(f"Unique English terms: {term_count}")
    print(f"Total translations:   {trans_count}")
    print(f"Avg translations/term: {trans_count / max(term_count, 1):.1f}")

    print("\n--- By Source ---")
    rows = conn.execute("""
        SELECT s.short_name, s.priority, COUNT(t.id)
        FROM sources s
        LEFT JOIN translations t ON s.id = t.source_id
        GROUP BY s.id ORDER BY s.priority
    """).fetchall()
    for name, pri, cnt in rows:
        print(f"  [{pri}] {name}: {cnt} translations")

    print("\n--- By Domain ---")
    rows = conn.execute("""
        SELECT domain, COUNT(*) FROM terms GROUP BY domain ORDER BY COUNT(*) DESC
    """).fetchall()
    for domain, cnt in rows:
        print(f"  {domain}: {cnt} terms")

    print("\n--- Terms with most alternatives ---")
    rows = conn.execute("""
        SELECT t.english, COUNT(DISTINCT tr.tamil_term) as cnt
        FROM terms t JOIN translations tr ON t.id = tr.term_id
        GROUP BY t.id ORDER BY cnt DESC LIMIT 15
    """).fetchall()
    for eng, cnt in rows:
        print(f"  {eng}: {cnt} alternatives")

    print("\n--- Sample: terms from your book (ai-tamil-glossary) ---")
    rows = conn.execute("""
        SELECT t.english, tr.tamil_term, tr.is_primary
        FROM terms t
        JOIN translations tr ON t.id = tr.term_id
        JOIN sources s ON tr.source_id = s.id
        WHERE s.short_name = 'ai-tamil-glossary'
        ORDER BY t.english LIMIT 10
    """).fetchall()
    for eng, tam, pri in rows:
        marker = " ★" if pri else ""
        print(f"  {eng} → {tam}{marker}")

    conn.close()


def export_markdown(conn):
    """Export consolidated glossary as markdown."""
    rows = conn.execute("""
        SELECT
            t.english,
            t.domain,
            GROUP_CONCAT(
                CASE WHEN tr.is_primary = 1 THEN tr.tamil_term END
            ) as primary_tamil,
            GROUP_CONCAT(DISTINCT tr.tamil_term) as all_tamil,
            GROUP_CONCAT(DISTINCT CASE WHEN s.author != '' THEN s.author ELSE s.short_name END) as sources
        FROM terms t
        JOIN translations tr ON t.id = tr.term_id
        JOIN sources s ON tr.source_id = s.id
        GROUP BY t.id
        ORDER BY t.english_normalized
    """).fetchall()

    priority_order = conn.execute(
        "SELECT short_name, author FROM sources ORDER BY priority ASC"
    ).fetchall()
    seen_authors = set()
    deduped = []
    for sn, author in priority_order:
        label = author if author else sn
        if label not in seen_authors:
            seen_authors.add(label)
            deduped.append(label)
    priority_str = " > ".join(deduped)

    lines = [
        "# Consolidated Tamil Computing & AI Glossary",
        "",
        f"> Total unique terms: {len(rows)}",
        "> Auto-generated from glossary.db",
        f"> Primary term (★) chosen by source priority: {priority_str}",
        "",
        "| # | English | Primary Tamil (★) | All Alternatives | Domain | Sources |",
        "|---|---------|-------------------|------------------|--------|---------|",
    ]

    for i, (eng, domain, primary, all_tamil, sources) in enumerate(rows, 1):
        # Deduplicate all_tamil
        all_terms = []
        seen = set()
        if all_tamil:
            for t in all_tamil.split(","):
                t = t.strip()
                if t and t not in seen:
                    seen.add(t)
                    all_terms.append(t)

        primary = primary or all_terms[0] if all_terms else ""
        # Remove primary from alternatives list
        alt_list = [t for t in all_terms if t != primary]
        alt_str = " / ".join(alt_list) if alt_list else "—"

        eng_safe = eng.replace("|", "\\|")
        primary_safe = primary.replace("|", "\\|") if primary else ""
        alt_safe = alt_str.replace("|", "\\|")
        src_safe = sources.replace("|", "\\|") if sources else ""

        lines.append(
            f"| {i} | {eng_safe} | {primary_safe} | {alt_safe} | {domain} | {src_safe} |"
        )

    with open(EXPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Markdown exported: {EXPORT_MD} ({len(rows)} terms)")


def export_csv(conn):
    """Export consolidated glossary as CSV."""
    rows = conn.execute("""
        SELECT
            t.english,
            t.english_normalized,
            t.domain,
            GROUP_CONCAT(
                CASE WHEN tr.is_primary = 1 THEN tr.tamil_term END
            ) as primary_tamil,
            GROUP_CONCAT(DISTINCT tr.tamil_term) as all_tamil,
            GROUP_CONCAT(DISTINCT CASE WHEN s.author != '' THEN s.author ELSE s.short_name END) as sources
        FROM terms t
        JOIN translations tr ON t.id = tr.term_id
        JOIN sources s ON tr.source_id = s.id
        GROUP BY t.id
        ORDER BY t.english_normalized
    """).fetchall()

    with open(EXPORT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "english", "english_normalized", "domain",
            "primary_tamil", "all_alternatives", "sources",
        ])
        for (eng, en_norm, domain, primary, all_tamil, sources) in rows:
            writer.writerow([eng, en_norm, domain, primary or "", all_tamil or "", sources or ""])

    print(f"CSV exported: {EXPORT_CSV} ({len(rows)} terms)")


def export_all():
    """Export markdown and CSV from existing DB."""
    if not os.path.exists(DB_PATH):
        print(f"ERROR: {DB_PATH} not found. Run without --export first.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    export_markdown(conn)
    export_csv(conn)
    conn.close()


def main():
    args = sys.argv[1:]
    if "--stats" in args:
        if not os.path.exists(DB_PATH):
            print(f"ERROR: {DB_PATH} not found. Build first.")
            sys.exit(1)
        print_stats()
        return

    if "--export" in args:
        export_all()
        return

    # Default: build + export
    print("Building glossary database...\n")
    build_db()
    print("\nExporting...\n")
    export_all()
    print("\nDone. Run with --stats for detailed statistics.")


if __name__ == "__main__":
    main()
