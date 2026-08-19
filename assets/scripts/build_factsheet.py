#!/usr/bin/env python3
"""Build a 1212.Stable monthly fact sheet from a JSON data file.

    python3 build_factsheet.py data.json out.html
    python3 build_factsheet.py data.json out.html --pdf out.pdf

The static pages (glossary, risk considerations, important information) come
from defaults.json and only need overriding when the legal or educational copy
changes. See references/data-contract.md for the full schema.
"""
import json, sys, os, html, pathlib, subprocess

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent
RAMP = ["lavender", "gold-sun", "accent", "periwinkle", "amber"]


def e(x):
    return html.escape(str(x), quote=False)


def load(path):
    with open(path) as f:
        return json.load(f)


def deep_default(data, defaults):
    for k, v in defaults.items():
        data.setdefault(k, v)
    return data


# --- fragments --------------------------------------------------------------

def head(meta):
    return f'''    <div class="pagehead">
      <div class="pagehead__row">
        <div class="logo"><span class="logo__mark">1212</span><span class="logo__word">CAPITAL</span></div>
        <div class="pagehead__meta">{e(meta)}</div>
      </div>
      <div class="rule"></div>
    </div>'''


def foot(n, total):
    return f'''  <div class="pagefoot">
    <div class="rule"></div>
    <div class="pagefoot__row">
      <div class="pagefoot__meta">1212 Capital  ·  contact@1212.capital  ·  Confidential</div>
      <div class="pagefoot__page">{n} / {total}</div>
    </div>
  </div>'''


def kvs(pairs, cls="kv"):
    return "\n".join(
        f'          <div class="{cls}"><span class="kv__label">{e(a)}</span>'
        f'<span class="kv__value">{e(b)}</span></div>' for a, b in pairs)


def table(header, rows, colw=240):
    out = ['      <div class="table">',
           '        <div class="table__row table__row--head">',
           f'          <div class="cell cell--head grow">{e(header[0])}</div>',
           f'          <div class="cell cell--head cell--end" style="width:{colw}px;flex:0 0 {colw}px">{e(header[1])}</div>',
           '        </div>']
    for r in rows:
        hl = " table__row--hl" if r.get("highlight") else ""
        lab = "cell--text cell--strong" if r.get("highlight") else "cell--text"
        val = "cell--fig-accent" if r.get("highlight") else "cell--fig"
        out += [f'        <div class="table__row{hl}">',
                f'          <div class="cell {lab} grow">{e(r["label"])}</div>',
                f'          <div class="cell {val}" style="width:{colw}px;flex:0 0 {colw}px">{e(r["value"])}</div>',
                '        </div>']
    out.append('      </div>')
    return "\n".join(out)


def donut(segments, size=210):
    stops, acc = [], 0.0
    for i, s in enumerate(segments):
        col = s.get("color", RAMP[i % len(RAMP)])
        stops.append(f"var(--{col}) {acc:.4g}% {acc + s['pct']:.4g}%")
        acc += s["pct"]
    return (f'<div class="donut" style="width:{size}px;height:{size}px;flex:0 0 {size}px;'
            f'background:conic-gradient({", ".join(stops)})"></div>')


def legend(segments):
    out = []
    for i, s in enumerate(segments):
        col = s.get("color", RAMP[i % len(RAMP)])
        out.append(f'            <div class="legend"><span class="legend__dot" style="background:var(--{col})"></span>'
                   f'<span class="legend__label">{e(s["label"])}</span>'
                   f'<span class="legend__value">{s["pct"]:g}%</span></div>')
    return "\n".join(out)


def exposure(rows):
    mx = max(r["pct"] for r in rows) or 1
    out = []
    for i, r in enumerate(rows):
        col = r.get("color", RAMP[i % len(RAMP)])
        w = round(r["pct"] / mx * 420)
        out.append(f'        <div class="exposure"><span class="exposure__dot" style="background:var(--{col})"></span>'
                   f'<span class="exposure__name">{e(r["name"])}</span>'
                   f'<span class="exposure__bar" style="width:{w}px;background:var(--lavender)"></span>'
                   f'<span class="exposure__value">{r["pct"]:.2f}%</span></div>')
    return "\n".join(out)


def protocols(names):
    half = (len(names) + 1) // 2
    cols = [names[:half], names[half:]]
    out = ['      <div class="columns">']
    n = 0
    for col in cols:
        out.append('        <div style="gap:11px">')
        for name in col:
            out.append(f'          <div class="protocol"><span class="protocol__mark" '
                       f'style="background:var(--{RAMP[n % len(RAMP)]})"></span>'
                       f'<span class="protocol__name">{e(name)}</span></div>')
            n += 1
        out.append('        </div>')
    out.append('      </div>')
    return "\n".join(out)


def returns_table(mr):
    months, fund, btc = mr["months"], mr["fund"], mr["btc"]
    hc = "".join(f'\n          <div class="cell cell--head cell--end grow">{e(m)}</div>' for m in months)
    fc = "".join(f'\n          <div class="cell cell--fig-accent grow">{e(v)}</div>' for v in fund)
    bc = "".join(f'\n          <div class="cell cell--fig grow">{e(v)}</div>' for v in btc)
    return f'''      <div class="table">
        <div class="table__row table__row--head">
          <div class="cell cell--head" style="width:96px;flex:0 0 96px">&nbsp;</div>{hc}
        </div>
        <div class="table__row table__row--hl">
          <div class="cell cell--text cell--strong" style="width:96px;flex:0 0 96px;font-size:10px">{e(mr.get("fund_label", "1212.Stable"))}</div>{fc}
        </div>
        <div class="table__row">
          <div class="cell cell--text cell--strong" style="width:96px;flex:0 0 96px;font-size:10px">BTC</div>{bc}
        </div>
      </div>'''


def entries(items, gap):
    out = []
    half = (len(items) + 1) // 2
    for col in (items[:half], items[half:]):
        out.append(f'        <div style="gap:{gap}px">')
        for it in col:
            out.append(f'          <div class="glossary"><div class="glossary__term">{e(it["term"])}</div>'
                       f'<div class="glossary__def">{e(it["def"])}</div></div>')
        out.append('        </div>')
    return "\n".join(out)


# --- pages ------------------------------------------------------------------

def build(d):
    meta = f'{d["product"]["name"].upper()} · FACT SHEET · AS OF {d["as_of"].upper()}'
    p = d["product"]
    total = 4

    cover = f'''<section class="cover" style="background-image:url('{d.get("cover_image_base", "../img/")}{d.get("cover_image", "midi/opt-02.jpg")}')">
  <div class="cover__scrim cover__scrim--fs"></div>
  <div class="cover__top">
    <div class="logo logo--cover"><span class="logo__mark">1212</span><span class="logo__word">CAPITAL</span></div>
    <div class="cover__issue">{e(d["issue"])}</div>
  </div>
  <div class="cover__bottom">
    <div class="masthead">
      <div class="masthead__kicker masthead__kicker--sentence">{e(p["kicker"])}</div>
      <div class="masthead__headline">{e(p["name"])}</div>
      <div class="masthead__standfirst">{e(p["standfirst"])}</div>
    </div>
    <div class="cover__rule"></div>
    <div class="coverstrip">
''' + "\n".join(
        f'      <div class="coverstrip__col"><div class="coverstrip__label">{e(h["label"])}</div>'
        f'<div class="coverstrip__value">{e(h["value"])}</div></div>' for h in d["headline"]) + f'''
    </div>
    <div class="cover__notice">Fact sheet as of {e(d["as_of"])}   ·   Confidential. For professional investors only. Not for retail distribution.</div>
  </div>
</section>'''

    page1 = f'''<section class="page">
  <div class="page__content">
{head(meta)}

    <div class="stack" style="gap:18px">
      <div class="row" style="gap:28px">
        <div class="stack" style="width:408px;flex:0 0 408px;gap:12px">
          <div class="tag">FUND DESCRIPTION</div>
          <div class="body-just">{e(d["description"])}</div>
        </div>
        <div class="stack" style="width:246px;flex:0 0 246px;gap:12px">
          <div class="tag">KEY FACTS</div>
{kvs(d["key_facts"])}
        </div>
      </div>
      <div class="row" style="gap:28px">
        <div class="stack" style="width:408px;flex:0 0 408px;gap:12px">
          <div class="tag">NET PERFORMANCE</div>
{kvs(d["performance"], "kv kv--metric")}
        </div>
        <div class="stack" style="width:246px;flex:0 0 246px;gap:12px">
          <div class="tag">TERMS</div>
{kvs(d["terms"])}
        </div>
      </div>
    </div>

    <div class="section">
      <div class="tag">{e(d.get("comparison_label", "CURRENT YIELD ENVIRONMENT"))}</div>
{table(d["yield_environment"]["header"], d["yield_environment"]["rows"])}
      <div class="footnote">{e(d["yield_environment"]["source"])}</div>
    </div>

    <div class="section">
      <div class="tag">RISK METRICS</div>
      <div class="statrow">
''' + "\n".join(
        f'        <div class="stat"><div class="stat__key">{e(k)}</div><div class="stat__value">{e(v)}</div></div>'
        for k, v in d["risk_metrics"]["items"]) + f'''
      </div>
      <div class="footnote">{e(d["risk_metrics"]["source"])}</div>
    </div>

  </div>
{foot(1, total)}
</section>'''

    a = d["allocation"]
    page2 = f'''<section class="page">
  <div class="page__content page__content--tight">
{head(meta)}

    <div class="tag">CURRENT ALLOCATION</div>

    <div class="section">
      <div class="heading"><span class="heading__main">{e(a.get("heading", "Strategy Allocation"))}</span><span class="heading__suffix">{e(a.get("suffix", "% of NAV"))}</span></div>
      <div class="row" style="gap:40px;align-items:center">
        {donut(a["segments"])}
        <div class="stack grow" style="gap:18px">
          <div class="stack" style="gap:10px">
{legend(a["segments"])}
          </div>
          <div class="note">{e(a["note"])}</div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="heading"><span class="heading__main">Stablecoins Exposure</span><span class="heading__suffix">% of NAV</span></div>
      <div class="stack" style="gap:11px">
{exposure(d["stablecoins"])}
      </div>
    </div>

    <div class="section">
      <div class="heading"><span class="heading__main">Protocols Exposure</span></div>
{protocols(d["protocols"])}
    </div>

    <div class="footnote">{e(d["allocation_source"])}</div>

    <div class="section">
      <div class="tag">MONTHLY RETURNS VS BTC</div>
{returns_table(d["monthly_returns"])}
      <div class="footnote">{e(d["monthly_returns"]["source"])}</div>
    </div>

  </div>
{foot(2, total)}
</section>'''

    page3 = f'''<section class="page">
  <div class="page__content page__content--tight">
{head(meta)}

    <div class="section">
      <div class="tag">GLOSSARY</div>
      <div class="columns">
{entries(d["glossary"], 19)}
      </div>
    </div>

    <div class="section">
      <div class="tag">RISK CONSIDERATIONS</div>
      <div class="columns">
{entries(d["risks"], 15)}
      </div>
    </div>

  </div>
{foot(3, total)}
</section>'''

    half = (len(d["issuer"]) + 1) // 2
    issuer_cols = "\n".join(
        f'      <div style="gap:9px">\n' + kvs(col, "kv kv--sm") + '\n      </div>'
        for col in (d["issuer"][:half], d["issuer"][half:]))

    page4 = f'''<section class="page">
  <div class="page__content">
{head(meta)}

    <div class="tag">IMPORTANT INFORMATION</div>

    <div class="stack" style="gap:11px">
''' + "\n".join(f'      <div class="disclaimer">{e(t)}</div>' for t in d["legal"]) + f'''
    </div>

    <div class="tag">ISSUER &amp; CONTACT</div>

    <div class="columns">
{issuer_cols}
    </div>

  </div>
{foot(4, total)}
</section>'''

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{e(p["name"])} — Fact Sheet — {e(d["as_of"])}</title>
<link rel="stylesheet" href="{d.get("css", "../css/1212.css")}">
</head>
<body>
{cover}
{page1}
{page2}
{page3}
{page4}
</body>
</html>
'''


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    data = load(sys.argv[1])
    fund = data.get("fund")
    if fund:
        reg = load(ASSETS / "schemas" / "funds.json")["funds"]
        if fund not in reg:
            sys.exit(f"unknown fund {fund!r}. Known: {', '.join(reg)}. "
                     f"Add it to assets/schemas/funds.json with its Lagoon address and its own copy block.")
        f = reg[fund]
        c = f["copy"]
        data.setdefault("product", {"name": f["name"], "kicker": c["kicker"], "standfirst": c["standfirst"]})
        data.setdefault("description", c["description"])
        data.setdefault("key_facts", c["key_facts"])
        data.setdefault("glossary", c["glossary"])
        data.setdefault("risks", c["risks"])
        data.setdefault("comparison_label", c["comparison_label"])
        data.setdefault("allocation", {})
        data["allocation"].setdefault("heading", c["allocation_heading"])
        data.setdefault("yield_environment", {})
        data["yield_environment"].setdefault("header", c["comparison_heading"])
    data = deep_default(data, load(ASSETS / "schemas" / "factsheet.defaults.json"))
    out = sys.argv[2]
    data.setdefault("css", str(ASSETS / "css" / "1212.css"))
    data.setdefault("cover_image_base", str(ASSETS / "img") + "/")
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out).write_text(build(data))
    print("HTML ->", out)
    if "--pdf" in sys.argv:
        pdf = sys.argv[sys.argv.index("--pdf") + 1]
        subprocess.run([sys.executable, str(HERE / "render_pdf.py"), out, pdf], check=True)


if __name__ == "__main__":
    main()
