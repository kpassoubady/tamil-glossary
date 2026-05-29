#!/bin/bash
# Render .excalidraw JSON files to PNG for the Tamil AI Glossary book.
#
# Uses a headless Chrome browser (via puppeteer-core) to load the Excalidraw
# library and export each diagram as PNG at 2× resolution with MyHands Tamil font.
# PNG avoids font-embedding issues in PDF/EPUB renderers.
#
# Usage: ./scripts/build-excalidraw.sh [chapter-prefix|all]
#
# Examples:
#   ./scripts/build-excalidraw.sh           # all .excalidraw files
#   ./scripts/build-excalidraw.sh 01        # only 01-*.excalidraw files
#
# One-time setup:
#   npm install --prefix scripts puppeteer-core

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIAGRAM_DIR="$REPO_ROOT/book/diagrams"
SCRIPT_DIR="$REPO_ROOT/scripts"
CONVERTER="$SCRIPT_DIR/excalidraw-to-svg.mjs"

# Check dependencies
if [ ! -d "$SCRIPT_DIR/node_modules/puppeteer-core" ]; then
  echo "puppeteer-core not found. Installing (one-time)..."
  npm install --prefix "$SCRIPT_DIR" puppeteer-core
fi

if [ ! -f "$CONVERTER" ]; then
  echo "Error: converter script not found at $CONVERTER"
  exit 1
fi

# Parse arguments
target="${1:-all}"

if [ "$target" = "all" ]; then
  pattern="*.excalidraw"
else
  pattern="${target}-*.excalidraw"
fi

# Find matching files (exclude generated outputs)
excalidraw_files=()
while IFS= read -r f; do
  excalidraw_files+=("$f")
done < <(find "$DIAGRAM_DIR" -maxdepth 1 -name "$pattern" ! -name "*.excalidraw.svg" ! -name "*.excalidraw.png" | sort)

if [ ${#excalidraw_files[@]} -eq 0 ]; then
  echo "No .excalidraw files matching '$pattern' in $DIAGRAM_DIR"
  exit 0
fi

echo "Building ${#excalidraw_files[@]} Excalidraw diagram(s) matching '$pattern'..."

for excalidraw_file in "${excalidraw_files[@]}"; do
  filename=$(basename "$excalidraw_file")
  png_file="$DIAGRAM_DIR/${filename}.png"

  node "$CONVERTER" "$excalidraw_file" "$png_file"
  echo "  $filename → ${filename}.png"
done

echo "Done. ${#excalidraw_files[@]} Excalidraw diagram(s) built."
