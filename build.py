#!/usr/bin/env python3
"""Build the static site for ดิกจีน.

Edit the Markdown in content/ (privacy, terms, credits) or the HTML of
index.html / support.html, then run:  python3 build.py
The document pages (privacy.html, terms.html, credits.html) are generated.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "thiravadhano@gmail.com"

NAV = [
    ("index.html", "หน้าแรก"),
    ("support.html", "ช่วยเหลือ"),
    ("privacy.html", "ความเป็นส่วนตัว"),
    ("terms.html", "เงื่อนไข"),
]


def header(current: str) -> str:
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{href}"{cur if href == current else ""}>{label}</a>'
        for href, label in NAV
    )
    return f"""<header class="site-header"><div class="wrap">
<a class="brand" href="index.html"><img src="assets/icon-512.png" alt="">ดิกจีน</a>
<nav class="nav" aria-label="เมนูหลัก">{links}</nav>
</div></header>"""


FOOTER = f"""<footer class="site-footer"><div class="wrap">
<span>© 2026 อุดม ศิริเฑียรทอง</span>
<nav aria-label="ลิงก์ท้ายเว็บ"><a href="privacy.html">นโยบายความเป็นส่วนตัว</a><a href="terms.html">เงื่อนไขการใช้งาน</a><a href="credits.html">ข้อมูลและลิขสิทธิ์</a><a href="mailto:{EMAIL}">ติดต่อ</a></nav>
</div></footer>"""


def page(title: str, current: str, body: str, description: str) -> str:
    return f"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
{header(current)}
{body}
{FOOTER}
</body>
</html>
"""


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', text)
    # bare URLs not already inside an href
    text = re.sub(r'(?<!href=")(?<!">)(https?://[^\s<)]+)', r'<a href="\1">\1</a>', text)
    text = text.replace(EMAIL, f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    return text


def markdown(md: str) -> tuple[str, str]:
    """Tiny Markdown subset: #, ##, paragraphs, - lists, ---, and the MIT text block."""
    out, title, para, items = [], "", [], []

    def flush():
        nonlocal para, items
        if para:
            out.append("<p>" + "<br>".join(inline(l) for l in para) + "</p>")
            para = []
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items = []

    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith("# "):
            flush(); title = line[2:].strip()
            out.append(f"<h1>{inline(title)}</h1>")
        elif line.startswith("## "):
            flush(); out.append(f"<h2>{inline(line[3:])}</h2>")
            if "MIT" in line:  # license text block until next heading
                block = []
                i += 1
                while i < len(lines) and not lines[i].startswith("#"):
                    block.append(lines[i]); i += 1
                note = [b for b in block if b.startswith("(")]
                text = "\n".join(b for b in block if not b.startswith("(")).strip()
                if note:
                    out.append(f'<p class="note">{inline(note[0])}</p>')
                out.append(f'<div class="license">{html.escape(text)}</div>')
                continue
        elif line.startswith("- "):
            if para: flush()
            items.append(line[2:])
        elif line.strip() == "---":
            flush(); out.append("<hr>")
        elif not line.strip():
            flush()
        elif line.startswith("มีผลตั้งแต่"):
            flush(); out.append(f'<p class="meta">{inline(line)}</p>')
        else:
            if items: flush()
            para.append(line)
        i += 1
    flush()
    return title, "\n".join(out)


DOCS = {
    "privacy": "นโยบายความเป็นส่วนตัวของแอปดิกจีน: ไม่เก็บข้อมูลส่วนตัว ไม่มีโฆษณา ไม่ติดตามผู้ใช้",
    "terms": "เงื่อนไขการใช้งานและการซื้อในแอปดิกจีน",
    "credits": "แหล่งข้อมูลและสัญญาอนุญาตที่แอปดิกจีนใช้",
}

for name, desc in DOCS.items():
    title, body = markdown((ROOT / "content" / f"{name}.md").read_text(encoding="utf-8"))
    (ROOT / f"{name}.html").write_text(
        page(f"{title} | ดิกจีน", f"{name}.html", f'<main class="doc">{body}</main>', desc),
        encoding="utf-8",
    )
    print("wrote", f"{name}.html")

for name in ("index", "support"):
    src = ROOT / "content" / f"{name}.body.html"
    meta = (ROOT / "content" / f"{name}.meta").read_text(encoding="utf-8").splitlines()
    (ROOT / f"{name}.html").write_text(
        page(meta[0], f"{name}.html", src.read_text(encoding="utf-8"), meta[1]), encoding="utf-8"
    )
    print("wrote", f"{name}.html")
