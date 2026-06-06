# Tamil Computing & AI Glossary Database

> **Scope:** This database is a **supporting reference, not a core deliverable** of the
> tamil-glossary project. The deliverables are `ai-tamil-glossary.md` and the `book/`.
> This consolidated computing glossary exists to source Tamil root words (வேர்ச்சொற்கள்)
> for the AI glossary. The dependency is one-way: the build reads `ai-tamil-glossary.md`
> as a priority-1 input, but the AI glossary and book do not depend on this db at runtime.
> Use it as a lookup aid.

## What this contains

`glossary.db` is a SQLite database consolidating **12,560 unique English-Tamil technical terms** from 10 sources:

| Source | Author | Priority | Terms |
|--------|--------|----------|-------|
| ai-tamil-glossary | காங்கேயன் பசுபதி | 1 (highest) | ~311 AI terms |
| sollaaayvu | சொல்லாய்வு குழு | 2 | ~130 AI terms |
| anna-univ | அண்ணா பல்கலைக்கழகம் | 3 | ~3,800 computing terms |
| sivalingam-csv | மு.சிவலிங்கம் | 4 | ~680 computing terms |
| k-murthy | அ.கி. மூர்த்தி | 5 | ~75 computing terms |
| wikisource | மணவை முஸ்தபா | 6 | ~10,600 computing terms |
| aangilam | aangilam.org | 7 | ~640 computing terms |
| sivalingam-txt | மு.சிவலிங்கம் | 8 | ~740 domain-tagged terms |
| sivalingam-md | மு.சிவலிங்கம் | 8 | ~45 computing terms |
| india-gov | இந்திய அரசு | 9 | ~25 computing terms |

### Domain tags

Terms are tagged by domain: `ai`, `programming`, `networking`, `database`, `internet`, `hardware`, `office`, `mobile`, `security`, `general`.

### Primary term selection

When multiple Tamil translations exist for one English term, the **primary** is chosen from the highest-priority source (lowest priority number).

## Canonical source of truth

The editable source of truth is:

```
docs-glossary/consolidated-glossary.csv
```

The DB and all other exports are regenerated from this CSV.

## Adding a new glossary source

### Step 1: Prepare the source file

Place the new file in `docs-glossary/` (or `docs-glossary/references/` for raw scraped data).

### Step 2: Option A — Add via build script (for bulk source files)

1. Add a parser function in `scripts/build-glossary-db.py` matching the file format
2. Add an entry to the `SOURCES` list with `(short_name, filepath, year, priority, parser_key, url, author)`
3. Assign a priority number (lower = higher authority)
4. Run: `python3 scripts/build-glossary-db.py`
5. Review the exported CSV and MD

### Step 2: Option B — Edit the CSV directly (for small additions)

1. Add rows to `docs-glossary/consolidated-glossary.csv`
2. Ensure the format: `english,english_normalized,domain,primary_tamil,all_alternatives,sources`
3. Run cleanup and regenerate (see below)

### Step 3: Clean up

Run the plural deduplication script:

```bash
python3 scripts/dedup-plurals.py        # dry-run first
python3 scripts/dedup-plurals.py --apply
```

### Step 4: Regenerate all outputs

```bash
python3 scripts/regenerate-from-csv.py --db   # regenerate MD + rebuild DB
python3 scripts/split-glossary-az.py           # regenerate A-Z split files
```

## Data quality rules

Follow these when adding or editing terms:

### Normalization

- `english_normalized` = lowercase, trimmed, collapsed whitespace, no trailing `.` or `:`
- Used for deduplication — two terms with the same normalized form are considered duplicates

### Plurals

- **Keep singular forms only.** If both `network` and `networks` exist, keep `network` and merge translations.
- **Exception — abbreviations ending in 's':** keep as-is. Examples: `BBS`, `GPS`, `HTTPS`, `UPS`, `CAPS`, `CTS`, `FLOPS`, `SPECS`
- **Exception — field names that are inherently plural:** `computer graphics`, `electronics`, `diagnostics`, `windows` (OS)
- The `scripts/dedup-plurals.py` script handles this automatically with an `EXCLUDE_TERMS` set.

### Abbreviations

- Keep abbreviations as-is (e.g., `CPU`, `RAM`, `HTTP`)
- Do not singularize abbreviation plurals (e.g., keep `BBS`, not `BB`)
- Tamil transliterations of abbreviations are valid entries (e.g., `CPU` → `சிபியூ`)

### Author attribution

- Every source must have an `author` field
- The `sources` column in the CSV shows author names (not short_names)
- When a term exists in multiple sources, all contributing authors are listed
- `ai-tamil-glossary` terms that also appear in `sollaaayvu` should credit `சொல்லாய்வு குழு`
- Only genuinely new coinages in `ai-tamil-glossary` should credit `காங்கேயன் பசுபதி`

### Domain tagging

- Assigned automatically by keyword heuristics in `build-glossary-db.py`
- `sivalingam-txt` source has domain headers (e.g., `(3) இணையம் (Internet)`) — these take precedence
- Valid domains: `ai`, `programming`, `networking`, `database`, `internet`, `hardware`, `office`, `mobile`, `security`, `general`

## Scripts reference

| Script | Purpose |
|--------|---------|
| `scripts/build-glossary-db.py` | Full rebuild from source files → DB + CSV + MD |
| `scripts/regenerate-from-csv.py` | Rebuild MD + DB from edited CSV |
| `scripts/regenerate-from-csv.py --db` | Also rebuild `db/glossary.db` |
| `scripts/dedup-plurals.py` | Find and merge plural duplicates in CSV |
| `scripts/split-glossary-az.py` | Split CSV into A-Z markdown files |
| `scripts/fix-duplicates-and-attribution.py` | Fix parenthetical dupes + attribution in DB |
| `scripts/update-authors.py` | Update author fields in DB |
| `scripts/scrape-wikisource-terms.py` | Scrape terms from Tamil Wikisource |
| `scripts/scrape-aangilam-terms.py` | Scrape terms from aangilam.org |

## Querying the DB

```bash
# Count terms by domain
sqlite3 db/glossary.db "SELECT domain, COUNT(*) FROM terms GROUP BY domain ORDER BY COUNT(*) DESC;"

# Find a term
sqlite3 db/glossary.db "SELECT english, primary_tamil, sources FROM terms WHERE english_normalized LIKE '%neural%';"

# All terms from a specific author
sqlite3 db/glossary.db "SELECT english, primary_tamil FROM terms WHERE sources LIKE '%சிவலிங்கம்%' LIMIT 20;"
```
