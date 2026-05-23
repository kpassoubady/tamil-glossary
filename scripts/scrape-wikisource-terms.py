#!/usr/bin/env python3
"""
Scrape English-Tamil computing terms from Tamil Wikisource:
கணினி களஞ்சியப் பேரகராதி-1. (A to Z)

Output: docs-glossary/wikisource-computer-glossary.md
"""

import re
import html
import urllib.request
import os
import time
import string

BASE_URL = (
    "https://ta.wikisource.org/wiki/"
    "%E0%AE%95%E0%AE%A3%E0%AE%BF%E0%AE%A9%E0%AE%BF_"
    "%E0%AE%95%E0%AE%B3%E0%AE%9E%E0%AF%8D%E0%AE%9A%E0%AE%BF"
    "%E0%AE%AF%E0%AE%AA%E0%AF%8D_%E0%AE%AA%E0%AF%87%E0%AE%B0"
    "%E0%AE%95%E0%AE%B0%E0%AE%BE%E0%AE%A4%E0%AE%BF-1./"
)
CACHE_DIR = "/tmp/wikisource_cache"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_FILE = os.path.join(
    PROJECT_ROOT, "docs-glossary", "wikisource-computer-glossary.md"
)


def fetch_page(letter):
    """Download a page or use cached version."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"{letter}.html")

    if os.path.exists(cache_file):
        print(f"  [{letter}] Using cached file")
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()

    url = BASE_URL + letter
    print(f"  [{letter}] Fetching {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        resp = urllib.request.urlopen(req)
        data = resp.read().decode("utf-8")
    except Exception as e:
        print(f"  [{letter}] ERROR: {e}")
        return None

    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(data)
    time.sleep(1)  # be polite to the server
    return data


def extract_terms_from_page(html_content):
    """
    Extract (english, tamil) pairs from a page.
    Pattern in <b> tags: english_term : tamil_term :
    """
    terms = []
    # Find all <p> tags in the content area
    idx = html_content.find("mw-parser-output")
    if idx < 0:
        return terms
    content = html_content[idx:]

    # Each entry is in a <p> tag with <b>english : tamil : </b>
    p_tags = re.findall(r"<p>(.*?)</p>", content, re.DOTALL)
    for p in p_tags:
        # Look for the bold pattern: <b>term : tamil_term : </b>
        bold_match = re.search(r"<b>(.*?)</b>", p, re.DOTALL)
        if not bold_match:
            continue
        bold_text = bold_match.group(1)
        # Clean HTML inside bold
        bold_text = re.sub(r"<[^>]+>", "", bold_text)
        bold_text = html.unescape(bold_text).strip()

        # Split by " : " — format is "english : tamil :"
        # Use \u00a0 (non-breaking space) aware split
        bold_text = bold_text.replace("\u00a0", " ")
        parts = [p.strip() for p in bold_text.split(" : ") if p.strip()]

        if len(parts) >= 2:
            eng = parts[0].strip().rstrip(":")
            tam = parts[1].strip().rstrip(":")
            if eng and tam:
                terms.append((eng, tam))

    return terms


def write_markdown(all_terms, path):
    lines = [
        "# கணினி களஞ்சியப் பேரகராதி (Computer Encyclopedia Dictionary)",
        "",
        "> Source: [Tamil Wikisource - கணினி களஞ்சியப் பேரகராதி-1.]"
        "(https://ta.wikisource.org/wiki/"
        "%E0%AE%95%E0%AE%A3%E0%AE%BF%E0%AE%A9%E0%AE%BF_"
        "%E0%AE%95%E0%AE%B3%E0%AE%9E%E0%AF%8D%E0%AE%9A%E0%AE%BF"
        "%E0%AE%AF%E0%AE%AA%E0%AF%8D_%E0%AE%AA%E0%AF%87%E0%AE%B0"
        "%E0%AE%95%E0%AE%B0%E0%AE%BE%E0%AE%A4%E0%AE%BF-1.)",
        "> Author: மணவை முஸ்தபா",
        ">",
        f"> Total terms: {sum(len(t) for t in all_terms.values())}",
        "",
    ]

    num = 0
    for letter in string.ascii_uppercase:
        terms = all_terms.get(letter, [])
        if not terms:
            continue
        lines.append(f"## {letter}")
        lines.append("")
        lines.append("| # | English | தமிழ் |")
        lines.append("|---|---------|-------|")
        for eng, tam in terms:
            num += 1
            eng_safe = eng.replace("|", "\\|")
            tam_safe = tam.replace("|", "\\|")
            lines.append(f"| {num} | {eng_safe} | {tam_safe} |")
        lines.append("")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    print("Scraping கணினி களஞ்சியப் பேரகராதி-1. (A-Z)...")
    all_terms = {}
    total = 0

    for letter in string.ascii_uppercase:
        html_content = fetch_page(letter)
        if html_content is None:
            print(f"  [{letter}] Skipped (download failed)")
            continue
        terms = extract_terms_from_page(html_content)
        all_terms[letter] = terms
        total += len(terms)
        print(f"  [{letter}] Extracted {len(terms)} terms")

    print(f"\nTotal: {total} terms across {len(all_terms)} letters")
    write_markdown(all_terms, OUTPUT_FILE)
    print(f"Written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
