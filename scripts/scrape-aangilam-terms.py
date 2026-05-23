#!/usr/bin/env python3
"""
Scrape English-Tamil computer terms from aangilam.org
and write them to docs-glossary/aangilam-computer-terms.md
"""

import re
import html
import urllib.request
import os

URL = "https://www.aangilam.org/2010/08/computer-terms-in-tamil.html"
CACHED_HTML = "/tmp/aangilam_raw.html"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "docs-glossary", "aangilam-computer-terms.md")


def fetch_html(url):
    if os.path.exists(CACHED_HTML):
        print(f"Using cached HTML from {CACHED_HTML}")
        with open(CACHED_HTML, "r", encoding="utf-8") as f:
            return f.read()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    data = resp.read().decode("utf-8")
    with open(CACHED_HTML, "w", encoding="utf-8") as f:
        f.write(data)
    return data


def extract_terms(html_content):
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html_content, re.DOTALL)
    terms = []
    for row in rows[1:]:  # skip header
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        if len(cells) >= 3:
            eng = html.unescape(re.sub(r"<[^>]+>", "", cells[1])).strip()
            tam = html.unescape(re.sub(r"<[^>]+>", "", cells[2])).strip()
            if eng and tam and eng != "English Terms":
                terms.append((eng, tam))
    return terms


def write_markdown(terms, path):
    lines = [
        "# கணினிக் கலைச்சொற்கள் (Computer Terms in Tamil)",
        "",
        "> Source: <https://www.aangilam.org/2010/08/computer-terms-in-tamil.html>",
        ">",
        f"> Total terms: {len(terms)}",
        "",
        "| # | English | தமிழ் |",
        "|---|---------|-------|",
    ]
    for i, (eng, tam) in enumerate(terms, 1):
        eng_safe = eng.replace("|", "\\|")
        tam_safe = tam.replace("|", "\\|")
        lines.append(f"| {i} | {eng_safe} | {tam_safe} |")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    print(f"Fetching {URL} ...")
    html_content = fetch_html(URL)
    print(f"Downloaded {len(html_content)} bytes")

    terms = extract_terms(html_content)
    print(f"Extracted {len(terms)} terms")

    write_markdown(terms, OUTPUT_FILE)
    print(f"Written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
