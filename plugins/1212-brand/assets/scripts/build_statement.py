#!/usr/bin/env python3
"""Build a 1212 Capital client statement from a JSON data file.

    python3 build_statement.py client.json out.html [--pdf out.pdf]
    python3 build_statement.py clients.json outdir/ --batch [--pdf]

With --batch the JSON is a list of accounts and one HTML (and PDF) is written
per account, named from the statement reference and the account number. See
references/data-contract.md for the schema.
"""
import json, sys, html, pathlib, subprocess

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent


def e(x):
    return html.escape(str(x), quote=False)


def head(meta):
    return f'''    <div class="pagehead">
      <div class="pagehead__row">
        <div class="logo"><span class="logo__mark">1212</span><span class="logo__word">CAPITAL</span></div>
        <div class="pagehead__meta">{e(meta)}</div>
      </div>
      <div class="rule"></div>
    </div>'''


def foot(n):
    return f'''  <div class="pagefoot">
    <div class="rule"></div>
    <div class="pagefoot__row">
      <div class="pagefoot__meta">1212 CAPITAL · CONFIDENTIAL · PREPARED FOR THE NAMED ACCOUNT HOLDER</div>
      <div class="pagefoot__page">{n} / 3</div>
    </div>
  </div>'''


def kvs(pairs, cls="kv"):
    return "\n".join(f'        <div class="{cls}"><span class="kv__label">{e(a)}</span>'
                     f'<span class="kv__value">{e(b)}</span></div>' for a, b in pairs)


def cells(items):
    """items: list of (text, width|None, is_figure)"""
    out = []
    for txt, w, fig in items:
        cls = "cell cell--fig cell--pad9" if fig else "cell cell--text cell--pad9"
        style = f' style="width:{w}px;flex:0 0 {w}px"' if w else ""
        out.append(f'          <div class="{cls}{"" if w else " grow"}"{style}>{e(txt)}</div>')
    return "\n".join(out)


def heads(items):
    out = []
    for txt, w, right in items:
        cls = "cell cell--head cell--pad9" + (" cell--end" if right else "")
        style = f' style="width:{w}px;flex:0 0 {w}px"' if w else ""
        out.append(f'          <div class="{cls}{"" if w else " grow"}"{style}>{e(txt)}</div>')
    return "\n".join(out)


def table(header_row, rows):
    body = "\n".join(f'        <div class="table__row">\n{cells(r)}\n        </div>' for r in rows)
    return (f'      <div class="table">\n'
            f'        <div class="table__row table__row--head">\n{heads(header_row)}\n        </div>\n'
            f'{body}\n      </div>')


def build(d):
    c = d["client"]
    meta = f'{c["name"].upper()} · ACCOUNT {c["account"]} · {d["as_of"].upper()}'
    img = d.get("cover_image_base", str(ASSETS / "img") + "/") + d.get("cover_image", "matin/opt-03.jpg")

    cover = f'''<section class="cover" style="background-image:url('{img}')">
  <div class="cover__scrim"></div>
  <div class="cover__top">
    <div class="logo logo--cover"><span class="logo__mark">1212</span><span class="logo__word">CAPITAL</span></div>
    <div class="cover__issue">CONFIDENTIAL · CLIENT STATEMENT</div>
  </div>
  <div class="cover__bottom">
    <div class="masthead">
      <div class="masthead__kicker">STATEMENT OF ACCOUNT</div>
      <div class="masthead__headline">{e(c["name"])}</div>
      <div class="masthead__standfirst">Your holdings, movements and performance for the period, prepared by 1212 Capital.</div>
    </div>
    <div class="cover__rule"></div>
    <div class="coverstrip coverstrip--sm">
      <div class="coverstrip__col"><div class="coverstrip__label">ACCOUNT</div><div class="coverstrip__value">{e(c["account"])}</div></div>
      <div class="coverstrip__col"><div class="coverstrip__label">PERIOD</div><div class="coverstrip__value">{e(d["period"])}</div></div>
      <div class="coverstrip__col"><div class="coverstrip__label">CURRENCY</div><div class="coverstrip__value">{e(d.get("currency", "USD"))}</div></div>
      <div class="coverstrip__col"><div class="coverstrip__label">RELATIONSHIP</div><div class="coverstrip__value">{e(c["manager"])}</div></div>
    </div>
    <div class="cover__notice">Prepared for the named account holder. Not a contract note and not for onward distribution.</div>
  </div>
</section>'''

    pos_rows = [[(p["strategy"], None, False), (p["units"], 110, True), (p["nav"], 110, True),
                 (p["value"], 130, True), (p["weight"], 90, True)] for p in d["positions"]]

    page1 = f'''<section class="page">
  <div class="page__content page__content--stmt">
{head(meta)}

    <div class="section">
      <div class="tag">PORTFOLIO SUMMARY</div>
      <div class="statrow">
''' + "\n".join(f'        <div class="stat"><div class="stat__key">{e(h["label"])}</div>'
                f'<div class="stat__value">{e(h["value"])}</div></div>' for h in d["headline"]) + f'''
      </div>
    </div>

    <div class="cols327">
      <div style="gap:12px">
        <div class="tag">ACCOUNT</div>
{kvs([("Account number", c["account"]), ("Account type", c["type"]),
      ("Base currency", d.get("currency", "USD")), ("Opened", c["opened"]),
      ("Relationship manager", c["manager"])])}
      </div>
      <div style="gap:12px">
        <div class="tag">YOUR PERFORMANCE</div>
{kvs(d["performance"], "kv kv--metric")}
      </div>
    </div>

    <div class="section">
      <div class="tag">POSITIONS</div>
{table([("Strategy", None, False), ("Units", 110, True), ("NAV", 110, True), ("Value", 130, True), ("Weight", 90, True)], pos_rows)}
      <div class="footnote">{e(d["positions_note"])}</div>
    </div>

  </div>
{foot(1)}
</section>'''

    mv_rows = [[(m["date"], 110, False), (m["type"], 170, False), (m["strategy"], None, False),
                (m["amount"], 150, True)] for m in d["movements"]]
    fee_rows = [[(f["item"], None, False), (f["basis"], 220, False), (f["amount"], 150, True)]
                for f in d["fees"]]
    com = d["commentary"]

    page2 = f'''<section class="page">
  <div class="page__content page__content--stmt">
{head(meta)}

    <div class="section">
      <div class="tag">MOVEMENTS THIS PERIOD</div>
{table([("Date", 110, False), ("Type", 170, False), ("Strategy", None, False), ("Amount", 150, True)], mv_rows)}
      <div class="footnote">{e(d["movements_note"])}</div>
    </div>

    <div class="section">
      <div class="tag">FEES &amp; COSTS</div>
{table([("Item", None, False), ("Basis", 220, False), ("This period", 150, True)], fee_rows)}
    </div>

    <div class="section">
      <div class="tag">COMMENTARY</div>
      <div class="commentary">
        <div class="commentary__title">{e(com["title"])}</div>
''' + "\n".join(f'        <div class="commentary__body">{e(p)}</div>' for p in com["body"]) + f'''
      </div>
    </div>

  </div>
{foot(2)}
</section>'''

    contact = d["contact"]
    half = (len(contact) + 1) // 2
    page3 = f'''<section class="page">
  <div class="page__content page__content--stmt-wide">
{head(meta)}

    <div class="section">
      <div class="tag">IMPORTANT INFORMATION</div>
''' + "\n".join(f'      <div class="disclaimer disclaimer--soft">{e(p)}</div>' for p in d["legal"]) + f'''
    </div>

    <div class="section">
      <div class="tag">QUESTIONS ON THIS STATEMENT</div>
      <div class="cols327">
        <div style="gap:9px">
{kvs(contact[:half], "kv kv--sm")}
        </div>
        <div style="gap:9px">
{kvs(contact[half:], "kv kv--sm")}
        </div>
      </div>
    </div>

  </div>
{foot(3)}
</section>'''

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>1212 Capital · Client Statement · {e(c["name"])} · {e(d["period"])}</title>
<link rel="stylesheet" href="{d.get("css", str(ASSETS / "css" / "1212.css"))}">
</head>
<body>
{cover}
{page1}
{page2}
{page3}
</body>
</html>
'''


def one(data, defaults, out, pdf):
    for k, v in defaults.items():
        data.setdefault(k, v)
    # the statement reference carries the account number
    ref = f'{data.get("reference", "CS")} · {data["client"]["account"]}'
    data["contact"] = [[a, ref if a == "Statement reference" else b] for a, b in data["contact"]]
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out).write_text(build(data))
    print("HTML ->", out)
    if pdf:
        subprocess.run([sys.executable, str(HERE / "render_pdf.py"), out, pdf], check=True)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, dest = sys.argv[1], sys.argv[2]
    want_pdf = "--pdf" in sys.argv
    defaults = json.loads((ASSETS / "schemas" / "statement.defaults.json").read_text())
    data = json.loads(pathlib.Path(src).read_text())

    if "--batch" in sys.argv:
        accounts = data if isinstance(data, list) else data["accounts"]
        base = data.get("common", {}) if isinstance(data, dict) else {}
        for acc in accounts:
            merged = {**base, **acc}
            slug = f'{merged.get("reference", "CS")}-{merged["client"]["account"]}'.replace(" ", "")
            out = str(pathlib.Path(dest) / f"{slug}.html")
            one(merged, defaults, out, out.replace(".html", ".pdf") if want_pdf else None)
    else:
        i = sys.argv.index("--pdf") + 1 if want_pdf else None
        pdf = sys.argv[i] if want_pdf and i < len(sys.argv) and not sys.argv[i].startswith("--") else None
        one(data, defaults, dest, pdf)


if __name__ == "__main__":
    main()
