# docs-glossary

Supporting glossary materials for the Tamil AI Glossary project. These are a
**reference, not a core deliverable** — the deliverables are `ai-tamil-glossary.md`
and the `book/`. This directory exists to source Tamil root words (வேர்ச்சொற்கள்)
for the AI glossary. See [`../db/README.md`](../db/README.md) for the full data
pipeline, sources, and editing rules.

## Consolidated glossary

A single consolidated set of ~12,560 English–Tamil technical terms aggregated from
multiple sources (AI terms from this project + சொல்லாய்வு குழு, plus computing terms
from Anna University, மு.சிவலிங்கம், மணவை முஸ்தபா, and others).

| File | Role |
|------|------|
| [`consolidated-glossary.csv`](consolidated-glossary.csv) | **Canonical source of truth.** All edits happen here. Columns: `english, english_normalized, domain, primary_tamil, all_alternatives, sources`. |
| [`consolidated-glossary.md`](consolidated-glossary.md) | Rendered Markdown view of the full glossary. Auto-generated from the CSV — do not edit by hand. |

To edit: change the CSV, then regenerate the derived outputs:

```bash
python3 scripts/regenerate-from-csv.py --db   # rebuild consolidated-glossary.md + db/glossary.db
python3 scripts/split-glossary-az.py          # rebuild the az/ split files
```

## [`az/`](az/) — A-Z lookup

The consolidated glossary split into one file per starting letter for quick lookup
by hand. Start at [`az/README.md`](az/README.md) for the per-letter index and term
counts. Auto-generated from the CSV by `scripts/split-glossary-az.py` — do not edit
the split files directly; edit the CSV and regenerate.

## Other contents

- `references/` — raw source files the consolidated glossary was built from (Anna
  University, மு.சிவலிங்கம், Wikisource (மனவை முஸ்தபா), aangilam.org, India Govt, அ.கி. மூர்த்தி).
- `ai-glossary-facebook-sollaivu.md` and `deviations-from-sollaayvu.md` are AI-specific
  reference files described in the [root README](../README.md).
