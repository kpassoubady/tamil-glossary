#!/usr/bin/env bash
# Build Mermaid diagrams (.mmd) to SVG and/or PNG for course slides.
#
# Usage:
#   bash scripts/build-diagrams.sh <diagrams-dir>                # SVG only
#   bash scripts/build-diagrams.sh <diagrams-dir> --svg            # SVG only
#   bash scripts/build-diagrams.sh <diagrams-dir> --png            # PNG only
#   bash scripts/build-diagrams.sh <diagrams-dir> --both           # SVG + PNG

set -euo pipefail

# Parse args
DIAGRAMS_DIR=""
FORMAT="svg"
for arg in "$@"; do
    case "$arg" in
        --svg)  FORMAT="svg" ;;
        --png)  FORMAT="png" ;;
        --both) FORMAT="both" ;;
        -h|--help)
            echo "Usage: bash scripts/build-diagrams.sh <diagrams-dir> [--svg|--png|--both]"
            exit 0
            ;;
        -*) echo "Unknown option: $arg" >&2; exit 1 ;;
        *) DIAGRAMS_DIR="$arg" ;;
    esac
done

if [[ -z "$DIAGRAMS_DIR" ]]; then
    echo "Usage: bash scripts/build-diagrams.sh <diagrams-dir> [--svg|--png|--both]" >&2
    exit 1
fi

if [[ ! -d "$DIAGRAMS_DIR" ]]; then
    echo "Error: directory not found: $DIAGRAMS_DIR" >&2
    exit 1
fi

DIAGRAMS_DIR="$(cd "$DIAGRAMS_DIR" && pwd)"

# Check dependency
if ! command -v mmdc &> /dev/null; then
    echo "Error: mmdc (Mermaid CLI) not found." >&2
    echo "Install it with:  npm install -g @mermaid-js/mermaid-cli" >&2
    exit 1
fi

SVG_COUNT=0
PNG_COUNT=0
FAILED=0

for mmd_file in "$DIAGRAMS_DIR"/*.mmd; do
    [ -f "$mmd_file" ] || continue
    filename=$(basename "$mmd_file" .mmd)
    outputs=""
    ok=true

    if [[ "$FORMAT" = "svg" || "$FORMAT" = "both" ]]; then
        svg_file="$DIAGRAMS_DIR/$filename.svg"
        if mmdc -i "$mmd_file" -o "$svg_file" -t neutral -b transparent 2>/dev/null; then
            outputs="$filename.svg"
        else
            echo "  ✗ $filename.mmd (SVG export failed)" >&2
            ok=false
        fi
    fi

    if [[ "$FORMAT" = "png" || "$FORMAT" = "both" ]]; then
        png_file="$DIAGRAMS_DIR/$filename.png"
        if mmdc -i "$mmd_file" -o "$png_file" -t neutral -b transparent --scale 3 2>/dev/null; then
            if [[ -n "$outputs" ]]; then
                outputs="$outputs + $filename.png"
            else
                outputs="$filename.png"
            fi
        else
            echo "  ✗ $filename.mmd (PNG export failed)" >&2
            ok=false
        fi
    fi

    if $ok && [[ -n "$outputs" ]]; then
        echo "  ✓ $filename.mmd → $outputs"
        if [[ "$FORMAT" = "svg" ]] || [[ "$FORMAT" = "both" ]]; then
            SVG_COUNT=$((SVG_COUNT + 1))
        fi
        if [[ "$FORMAT" = "png" ]] || [[ "$FORMAT" = "both" ]]; then
            PNG_COUNT=$((PNG_COUNT + 1))
        fi
    elif ! $ok; then
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "Done. SVG: $SVG_COUNT, PNG: $PNG_COUNT, Failed: $FAILED"
