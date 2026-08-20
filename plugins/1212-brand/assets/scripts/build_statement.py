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


def foot(n, total=2):
    return f'''  <div class="pagefoot">
    <div class="rule"></div>
    <div class="pagefoot__row">
      <div class="pagefoot__meta">1212 CAPITAL · CONFIDENTIAL · PREPARED FOR THE NAMED ACCOUNT HOLDER</div>
      <div class="pagefoot__page">{n} / {total}</div>
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
    fund = fund_label(d)
    addr = short_address(c["address"])
    meta = f'{c["name"].upper()} · {fund.upper()} · {addr} · {d["as_of"].upper()}'
    img = d.get("cover_image_base", str(ASSETS / "img") + "/") + d.get("cover_image", "matin/opt-03.jpg")

    cover = f'''<section class="cover" style="background-image:url('{img}')">
  <div class="cover__scrim"></div>
  <div class="cover__top">
    <div class="logo logo--cover"><span class="logo__mark">1212</span><span class="logo__word">CAPITAL</span></div>
    <div class="cover__issue">CONFIDENTIAL · CLIENT STATEMENT</div>
  </div>
  <div class="cover__bottom">
    <div class="masthead">
      <div class="masthead__kicker">STATEMENT OF ACCOUNT · {e(fund.upper())}</div>
      <div class="masthead__headline">{e(c["name"])}</div>
      <div class="masthead__standfirst">Your holdings, movements and performance for the period, prepared by 1212 Capital.</div>
    </div>
    <div class="cover__rule"></div>
    <div class="coverstrip coverstrip--sm">
      <div class="coverstrip__col"><div class="coverstrip__label">ADDRESS</div><div class="coverstrip__value">{e(addr)}</div></div>
      <div class="coverstrip__col"><div class="coverstrip__label">PERIOD</div><div class="coverstrip__value">{e(d["period"])}</div></div>
      <div class="coverstrip__col"><div class="coverstrip__label">CURRENCY</div><div class="coverstrip__value">{e(d.get("currency", "USD"))}</div></div>
      <div class="coverstrip__col"><div class="coverstrip__label">FUND</div><div class="coverstrip__value">{e(fund)}</div></div>
    </div>
    <div class="cover__notice">Prepared for the named account holder. Not a contract note and not for onward distribution.</div>
  </div>
</section>'''

    cur = d.get("currency", "USD")
    pos_rows = [[(p["strategy"], None, False), (p["units"], 100, True), (p["nav"], 100, True),
                 (p["value"], 120, True), (p.get("currency", cur), 60, True),
                 (p["weight"], 80, True)] for p in d["positions"]]

    page1 = f'''<section class="page">
  <div class="page__content page__content--stmt">
{head(meta)}

    <div class="section">
      <div class="tag">PORTFOLIO SUMMARY</div>
      <div class="statrow">
''' + "\n".join(f'        <div class="stat"><div class="stat__key">{e(k)}</div>'
                f'<div class="stat__value">{e(v)}</div></div>' for k, v in [
                    (h["label"], h["value"]) if isinstance(h, dict) else h for h in d["headline"]]) + f'''
      </div>
    </div>

    <div class="cols327">
      <div style="gap:12px">
        <div class="tag">ACCOUNT</div>
{kvs([("Address", addr), ("Fund", fund),
      ("Base currency", d.get("currency", "USD")), ("Opened", c["opened"])])}
      </div>
      <div style="gap:12px">
        <div class="tag">YOUR PERFORMANCE</div>
{kvs(d["performance"], "kv kv--metric")}
      </div>
    </div>

    <div class="section">
      <div class="tag">POSITIONS</div>
{table([("Strategy", None, False), ("Units", 100, True), ("NAV", 100, True), ("Value", 120, True), ("Ccy", 60, True), ("Weight", 80, True)], pos_rows)}
      <div class="footnote">{e(d["positions_note"])}</div>
    </div>

  </div>
{foot(1)}
</section>'''

    # inception to date, and no fee lines: fees are explained in Important
    # Information now, and every figure on this statement is already net of them.
    movements = [m for m in d.get("movements_since_inception", d.get("movements", []))
                 if m.get("type", "").lower() != "fee"]
    mv_rows = [[(m["date"], 110, False), (m["type"], 190, False),
                (m["amount"], 150, True), (m.get("currency", cur), 70, True)] for m in movements]

    page2 = f'''<section class="page">
  <div class="page__content page__content--stmt">
{head(meta)}

    <div class="section">
      <div class="tag">MOVEMENTS SINCE INCEPTION</div>
{table([("Date", 110, False), ("Type", 190, False), ("Amount", 150, True), ("Ccy", 70, True)], mv_rows)}
      <div class="footnote">{e(d["movements_note"])}</div>
    </div>

    <div class="section">
      <div class="tag">IMPORTANT INFORMATION</div>
''' + "\n".join(f'      <div class="disclaimer disclaimer--soft">{e(x)}</div>' for x in d["legal"]) + f'''
    </div>

  </div>
{foot(2)}
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
</body>
</html>
'''


# Placeholders that must never reach a client. A document that prints one of
# these is worse than a document that fails to build: nobody notices.
PLACEHOLDER_MARKS = ("XX days", "DD/MM/YYYY", "MMM YYYY", "XX.XX", "0000-0000",
                     "[TBD]", "TODO", "Example Family Trust", "Lorem ipsum")


def refuse_placeholders(html, where):
    hits = sorted({m for m in PLACEHOLDER_MARKS if m in html})
    if hits:
        sys.exit(
            f"{where}: refusing to build, unresolved placeholder(s) still present: "
            + ", ".join(repr(h) for h in hits)
            + ".\nFill them in the input file, or in statement.defaults.json for the legal copy."
        )


FUND_LABELS = {"stable": "1212.Stable", "alpha": "1212.Alpha"}


def fund_label(data):
    """The fund this statement covers. One statement per fund, never a blend."""
    f = data.get("fund")
    if not f:
        sys.exit("statement: 'fund' is required. One statement per fund; say which one.")
    return data.get("fund_label") or FUND_LABELS.get(f, f)


def short_address(addr):
    """The one truncation used everywhere: cover, page heads, statement reference."""
    a = str(addr)
    if not a.startswith("0x") or len(a) < 12:
        sys.exit(f"statement: expected an ERC-20 address, got {a!r}")
    return f"{a[:6]}\u2026{a[-3:]}"


def statement_ref(data):
    """CS-2026-07 · STABLE · 0xbb30…eb5 · unique per account, month and fund."""
    return " \u00b7 ".join([
        data.get("reference", "CS"),
        data.get("fund", "").upper(),
        short_address(data["client"]["address"]),
    ])


def one(data, defaults, out, pdf):
    for k, v in defaults.items():
        data.setdefault(k, v)
    # the reference must identify the fund too: one client can hold several
    ref = statement_ref(data)
    data["contact"] = [[a, ref if a == "Statement reference" else b] for a, b in data["contact"]]
    html = build(data)
    refuse_placeholders(html, out)
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out).write_text(html)
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
        written = set()
        for acc in accounts:
            merged = {**base, **acc}
            slug = "-".join([
                merged.get("reference", "CS"),
                merged.get("fund", ""),
                short_address(merged["client"]["address"]).replace("\u2026", ""),
            ]).replace(" ", "")
            out = str(pathlib.Path(dest) / f"{slug}.html")
            if out in written:
                sys.exit(f"statement: two accounts produce the same file {out!r}. "
                         "Check that fund and address differ.")
            written.add(out)
            one(merged, defaults, out, out.replace(".html", ".pdf") if want_pdf else None)
    else:
        pdf = None
        if want_pdf:
            i = sys.argv.index("--pdf") + 1
            explicit = sys.argv[i] if i < len(sys.argv) and not sys.argv[i].startswith("--") else None
            # bare --pdf derives the path from dest, the way --batch already does
            pdf = explicit or str(pathlib.Path(dest).with_suffix(".pdf"))
        one(data, defaults, dest, pdf)


if __name__ == "__main__":
    main()
