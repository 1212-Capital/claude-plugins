#!/usr/bin/env python3
"""Report how full each page's Content stack is, before exporting a PDF.

    python3 measure_pages.py doc.html

The 1212 A4 pages are 1123 px tall with 56 px margins. A page overflows when
its Content stack plus the footer exceeds that. This prints the used height and
the slack for every page, and exits non-zero if anything overflows.
"""
import sys, pathlib, asyncio

JS = """() => [...document.querySelectorAll('.page')].map((pg, i) => {
  const c = pg.querySelector('.page__content');
  const f = pg.querySelector('.pagefoot');
  const pad = 56 * 2;
  const avail = pg.clientHeight - pad - (f ? f.offsetHeight : 0);
  let used = 0;
  if (c) { for (const k of c.children) used += k.offsetHeight;
           used += (c.children.length - 1) * parseFloat(getComputedStyle(c).gap || 0); }
  return {page: i + 2, used: Math.round(used), avail: Math.round(avail),
          slack: Math.round(avail - used), overflow: used > avail + 0.5};
})"""


async def run(src):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 794, "height": 1123})
        await pg.goto(pathlib.Path(src).resolve().as_uri(), wait_until="networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(400)
        rows = await pg.evaluate(JS)
        await b.close()
    bad = 0
    for r in rows:
        flag = "OVERFLOW" if r["overflow"] else ("tight" if r["slack"] < 24 else "ok")
        bad += r["overflow"]
        print(f"  page {r['page']}: {r['used']:4d} / {r['avail']:4d} px   slack {r['slack']:+5d}   {flag}")
    return bad


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(1 if asyncio.run(run(sys.argv[1])) else 0)
