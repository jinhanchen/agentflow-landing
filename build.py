"""
Solarian static site builder.

Workflow:
  1. Edit source files under src/<page>/
  2. Run: python build.py
  3. Open the output HTML files (double-click, file:// works)
  4. Commit both src/ and output HTML to git

Pages built:
  news.html         ← src/news/{template.html, index.json}
  news/<id>.html    ← src/news/{article-page.html, articles/<id>.html}
  trends.html       ← src/trends/{template.html, index.json}
  trends/<id>.html  ← src/trends/{article-page.html, articles/<id>.html}

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

    # ---------- Generate list rows (now <a> links) ----------
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
            f'<a href="/news/{art["id"]}" class="news-row">\n'
            f'{cover_html}'
            f'        <div class="news-date">{art["date"]}</div>\n'
            f'        <div class="news-tag {art["tagClass"]}">{art["tag"]}</div>\n'
            f'        <div class="news-title-cell">\n'
            f'          <div class="news-title">{art["title"]}</div>\n'
            f'          <div class="news-summary">{art["summary"]}</div>\n'
            f'        </div>\n'
            f'        <div class="news-arrow">→</div>\n'
            f'      </a>'
        )
    rows_html = "\n\n      ".join(row_parts)
    output = template.replace("{{NEWS_ROWS}}", rows_html)
    output = output.replace("\r\n", "\n")

    out_path = ROOT / "news.html"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(output)
    print(f"[OK] Built {out_path.name} | {len(index['articles'])} articles | {len(output):,} chars")


def build_news_articles() -> None:
    src = ROOT / "src" / "news"
    template = (src / "article-page.html").read_text(encoding="utf-8")
    index = json.loads((src / "index.json").read_text(encoding="utf-8"))
    articles_dir = src / "articles"
    out_dir = ROOT / "news"
    out_dir.mkdir(exist_ok=True)

    for art in index["articles"]:
        content = (articles_dir / f"{art['id']}.html").read_text(encoding="utf-8").rstrip("\n")

        output = template
        output = output.replace("{{TITLE}}", art["title"])
        output = output.replace("{{DESC}}", art.get("summary", ""))
        output = output.replace("{{TAG_CLASS}}", art.get("tagClass", ""))
        output = output.replace("{{TAG}}", art.get("articleTag", art.get("tag", "")))
        output = output.replace("{{DATE}}", art["date"])
        output = output.replace("{{AUTHOR}}", art.get("author", ""))
        output = output.replace("{{CONTENT}}", content)
        output = output.replace("{{CANONICAL_ID}}", art["id"])
        output = output.replace("\r\n", "\n")

        out_path = out_dir / f"{art['id']}.html"
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(output)

    print(f"[OK] Built {len(index['articles'])} news article pages → news/")


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

    parts = []
    for art in index["articles"]:
        grad_line = ", grad: null" if art.get("gradNull") else ""
        parts.append(
            f"  {{\n"
            f"    id: {_js_single_quoted(art['id'])},\n"
            f"    title: {_js_single_quoted(art['title'])},\n"
            f"    tag: {_js_single_quoted(art['tag'])}, tagClass: {_js_single_quoted(art['tagClass'])},\n"
            f"    desc: {_js_single_quoted(art['desc'])},\n"
            f"    source: {_js_single_quoted(art['source'])}, date: {_js_single_quoted(art['date'])}, readTime: {_js_single_quoted(art['readTime'])},\n"
            f"    cover: {_js_single_quoted(art.get('cover', ''))}{grad_line}\n"
            f"  }}"
        )

    js_array = "[\n" + ",\n".join(parts) + "\n]"
    output = template.replace("{{ARTICLES_JS}}", js_array)
    output = output.replace("\r\n", "\n")

    out_path = ROOT / "trends.html"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(output)
    print(f"[OK] Built {out_path.name} | {len(index['articles'])} articles | {len(output):,} chars")


def build_trends_articles() -> None:
    src = ROOT / "src" / "trends"
    template = (src / "article-page.html").read_text(encoding="utf-8")
    index = json.loads((src / "index.json").read_text(encoding="utf-8"))
    articles_dir = src / "articles"
    out_dir = ROOT / "trends"
    out_dir.mkdir(exist_ok=True)

    for art in index["articles"]:
        content = (articles_dir / f"{art['id']}.html").read_text(encoding="utf-8").rstrip("\n")

        cover = art.get("cover", "")
        if cover:
            cover_html = f'<img class="article-cover" src="/{cover}" alt="">'
        else:
            grad = "grad-1" if not art.get("gradNull") else "grad-1"
            cover_html = f'<div class="article-cover-grad card-cover-placeholder {grad}"></div>'

        output = template
        output = output.replace("{{TITLE}}", art["title"])
        output = output.replace("{{DESC}}", art.get("desc", ""))
        output = output.replace("{{TAG_CLASS}}", art["tagClass"])
        output = output.replace("{{TAG}}", art["tag"])
        output = output.replace("{{SOURCE}}", art["source"])
        output = output.replace("{{DATE}}", art["date"])
        output = output.replace("{{READ_TIME}}", art["readTime"])
        output = output.replace("{{COVER_HTML}}", cover_html)
        output = output.replace("{{CONTENT}}", content)
        output = output.replace("{{CANONICAL_ID}}", art["id"])
        output = output.replace("\r\n", "\n")

        out_path = out_dir / f"{art['id']}.html"
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(output)

    print(f"[OK] Built {len(index['articles'])} trends article pages → trends/")


def main() -> int:
    try:
        build_news()
        build_news_articles()
        build_trends()
        build_trends_articles()
    except Exception as e:
        print(f"[FAIL] Build failed: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
