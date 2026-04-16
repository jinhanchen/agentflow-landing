"""
Solarian static site builder.

Workflow:
  1. Edit source files under src/<page>/
  2. Run: python build.py
  3. Open the output HTML files (double-click, file:// works)
  4. Commit both src/ and output HTML to git

Current pages built:
  news.html     ← src/news/{template.html, index.json, articles/*.html}
  trends.html   ← src/trends/{template.html, index.json, articles/*.html}

To add a new article:
  a. Create src/<page>/articles/<id>.html (content only, no wrapper)
  b. Add an entry to src/<page>/index.json
  c. Run: python build.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def build_news() -> None:
    src = ROOT / "src" / "news"
    template = (src / "template.html").read_text(encoding="utf-8")
    index = json.loads((src / "index.json").read_text(encoding="utf-8"))
    articles_dir = src / "articles"

    # ---------- Generate list rows ----------
    row_parts = []
    for art in index["articles"]:
        cover = art.get("cover", "")
        cover_bg = art.get("coverBg", "")
        if cover:
            bg_style = f" style=\"background:{cover_bg}\"" if cover_bg else ""
            cover_html = (
                f'        <div class="news-cover"{bg_style}>\n'
                f'          <img src="{cover}" alt="" loading="lazy">\n'
                f'        </div>\n'
            )
        else:
            cover_html = '        <div class="news-cover news-cover-placeholder"></div>\n'

        row_parts.append(
            f'<div class="news-row" onclick="openArticle(\'{art["id"]}\')">\n'
            f'{cover_html}'
            f'        <div class="news-date">{art["date"]}</div>\n'
            f'        <div class="news-tag {art["tagClass"]}">{art["tag"]}</div>\n'
            f'        <div class="news-title-cell">\n'
            f'          <div class="news-title">{art["title"]}</div>\n'
            f'          <div class="news-summary">{art["summary"]}</div>\n'
            f'        </div>\n'
            f'        <div class="news-arrow">→</div>\n'
            f'      </div>'
        )
    # Join with blank line + row-level indent (6 spaces) to match original layout
    rows_html = "\n\n      ".join(row_parts)

    # ---------- Generate article blocks ----------
    output = template.replace("{{NEWS_ROWS}}", rows_html)

    article_placeholder_re = re.compile(r"\{\{ARTICLE:([\w-]+)\}\}")

    def replace_article(m: re.Match) -> str:
        aid = m.group(1)
        meta = next((a for a in index["articles"] if a["id"] == aid), None)
        if meta is None:
            raise ValueError(
                f"Template references article '{aid}' but it's missing from index.json"
            )
        inner = (articles_dir / f"{aid}.html").read_text(encoding="utf-8").rstrip("\n")
        author = meta.get("author", "")
        # articleTag is the data-tag attribute on <article> (for JS hooks);
        # if not specified, fall back to the row tag label.
        article_tag = meta.get("articleTag", meta["tag"])
        return (
            f'<article class="story" id="article-{aid}" style="display:none"\n'
            f'               data-tag="{article_tag}" data-date="{meta["date"]}" data-author="{author}">\n'
            f'{inner}\n'
            f'      </article>'
        )

    output = article_placeholder_re.sub(replace_article, output)

    # ---------- Write (force LF line endings for clean git diffs) ----------
    out_path = ROOT / "news.html"
    # Normalize any CRLF from sources down to LF so the output is consistent
    output = output.replace("\r\n", "\n")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(output)
    print(f"[OK] Built {out_path.name} | {len(index['articles'])} articles | {len(output):,} chars")


def _js_single_quoted(s: str) -> str:
    """Encode a string as a JS single-quoted string literal."""
    escaped = (
        s.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f"'{escaped}'"


def _js_template_literal(s: str) -> str:
    """Encode a string as a JS template-literal (backtick) string."""
    escaped = s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    return f"`{escaped}`"


def build_trends() -> None:
    src = ROOT / "src" / "trends"
    template = (src / "template.html").read_text(encoding="utf-8")
    index = json.loads((src / "index.json").read_text(encoding="utf-8"))
    articles_dir = src / "articles"

    parts = []
    for art in index["articles"]:
        content = (articles_dir / f"{art['id']}.html").read_text(encoding="utf-8").rstrip("\n")
        grad_line = ", grad: null" if art.get("gradNull") else ""
        parts.append(
            f"  {{\n"
            f"    id: {art['num']},\n"
            f"    title: {_js_single_quoted(art['title'])},\n"
            f"    tag: {_js_single_quoted(art['tag'])}, tagClass: {_js_single_quoted(art['tagClass'])},\n"
            f"    desc: {_js_single_quoted(art['desc'])},\n"
            f"    source: {_js_single_quoted(art['source'])}, date: {_js_single_quoted(art['date'])}, readTime: {_js_single_quoted(art['readTime'])},\n"
            f"    cover: {_js_single_quoted(art['cover'])}{grad_line},\n"
            f"    content: {_js_template_literal(content)}\n"
            f"  }}"
        )

    js_array = "[\n" + ",\n".join(parts) + "\n]"
    output = template.replace("{{ARTICLES_JS}}", js_array)
    output = output.replace("\r\n", "\n")

    out_path = ROOT / "trends.html"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(output)
    print(f"[OK] Built {out_path.name} | {len(index['articles'])} articles | {len(output):,} chars")


def main() -> int:
    try:
        build_news()
        build_trends()
    except Exception as e:
        print(f"[FAIL] Build failed: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
