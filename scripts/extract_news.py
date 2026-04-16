"""
One-shot: split current news.html into src/news/ structure.

Outputs:
  src/news/template.html       - news.html shell with {{NEWS_ROWS}} and {{NEWS_ARTICLES}} placeholders
  src/news/articles/*.html     - each article's inner content (no <article> wrapper)
  src/news/index.json          - article metadata for list rendering

Run once after making news.html "the source of truth" for current state.
"""

import re
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
NEWS_HTML = ROOT / "news.html"
SRC = ROOT / "src" / "news"
ARTICLES = SRC / "articles"

ARTICLES.mkdir(parents=True, exist_ok=True)

html = NEWS_HTML.read_text(encoding="utf-8")

# ---------- Extract article blocks ----------
# Match: <article class="story" id="article-XXX" ...attrs...>INNER</article>
article_re = re.compile(
    r'(?P<indent>[ \t]*)<article class="story" id="article-(?P<id>[\w-]+)"(?P<attrs>[^>]*)>'
    r'(?P<inner>.*?)'
    r'(?P=indent)</article>',
    re.DOTALL,
)

attr_re = re.compile(r'(data-\w[\w-]*)\s*=\s*"([^"]*)"')

articles_meta = {}

def save_article(match):
    aid = match.group("id")
    attrs = dict(attr_re.findall(match.group("attrs")))
    inner = match.group("inner").strip("\n")
    # Save to file
    (ARTICLES / f"{aid}.html").write_text(inner + "\n", encoding="utf-8")
    articles_meta[aid] = {
        "tag": attrs.get("data-tag", ""),
        "date": attrs.get("data-date", ""),
        "author": attrs.get("data-author", ""),
    }
    # Replace with placeholder (single, on its own line, keep indent)
    return f'{match.group("indent")}{{{{ARTICLE:{aid}}}}}'

html_after_articles = article_re.sub(save_article, html)
print(f"Extracted {len(articles_meta)} articles: {list(articles_meta)}")

# ---------- Extract row blocks to harvest metadata ----------
# Each row has: onclick id, date, tag class, tag label, title, summary
row_re = re.compile(
    r'<div class="news-row" onclick="openArticle\(\'(?P<id>[\w-]+)\'\)">\s*'
    r'<div class="news-date">(?P<date>[^<]+)</div>\s*'
    r'<div class="news-tag (?P<tagClass>[\w-]+)">(?P<tag>[^<]+)</div>\s*'
    r'<div class="news-title-cell">\s*'
    r'<div class="news-title">(?P<title>[^<]+)</div>\s*'
    r'<div class="news-summary">(?P<summary>[^<]+)</div>\s*'
    r'</div>\s*'
    r'<div class="news-arrow">[^<]+</div>\s*'
    r'</div>',
    re.DOTALL,
)

rows_ordered = []
for m in row_re.finditer(html):
    rid = m.group("id")
    rows_ordered.append({
        "id": rid,
        "date": m.group("date"),
        "tag": m.group("tag"),
        "tagClass": m.group("tagClass"),
        "title": m.group("title"),
        "summary": m.group("summary"),
    })

print(f"Extracted {len(rows_ordered)} rows: {[r['id'] for r in rows_ordered]}")

# ---------- Replace rows block with placeholder ----------
# Find the first row start and last row end, replace entire block
first_start = html_after_articles.find('<div class="news-row"')
if first_start == -1:
    raise RuntimeError("No news-row found in news.html")

# Find end: the last </div> that closes the last news-row
# Simpler: find last '<div class="news-row"' and then find its matching </div>
# We'll parse depth from there
last_row_start = html_after_articles.rfind('<div class="news-row"')
# Walk from there to find the closing </div> of this row
i = last_row_start
depth = 0
last_end = None
while i < len(html_after_articles):
    if html_after_articles.startswith("<div", i) and html_after_articles[i + 4] in " >":
        depth += 1
        # advance past >
        close_gt = html_after_articles.find(">", i) + 1
        i = close_gt
    elif html_after_articles.startswith("</div>", i):
        depth -= 1
        i += len("</div>")
        if depth == 0:
            last_end = i
            break
    else:
        i += 1

if last_end is None:
    raise RuntimeError("Could not find closing </div> of last news-row")

# Determine indent of first row (copy leading whitespace on that line)
line_start = html_after_articles.rfind("\n", 0, first_start) + 1
row_indent = html_after_articles[line_start:first_start]

# Rebuild: before + placeholder + after
template_html = (
    html_after_articles[:line_start]
    + f"{row_indent}{{{{NEWS_ROWS}}}}\n"
    + html_after_articles[last_end:].lstrip(" \t")
    # preserve the newline that follows
)

# Actually: preserve newline after last_end - let's not strip
template_html = (
    html_after_articles[:line_start]
    + f"{row_indent}{{{{NEWS_ROWS}}}}"
    + html_after_articles[last_end:]
)

# ---------- Write outputs ----------
(SRC / "template.html").write_text(template_html, encoding="utf-8")
print(f"Wrote template: {SRC / 'template.html'} ({len(template_html)} chars)")

# Merge article author into row metadata for index.json
for row in rows_ordered:
    aid = row["id"]
    if aid in articles_meta:
        row["author"] = articles_meta[aid]["author"]

index_json = {"articles": rows_ordered}
(SRC / "index.json").write_text(
    json.dumps(index_json, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"Wrote index: {SRC / 'index.json'} ({len(rows_ordered)} articles)")

print("\nDone. Run `python build.py` to regenerate news.html from src/.")
