#!/bin/bash
# Build all Marp slide decks to PDF
# Usage: ./scripts/build-slides.sh [day1|day2|day3|all]
#        ./scripts/build-slides.sh /absolute/path/to/slides

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# The theme is imported per-deck via the `style` front-matter directive (jsDelivr),
# so no --theme flag is needed here.

build_dir() {
  local slide_dir=$1
  local pdf_dir="$slide_dir/pdf"

  if [ ! -d "$slide_dir" ]; then
    echo "No slides directory: $slide_dir — skipping"
    return
  fi

  local md_count
  md_count=$(find "$slide_dir" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')
  if [ "$md_count" -eq 0 ]; then
    echo "No .md files in $slide_dir — skipping"
    return
  fi

  mkdir -p "$pdf_dir"
  echo "Building slides → $pdf_dir/"

  for md_file in "$slide_dir"/*.md; do
    local filename
    filename=$(basename "$md_file" .md)
    echo "  $filename.md → $filename.pdf"
    marp --pdf --allow-local-files "$md_file" -o "$pdf_dir/$filename.pdf"
  done
}

build_day() {
  build_dir "$REPO_ROOT/$1/slides"
}

target="${1:-all}"

case "$target" in
  /*)
    build_dir "$target"
    ;;
  all)
    for day in day1 day2 day3; do
      build_day "$day"
    done
    ;;
  *)
    build_day "$target"
    ;;
esac

echo "Done."
