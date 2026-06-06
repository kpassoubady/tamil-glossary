# Tamil AI Glossary Project

## Project Goal

Expand and simplify `ai-tamil-glossary.md` — a comprehensive Tamil glossary for AI and computing terminology. The glossary follows these principles:

1. சொல்லாய்வு குழுவின் கலைச்சொற்களுக்கு முன்னுரிமை
2. ஒற்றுச் சேர்ந்த ஒற்றைச் சொல் வடிவம் (compound words joined)
3. வடசொற்கள் இயன்றவரை நீக்கப்பட வேண்டும்
4. a + b + c சொல் வேர் விளக்கம் சாத்தியமான இடங்களில்
5. ஒருமை வடிவம் preferred

## Scope: Core vs. Supporting Reference

The **deliverables** of this project are `ai-tamil-glossary.md` and the `book/`. Everything else is supporting infrastructure.

The consolidated computing glossary — `db/glossary.db`, `docs-glossary/consolidated-glossary.{csv,md}`, the `docs-glossary/az/` split files, and the `scripts/build-glossary-db.py` pipeline — is a **supporting reference, not core**. Its purpose is sourcing Tamil root words (வேர்ச்சொற்கள்) for the AI glossary. The dependency runs one way: the build reads `ai-tamil-glossary.md` as a priority-1 input; the AI glossary and book do not depend on the db at runtime. Treat the computing glossary as a lookup aid; do not let it dilute the AI-glossary/book focus. It is kept in this repo (rather than split out) to avoid cross-repo sync, since the build consumes `ai-tamil-glossary.md` directly.

## Required Skills (Apply Automatically)

When editing any Tamil content in this project, **always** apply these skills:

- **tamil-article-review** — fact-check, fix grammar/sandhi/case-marker errors, remove English and Sanskrit borrowings, rewrite in pure Tamil
- **natural-prose-formatting** — no em/en dashes, no bold/italic for emphasis mid-sentence, no list abuse, natural paragraph prose
- **tamil-book-review** — validate chapter structure, term format, mandatory sections (objectives, story, quiz, summary, concept map), cross-chapter consistency, and prose quality for `book/` content

These skills are installed at `~/.claude/skills/` and must not be duplicated into this repo.

## Reference Materials

- `docs-glossary/ai-glossary-செய்யறிவுக்-கலைச்சொற்கள்-சொல்லாய்வு.md` — முகநூல் [சொல்லாய்வு குழு](https://www.facebook.com/groups/col.aayvu) coined AI terms. Primary source for Tamil AI terminology; entries adopted from this list are marked with footnote `[^1]` in the glossary.
- `docs-glossary/deviations-from-sollaayvu.md` — Terms in `ai-tamil-glossary.md` that deviate from the சொல்லாய்வு குழு original, with reasons (spelling joins, sandhi, word changes).
- `docs-glossary/computing-glossary.md` — 1998 Anna University computing glossary (வளர்தமிழ் மன்றம்). Use as a reference for established Tamil computing terms.

## File Structure

```
ai-tamil-glossary.md          # Main glossary (primary deliverable)
docs-glossary/
  ai-glossary-செய்யறிவுக்-கலைச்சொற்கள்-சொல்லாய்வு.md  # Reference: சொல்லாய்வு குழு AI terms
  deviations-from-sollaayvu.md # Deviations from சொல்லாய்வு குழு
  computing-glossary.md        # Reference: Anna University computing terms
.agent/
  workflows/
    push-feature-pr.md         # Gitflow feature branch workflow
```

## Conventions

- All glossary entries use Markdown table format: `| English | Primary Tamil Word | Alternative Tamil Words | Notes / Explanation |`
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)
- Use the Gitflow workflow in `.agent/workflows/push-feature-pr.md` for all changes
- Markdown linting configured via `.markdownlint.json`
- **Markdown List Indentation:** When nesting elements (like tables or sub-lists) inside a numbered list, indent them by exactly 4 spaces and include an empty line before them to prevent PDF conversion issues.
