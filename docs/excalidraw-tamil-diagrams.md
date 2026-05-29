# Excalidraw Diagrams with Tamil Text

How hand-drawn Excalidraw diagrams are authored and exported for this book, why SVG failed for Tamil, and why PNG is the production format.

---

## TL;DR

- `scripts/build-excalidraw.sh` converts `.excalidraw` JSON → **PNG at 2× resolution** via headless Chrome screenshot.
- Font: **Kavivanar** (Google Fonts, OFL) — handwritten Tamil + Latin. Switchable to MyHands via `--font` flag.
- Excalidraw diagrams complement (not replace) the Mermaid SVG pipeline — used for intuition-building sketches with 3–6 elements.
- Source files are version-controlled JSON; PNGs are generated artifacts.

## Why Excalidraw (alongside Mermaid)

| Aspect | Mermaid | Excalidraw |
|:-------|:--------|:-----------|
| **Style** | Formal flowcharts, pipelines | Hand-drawn sketches, concept maps |
| **Output** | SVG (text-as-paths via pdf2svg) | PNG (Puppeteer screenshot at 2×) |
| **Tamil font** | Noto Sans Tamil (via mermaid-config) | Kavivanar (handwritten, injected at export) |
| **Best for** | Technical process flows, hierarchies | Cycles, hub-and-spoke, intuition diagrams |
| **Authoring** | `.mmd` text files | `.excalidraw` JSON (Claude-generated or excalidraw.com) |

Readers intuitively distinguish "sketch = overview/intuition" from "flowchart = technical detail".

## The Problem: SVG Font Rendering

### What we tried

1. **SVG with remote font URL** — `@font-face` referencing `fonts.gstatic.com`
   - Chrome renders correctly, but WeasyPrint and EPUB readers cannot fetch remote fonts
   - Tamil text appeared as garbled characters in PDF/EPUB

2. **SVG with base64-embedded font** — `@font-face` with `data:font/ttf;base64,...`
   - Tested with both Kavivanar and MyHands fonts
   - Chrome renders correctly, but WeasyPrint's Cairo renderer still doesn't apply complex-script shaping for Tamil
   - Same garbled output — identical root cause as the original Mermaid SVG problem

3. **SVG text-as-paths** (the Mermaid fix) — not applicable
   - Mermaid uses `mmdc → PDF → pdf2svg` to convert text to vector paths
   - Excalidraw's `exportToSvg()` outputs `<text>` elements, not paths
   - No equivalent PDF intermediate step exists for Excalidraw

### Root cause

WeasyPrint's Cairo text renderer cannot shape Tamil Unicode correctly in SVG `<text>` elements, regardless of font embedding method. This is the same fundamental issue documented in [`svg-tamil-diagrams.md`](svg-tamil-diagrams.md) for Mermaid, but Excalidraw has no PDF intermediate workaround.

## The Fix: PNG via Puppeteer Screenshot

Since Chrome's text renderer handles Tamil correctly, we render the diagram in headless Chrome and take a screenshot:

```
.excalidraw (JSON)
  └─ excalidraw-to-svg.mjs
     ├─ Load @excalidraw/utils from esm.sh CDN
     ├─ exportToSvg() with Kavivanar @font-face (base64)
     ├─ Append SVG to page DOM
     └─ Puppeteer page.screenshot() at 2× deviceScaleFactor
        └─ .excalidraw.png (production output, 2× resolution)
```

**Why 2× resolution?** The output PNG is used in print PDF. At 1× (820×590 for a typical diagram), text would be fuzzy. At 2× (1640×1180), it's sharp at 300 DPI equivalent.

**Background:** White (`#ffffff`) for PNG output. Kindle dark mode inverts white-background images automatically.

## Font Choice: Kavivanar

We evaluated two handwritten Tamil Unicode fonts:

| Font | Style | License | Legibility | Decision |
|:-----|:------|:--------|:-----------|:---------|
| **Kavivanar** | Calligraphic handwriting | OFL (Google Fonts) | Better at small sizes | **Default** ✓ |
| **MyHands** | Mouse-drawn, rustic | CC0 Public Domain | More casual, less crisp | Available via `--font` |

Both fonts are stored locally in `scripts/fonts/` — no network dependency at build time.

Kavivanar was chosen for production because:
- Better legibility in print PDF at the sizes diagrams typically render
- Cleaner Tamil conjuncts and vowel signs
- Still has a handwritten feel that matches Excalidraw's sketch aesthetic

## Build Pipeline

### Scripts

| Script | Purpose |
|:-------|:--------|
| `scripts/build-excalidraw.sh` | Shell wrapper — finds `.excalidraw` files, installs deps, runs converter |
| `scripts/excalidraw-to-svg.mjs` | Node.js converter — headless Chrome + Puppeteer + @excalidraw/utils |

### Usage

```bash
# Build all Excalidraw diagrams
./scripts/build-excalidraw.sh

# Build only chapter 09 diagrams
./scripts/build-excalidraw.sh 09

# Direct invocation with font choice
node scripts/excalidraw-to-svg.mjs --font kavivanar input.excalidraw output.png
node scripts/excalidraw-to-svg.mjs --font myhands   input.excalidraw output.png

# SVG output (for browser preview, not for PDF/EPUB)
node scripts/excalidraw-to-svg.mjs input.excalidraw output.svg
```

### Dependencies

| Dependency | Install | Purpose |
|:-----------|:--------|:--------|
| `puppeteer-core` | `npm install --prefix scripts puppeteer-core` | Headless Chrome control |
| Google Chrome | Pre-installed on macOS/Linux | Renders SVG with correct Tamil shaping |

No Chromium download needed — `puppeteer-core` uses the system Chrome.

### One-time setup

```bash
npm install --prefix scripts puppeteer-core
```

## Authoring Excalidraw Diagrams

### JSON conventions

Diagrams are authored as `.excalidraw` JSON files (Claude-generated or via excalidraw.com):

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "tamil-glossary-poc",
  "elements": [
    {
      "type": "rectangle",
      "fillStyle": "hachure",
      "roughness": 1,
      "strokeColor": "#1a4d2e",
      "backgroundColor": "#e8f5e9",
      "fontFamily": 2,
      "roundness": { "type": 3 }
    }
  ],
  "appState": {
    "viewBackgroundColor": "transparent",
    "gridSize": null
  }
}
```

### Style guide

| Property | Value | Reason |
|:---------|:------|:-------|
| `fillStyle` | `"hachure"` | Hand-drawn fill pattern |
| `roughness` | `1` | Subtle sketch feel (2 = more dramatic) |
| `strokeColor` | `"#1a4d2e"` | Deep green, matches book palette |
| `backgroundColor` | `"#ffebcd"` / `"#e8f5e9"` / `"#e3f2fd"` | Earth tones from book palette |
| `fontFamily` | `2` | Mapped to Kavivanar at export time |
| `roundness` | `{ "type": 3 }` | Rounded rectangle corners |
| `opacity` | `100` | Fully opaque |

### Design principles

- **3–6 elements max** — diagrams must be legible at PDF/EPUB scale
- **Cycles and flows** — Plan → Act → Observe; Data → Train → Evaluate → Improve
- **Hub-and-spoke** — central concept with radiating connections
- **Short linear flows** — 3–4 steps in sequence
- **Avoid** large concept maps with 10+ nodes — they lose legibility when scaled down

## File Convention

| Item | Convention |
|:-----|:-----------|
| Source | `book/diagrams/NN-name.excalidraw` (JSON, version-controlled) |
| Output | `book/diagrams/NN-name.excalidraw.png` (generated, 2× resolution) |
| Reference | `![alt text](diagrams/NN-name.excalidraw.png)` |
| Naming | Same `NN-` chapter prefix as Mermaid files |

The `.excalidraw.png` suffix distinguishes from Mermaid-generated `.svg`/`.png` files.

## Troubleshooting

| Symptom | Cause | Fix |
|:--------|:------|:----|
| Tamil text garbled in PNG | Font file missing | Check `scripts/fonts/Kavivanar-Regular.ttf` exists |
| `Error: Font file not found` | Font not downloaded | Copy `.ttf` to `scripts/fonts/` |
| `puppeteer-core` not found | First run | `npm install --prefix scripts puppeteer-core` |
| Chrome not found | Non-standard install path | Add path to `findChrome()` in `excalidraw-to-svg.mjs` |
| PNG is blurry | Low resolution | Verify `deviceScaleFactor: 2` in screenshot options |
| Diagram too large for PDF page | Too many elements | Simplify to 3–6 elements per diagram |

## Related Documents

- [`docs/svg-tamil-diagrams.md`](svg-tamil-diagrams.md) — Mermaid SVG pipeline and Tamil rendering fix
- [`llm-context/excalidraw-poc-plan.md`](../llm-context/excalidraw-poc-plan.md) — POC plan and strategic placement
- [`scripts/build-excalidraw.sh`](../scripts/build-excalidraw.sh) — build script
- [`scripts/excalidraw-to-svg.mjs`](../scripts/excalidraw-to-svg.mjs) — converter script
