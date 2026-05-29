# Excalidraw Diagram POC Plan

## Decision

**Option B selected:** Add new Excalidraw-style diagrams in strategic places.
Do NOT bulk-convert existing Mermaid diagrams — keep the proven Mermaid pipeline
for structured flowcharts. Excalidraw diagrams fill a different role (concept maps,
intuition-building sketches).

**UPDATE (2025-05-27):** The Tamil font blocker is resolved. Kavivanar, a free
handwritten Tamil font on Google Fonts, gives true hand-drawn Tamil glyphs.
This makes Option B even stronger — Excalidraw diagrams now look fully hand-drawn
for both English and Tamil text.

**UPDATE (2025-05-28):** POC validated end-to-end in PDF and EPUB.
- SVG output has font-shaping issues in WeasyPrint/EPUB renderers → **PNG output chosen**
- Kavivanar selected over MyHands for better legibility in print
- Diagrams should be **small and simple** (3–6 elements) — cycles, flows, hub-and-spoke
- Complex concept maps (like 01-ai-big-picture) work but are harder to read at PDF scale

## Why Excalidraw (for select diagrams)

- Hand-drawn aesthetic is warmer for concept maps and big-picture overviews
- Complements (not replaces) the structured Mermaid flowcharts/pipelines
- Readers intuitively distinguish "sketch = overview" from "flowchart = technical detail"

## Tamil Font: Kavivanar (Solved)

Excalidraw's Virgil font has no Tamil glyphs, but **Kavivanar** (Google Fonts,
OFL license) is a handwritten-style font with full Tamil + Latin support.

Font URL: `https://fonts.gstatic.com/s/kavivanar/v22/o-0IIpQgyXYSwhxP7_Jb4g.ttf`

### How to use Kavivanar in Excalidraw

**In JSON authoring (fontFamily mapping):**
- `fontFamily: 1` = Virgil (hand-drawn Latin — no Tamil)
- `fontFamily: 2` = Helvetica (normal — fallback)
- When exporting SVG, inject a `@font-face` rule that overrides `fontFamily: 2`
  (or a custom index) to load Kavivanar instead

**In SVG export (font injection):**
```xml
<defs>
  <style>
    @font-face {
      font-family: 'Kavivanar';
      src: url('data:font/ttf;base64,...') format('truetype');
    }
    text { font-family: 'Kavivanar', 'Noto Sans Tamil', sans-serif; }
  </style>
</defs>
```

For Kindle/PDF embedding, base64-encode the .ttf into the SVG so it is
fully self-contained (no external URL dependency).

### Result

- Shapes, arrows, boxes: Excalidraw's sketchy roughness (roughness: 1-2)
- Tamil text: Kavivanar handwritten glyphs
- English text: Kavivanar (also has Latin) or Virgil
- **Fully hand-drawn look for the entire diagram**

## Authoring Approach: Claude-Generated JSON

Instead of using the web editor for every diagram, Claude can generate the
Excalidraw JSON directly from a description. This is effective because:
- Claude handles Tamil text wrapping and positioning in the JSON
- Consistent styling (colors, roughness, fonts) across diagrams
- Version-controlled source (`.excalidraw` JSON in git)
- Quick iteration: describe the diagram, get JSON, drop into excalidraw.com for
  visual fine-tuning if needed

**JSON skeleton conventions:**
- `fillStyle: "hachure"` for the hand-drawn fill pattern
- `roughness: 1` for subtle sketch feel (2 for more dramatic)
- `strokeColor: "#1a4d2e"` (deep green, matches book palette)
- `backgroundColor: "#ffebcd"` (root/highlight nodes), `"#e8f5e9"` (standard),
  `"#e3f2fd"` (special), `"#f3e5f5"` (concepts)
- `fontFamily: 2` for Tamil text (remapped to Kavivanar at export time)
- `roundness: {"type": 3}` for rounded rectangles
- Always include `originalText` field matching `text` for Excalidraw compat

## POC Chapter: 01 (AI Foundations)

### New diagram: `01-ai-big-picture.excalidraw`

A concept-map style diagram showing:
- Central node: செய்யறிவு (AI) — large, sketchy box
- Radiating branches to: levels (ANI → AGI → ASI), modern types (GenAI, Agentic, Multimodal), core concepts (Algorithm, Classification)
- Color palette: same deep green (#1a4d2e) / muted earth tones as existing diagrams
- Hand-drawn arrows, rough boxes — whiteboard feel

This fills a gap: Chapter 01 has no single overview diagram connecting ALL its sections.

### Workflow

1. Describe the diagram concept (what nodes, relationships, layout)
2. Generate Excalidraw JSON (Claude or manual in excalidraw.com)
3. Save as `book/diagrams/NN-name.excalidraw` (JSON source, version-controlled)
4. (Optional) Open in excalidraw.com for visual QA / fine-tuning
5. Run `./scripts/build-excalidraw.sh NN` → auto-exports PNG at 2× with Kavivanar font
6. Reference in chapter: `![alt text](diagrams/NN-name.excalidraw.png)`

### Build Script (working)

Two scripts mirror the existing `build-diagrams.sh` for Mermaid:

- `scripts/build-excalidraw.sh` — shell wrapper, finds `.excalidraw` files,
  auto-installs `puppeteer-core` on first run, outputs PNG
- `scripts/excalidraw-to-svg.mjs` — Node.js converter using headless Chrome +
  `@excalidraw/utils` from esm.sh CDN. Supports both SVG and PNG output.

Usage (same pattern as Mermaid):
```bash
./scripts/build-excalidraw.sh           # all .excalidraw files → PNG
./scripts/build-excalidraw.sh 01        # only 01-*.excalidraw files
```

Font switching (default: kavivanar):
```bash
node scripts/excalidraw-to-svg.mjs --font kavivanar input.excalidraw output.png
node scripts/excalidraw-to-svg.mjs --font myhands   input.excalidraw output.png
```

Available fonts in `scripts/fonts/`:
- `Kavivanar-Regular.ttf` — Google Fonts, OFL (default, best for print)
- `MyHands_2025-Regular.ttf` — CC0 handwritten Tamil (mouse-drawn, more rustic)

One-time setup: `npm install --prefix scripts puppeteer-core`
Requires: Google Chrome installed on the system (uses puppeteer-core, no
Chromium download needed)

## Strategic Placement (after POC approval)

**Design principle:** Keep diagrams **small and simple** — 3 to 6 elements max.
Cycles, hub-and-spoke, and short linear flows work best. Avoid large concept maps
with many nodes — they lose legibility at PDF/EPUB scale.

Candidate Excalidraw diagrams (revised for simplicity):

| Chapter | Diagram | Style | Elements |
|:--------|:--------|:------|:---------|
| 08 | Prompt anatomy | Hub-and-spoke | 4 boxes: System → User → Assistant → Output |
| 09 | Agent loop | Cycle (3 nodes) | திட்டமிடு → செயல்படு → கவனி (POC done ✓) |
| 10 | Safety layers | Concentric rings | 3 rings: Model → Application → Human |
| 02 | ML training cycle | Cycle (4 nodes) | Data → Train → Evaluate → Improve |
| 06 | LLM pipeline | Linear flow (3 steps) | Pre-train → Fine-tune → Deploy |

Dropped from original list:
- ~~01 AI big-picture concept map~~ — too many elements, legibility issues at scale
- ~~05 Transformer attention~~ — too complex for sketch style, better as Mermaid
- ~~07 Vector space intuition~~ — abstract dot plots don't suit hand-drawn style

These are all "intuition-building" diagrams where hand-drawn > formal flowchart.

## File Convention

- Source: `book/diagrams/NN-name.excalidraw` (JSON, version-controlled)
- Output: `book/diagrams/NN-name.excalidraw.png` (PNG at 2× resolution)
- The `.excalidraw.png` suffix distinguishes from Mermaid-generated `.svg`/`.png` files
- Naming: same `NN-` chapter prefix as Mermaid files
- Reference in chapter: `![alt text](diagrams/NN-name.excalidraw.png)`
- PNG chosen over SVG because PDF/EPUB renderers cannot handle embedded fonts in SVG
- Mermaid diagrams remain SVG (their font pipeline works differently)

## Open Questions

- [x] ~~Test Kavivanar rendering in WeasyPrint (book builder) — does embedded base64 .ttf work?~~
      **Resolved:** SVG font embedding fails in WeasyPrint. Switched to PNG output (Puppeteer screenshot at 2×). Tamil renders correctly.
- [x] ~~Test Kavivanar rendering on Kindle — does the SVG @font-face survive KDP conversion?~~
      **Resolved:** SVG fonts don't work in EPUB readers either. PNG output solves this.
- [x] ~~Decide if hand-drawn boxes should use Excalidraw's default color or match the book palette~~
      **Resolved:** Use book palette (#1a4d2e, #ffebcd, #e8f5e9) with hachure fill
- [x] ~~Evaluate `@excalidraw/utils` stability for automated SVG export~~
      **Resolved:** Works via `esm.sh/@excalidraw/utils?bundle` in headless Chrome (puppeteer-core)
- [x] ~~Determine if Kavivanar Latin glyphs are close enough to Virgil to use as a single font~~
      **Resolved:** Kavivanar used as sole font for both Tamil and English. Tested against MyHands — Kavivanar is more legible in print. `--font` flag available for switching.
