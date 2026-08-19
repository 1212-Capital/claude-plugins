#!/usr/bin/env python3
"""Start a 1212 document from a template, anywhere on disk.

    python3 new_doc.py factsheet   out/factsheet-2026-07.html
    python3 new_doc.py newsletter  out/newsletter-2026-07.html
    python3 new_doc.py internal-doc out/protocol-review.html
    python3 new_doc.py social      out/posts.html

Copies the template and rewrites its `../css/` and `../img/` references to
absolute paths inside the plugin, so the copy renders correctly from any
directory.
"""
import sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent
TEMPLATES = {p.stem: p for p in (ASSETS / "templates").glob("*.html")}


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in TEMPLATES:
        print(__doc__)
        print("templates:", ", ".join(sorted(TEMPLATES)))
        sys.exit(1)
    src, out = TEMPLATES[sys.argv[1]], pathlib.Path(sys.argv[2])
    html = src.read_text()
    html = html.replace("../css/", str(ASSETS / "css") + "/")
    html = html.replace("../img/", str(ASSETS / "img") + "/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("->", out)


if __name__ == "__main__":
    main()
