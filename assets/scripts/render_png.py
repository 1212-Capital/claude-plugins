#!/usr/bin/env python3
"""Render each .post element of a 1212 social HTML file to a PNG at 1x.

    python3 render_png.py social.html outdir
"""
import sys, os, pathlib, asyncio


async def run(src, outdir):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        sys.exit("playwright is required:  pip install playwright  &&  playwright install chromium")
    os.makedirs(outdir, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 2000, "height": 1200}, device_scale_factor=1)
        await pg.goto(pathlib.Path(src).resolve().as_uri(), wait_until="networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(400)
        for i, n in enumerate(await pg.query_selector_all(".post"), 1):
            await n.screenshot(path=os.path.join(outdir, f"post{i:02d}.png"))
            print("->", os.path.join(outdir, f"post{i:02d}.png"))
        await b.close()


if __name__ == "__main__":
    asyncio.run(run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "out"))
