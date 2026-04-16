"""
One-shot: split current trends.html into src/trends/ structure.

Outputs:
  src/trends/template.html    - trends.html shell with {{ARTICLES_JS}} placeholder
  src/trends/articles/*.html  - each article's body HTML (the template-literal content)
  src/trends/index.json       - article metadata (everything except content)
"""

import re
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRENDS_HTML = ROOT / "trends.html"
SRC = ROOT / "src" / "trends"
ARTICLES_DIR = SRC / "articles"
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

html = TRENDS_HTML.read_text(encoding="utf-8")

# ---------- Locate the articles array ----------
m = re.search(r"const articles = \[(.*?)\];", html, re.DOTALL)
if not m:
    raise RuntimeError("`const articles = [...]` not found in trends.html")

articles_body = m.group(1)
articles_block = m.group(0)


# ---------- Split into top-level object literals ----------
def split_top_level_objects(s: str) -> list[str]:
    out, depth, start = [], 0, None
    in_string: str | None = None
    escape = False
    for i, ch in enumerate(s):
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if in_string:
            if ch == in_string:
                in_string = None
            continue
        if ch in ("'", '"', "`"):
            in_string = ch
            continue
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                out.append(s[start : i + 1])
                start = None
    return out


objects = split_top_level_objects(articles_body)
print(f"Found {len(objects)} article objects")


# ---------- Field extraction helpers ----------
def field_str(obj: str, name: str) -> str | None:
    m = re.search(rf"\b{name}:\s*'((?:\\.|[^'\\])*)'", obj, re.DOTALL)
    return m.group(1).replace("\\'", "'").replace("\\\\", "\\") if m else None


def field_num(obj: str, name: str) -> int | None:
    m = re.search(rf"\b{name}:\s*(\d+)", obj)
    return int(m.group(1)) if m else None


def field_template(obj: str, name: str) -> str | None:
    m = re.search(rf"\b{name}:\s*`((?:\\.|[^`\\])*)`", obj, re.DOTALL)
    if not m:
        return None
    s = m.group(1)
    # Reverse JS template-literal escapes
    return s.replace("\\`", "`").replace("\\${", "${").replace("\\\\", "\\")


def field_optional_null(obj: str, name: str) -> bool:
    """Check if `name: null` is present (e.g., grad: null)."""
    return bool(re.search(rf"\b{name}:\s*null", obj))


# ---------- Extract each article ----------
index_articles = []

for obj in objects:
    num = field_num(obj, "id")
    title = field_str(obj, "title")
    tag = field_str(obj, "tag")
    tag_class = field_str(obj, "tagClass")
    desc = field_str(obj, "desc")
    source = field_str(obj, "source")
    date = field_str(obj, "date")
    read_time = field_str(obj, "readTime")
    cover = field_str(obj, "cover")
    grad_null = field_optional_null(obj, "grad")
    content = field_template(obj, "content")

    if content is None:
        raise RuntimeError(f"Failed to extract `content` from article id={num}")

    file_id = f"{num:03d}"
    (ARTICLES_DIR / f"{file_id}.html").write_text(content.strip() + "\n", encoding="utf-8")

    entry = {
        "id": file_id,
        "num": num,
        "title": title,
        "tag": tag,
        "tagClass": tag_class,
        "desc": desc,
        "source": source,
        "date": date,
        "readTime": read_time,
        "cover": cover,
    }
    if grad_null:
        entry["gradNull"] = True
    index_articles.append(entry)

    print(f"  [{file_id}] {title}")

# ---------- Write index.json ----------
(SRC / "index.json").write_text(
    json.dumps({"articles": index_articles}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"Wrote {SRC / 'index.json'}")

# ---------- Build template.html ----------
template = html.replace(articles_block, "const articles = {{ARTICLES_JS}};")
(SRC / "template.html").write_text(template, encoding="utf-8")
print(f"Wrote {SRC / 'template.html'}")

print("\nDone. Update build.py to also rebuild trends.html.")
