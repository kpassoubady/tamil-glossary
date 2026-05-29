#!/usr/bin/env node
// Convert .excalidraw JSON files to SVG or PNG using a headless browser.
//
// Usage:
//   node scripts/excalidraw-to-svg.mjs [--font myhands|kavivanar] <input.excalidraw> <output.svg|png>
//
// Options:
//   --font    Font family to use (default: myhands)
//              myhands    — MyHands (handwritten Tamil, mouse-drawn, CC0)
//              kavivanar  — Kavivanar (Google Fonts, OFL)
//
// Output format is detected from the file extension:
//   .svg  — raw SVG with embedded font (for browser use)
//   .png  — rasterised via Puppeteer screenshot at 2× (for PDF/EPUB)
//
// Dependencies (one-time): npm install --prefix scripts puppeteer-core
// Requires Google Chrome installed on the system.

import { existsSync } from 'node:fs';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';
import { dirname, resolve, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// --- Argument parsing ---
let fontName = 'kavivanar';
let inputFile, outputFile;
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--font' && i + 1 < args.length) {
    fontName = args[i + 1].toLowerCase();
    i++;
  } else if (!inputFile) {
    inputFile = args[i];
  } else if (!outputFile) {
    outputFile = args[i];
  }
}
if (!inputFile || !outputFile) {
  console.error('Usage: node excalidraw-to-svg.mjs [--font myhands|kavivanar] <input.excalidraw> <output.svg|png>');
  process.exit(1);
}
if (fontName !== 'myhands' && fontName !== 'kavivanar') {
  console.error('Error: --font must be myhands or kavivanar');
  process.exit(1);
}
const outputFormat = outputFile.endsWith('.png') ? 'png' : 'svg';

// --- Find Chrome ---
function findChrome() {
  const candidates = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
  ];
  for (const c of candidates) {
    if (existsSync(c)) return c;
  }
  return null;
}

// --- Font registry ---
const FONTS = {
  myhands: {
    name: 'MyHands',
    path: join(__dirname, 'fonts', 'MyHands_2025-Regular.ttf'),
  },
  kavivanar: {
    name: 'Kavivanar',
    path: join(__dirname, 'fonts', 'Kavivanar-Regular.ttf'),
  },
};
const FONT = FONTS[fontName];

// Read local font and return base64-encoded data URI
async function getFontBase64() {
  if (!existsSync(FONT.path)) {
    throw new Error(`Font file not found: ${FONT.path}\nDownload ${FONT.name}.ttf to scripts/fonts/`);
  }
  const buf = await readFile(FONT.path);
  return `data:font/ttf;base64,${buf.toString('base64')}`;
}

// --- HTML page that loads Excalidraw and exports SVG ---
function buildHtml(excalidrawJson, fontDataUri, asPng) {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    @font-face {
      font-family: '${FONT.name}';
      src: url('${fontDataUri}') format('truetype');
      font-display: block;
    }
    /* Map Excalidraw fontFamily 2 (Helvetica) to selected font */
    * { font-family: '${FONT.name}', 'Noto Sans Tamil', sans-serif !important; }
    body { margin: 0; padding: 0; }
  </style>
</head>
<body>
<script type="module">
  try {
    const { exportToSvg } = await import('https://esm.sh/@excalidraw/utils?bundle');
    const data = ${excalidrawJson};
    const exportBackground = ${asPng ? 'true' : 'false'};
    const svg = await exportToSvg({
      elements: data.elements,
      appState: {
        ...data.appState,
        exportWithDarkMode: false,
        exportBackground: exportBackground,
        viewBackgroundColor: exportBackground ? '#ffffff' : 'transparent',
      },
      files: data.files || {},
    });
    // Inject selected font @font-face with base64 data into SVG for portability
    const ns = 'http://www.w3.org/2000/svg';
    let defs = svg.querySelector('defs');
    if (!defs) {
      defs = document.createElementNS(ns, 'defs');
      svg.insertBefore(defs, svg.firstChild);
    }
    const style = document.createElementNS(ns, 'style');
    style.textContent = \`
      @font-face {
        font-family: '${FONT.name}';
        src: url('${fontDataUri}') format('truetype');
      }
      text { font-family: '${FONT.name}', 'Noto Sans Tamil', sans-serif; }
    \`;
    defs.appendChild(style);

    if (${asPng}) {
      // For PNG: render SVG in the page so Puppeteer can screenshot it
      const w = parseInt(svg.getAttribute('width')) || 800;
      const h = parseInt(svg.getAttribute('height')) || 600;
      document.body.innerHTML = '';
      document.body.appendChild(svg);
      svg.style.display = 'block';
      window.__svgDimensions = { width: w, height: h };
    } else {
      window.__svgResult = new XMLSerializer().serializeToString(svg);
    }
  } catch (err) {
    window.__svgError = err.message || String(err);
  }
</script>
</body>
</html>`;
}

// --- Main ---
async function main() {
  const puppeteer = await import('puppeteer-core');
  const json = await readFile(inputFile, 'utf-8');

  // Validate JSON
  JSON.parse(json);

  // Read and base64-encode selected font
  const fontDataUri = await getFontBase64();
  console.error(`  Font: ${FONT.name} embedded as base64`);

  const asPng = outputFormat === 'png';

  // Start a local HTTP server (needed for ES module imports in the page)
  const html = buildHtml(json, fontDataUri, asPng);
  const server = createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(html);
  });

  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const port = server.address().port;

  const chromePath = findChrome() ||
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

  const browser = await puppeteer.default.launch({
    headless: 'new',
    executablePath: chromePath,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  try {
    const page = await browser.newPage();

    // Navigate and wait for the export to complete
    await page.goto(`http://127.0.0.1:${port}`, { waitUntil: 'networkidle0', timeout: 60000 });

    if (asPng) {
      // PNG mode: wait for SVG to render in page, then screenshot
      await page.waitForFunction(
        'window.__svgDimensions || window.__svgError',
        { timeout: 60000 }
      );
      const error = await page.evaluate(() => window.__svgError);
      if (error) throw new Error(`Excalidraw export failed: ${error}`);

      const dims = await page.evaluate(() => window.__svgDimensions);
      // 2× scale for sharp rendering in print
      const scale = 2;
      await page.setViewport({
        width: dims.width,
        height: dims.height,
        deviceScaleFactor: scale,
      });
      // Brief pause for font rendering
      await new Promise((r) => setTimeout(r, 500));
      await page.screenshot({
        path: outputFile,
        type: 'png',
        clip: { x: 0, y: 0, width: dims.width, height: dims.height },
        omitBackground: false,
      });
    } else {
      // SVG mode: extract serialized SVG string
      await page.waitForFunction(
        'window.__svgResult || window.__svgError',
        { timeout: 60000 }
      );
      const error = await page.evaluate(() => window.__svgError);
      if (error) throw new Error(`Excalidraw export failed: ${error}`);

      const svgString = await page.evaluate(() => window.__svgResult);
      await writeFile(outputFile, svgString, 'utf-8');
    }
  } finally {
    await browser.close();
    server.close();
  }
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
