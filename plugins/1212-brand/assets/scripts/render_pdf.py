#!/usr/bin/env python3
"""Render a 1212 Capital HTML document to a true A4 PDF (794 x 1123 px @ 96 dpi).

    python3 render_pdf.py input.html [output.pdf]
    python3 render_pdf.py input.html --png outdir     # one PNG per page, for review

Every .page / .cover element becomes exactly one PDF page. Fonts and images are
loaded from the plugin's assets/ directory, so the HTML must reference them with
the relative paths the templates already use.

Chromium passes JPEGs into the PDF byte for byte but tags the stream
`/ColorTransform 0`, which tells a reader the three components are already RGB.
They are YCbCr. Lenient readers ignore the flag; strict ones honour it and the
brand photographs come out magenta. `fix_jpeg_colortransform` repairs the flag
in place after Chromium writes the file. Same byte length, so the xref offsets
stay valid.
"""
import sys, os, re, struct, pathlib, asyncio

W, H = 794, 1123


# --- JPEG colour-transform repair -------------------------------------------

def _jpeg_is_ycbcr(buf):
    """True when a JPEG's frame header describes YCbCr rather than RGB."""
    i = 2
    n = len(buf)
    while i + 4 <= n and buf[i] == 0xFF:
        marker = buf[i + 1]
        if marker in (0xD8, 0xD9):
            i += 2
            continue
        ln = struct.unpack(">H", buf[i + 2:i + 4])[0]
        seg = buf[i + 4:i + 2 + ln]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):          # SOF
            ncomp = seg[5]
            ids = [seg[6 + 3 * k] for k in range(ncomp)]
            if ncomp != 3:
                return False
            # 'R','G','B' component ids mean the data really is RGB
            return ids != [ord("R"), ord("G"), ord("B")]
        if marker == 0xDA:                               # SOS, no frame header found
            return False
        i += 2 + ln
    return False


def fix_jpeg_colortransform(path):
    """Set /ColorTransform 1 on DCTDecode streams whose JPEG is YCbCr."""
    data = bytearray(pathlib.Path(path).read_bytes())
    fixed = 0
    for m in re.finditer(rb"/ColorTransform\s+0", bytes(data)):
        s = data.find(b"stream", m.end())
        if s == -1:
            continue
        j = s + 6
        while j < len(data) and data[j] in (0x0D, 0x0A):
            j += 1
        if data[j:j + 2] != b"\xff\xd8":                  # not a JPEG stream
            continue
        if not _jpeg_is_ycbcr(data[j:j + 4096]):
            continue
        zero = data.rfind(b"0", m.start(), m.end())
        data[zero:zero + 1] = b"1"
        fixed += 1
    if fixed:
        pathlib.Path(path).write_bytes(bytes(data))
    return fixed


# --- render ------------------------------------------------------------------

async def run(src, out, png_dir):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        sys.exit("playwright is required:  pip install playwright  &&  playwright install chromium")

    url = pathlib.Path(src).resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": W, "height": H},
                                      device_scale_factor=2)
        await page.goto(url, wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(400)

        if png_dir:
            os.makedirs(png_dir, exist_ok=True)
            nodes = await page.query_selector_all(".page, .cover")
            for i, node in enumerate(nodes, 1):
                await node.screenshot(path=os.path.join(png_dir, f"p{i:02d}.png"))
            print(f"{len(nodes)} PNG -> {png_dir}")

        await page.pdf(path=out, width=f"{W}px", height=f"{H}px",
                       print_background=True,
                       margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                       prefer_css_page_size=True)
        await browser.close()

    n = fix_jpeg_colortransform(out)
    print(f"PDF -> {out}" + (f"  ({n} JPEG colour flags repaired)" if n else ""))


def main():
    args = list(sys.argv[1:])
    if not args:
        print(__doc__)
        sys.exit(1)
    src = args[0]
    png_dir = None
    if "--png" in args:
        i = args.index("--png")
        png_dir = args[i + 1]
        args = args[:i] + args[i + 2:]
    out = args[1] if len(args) > 1 else os.path.splitext(src)[0] + ".pdf"
    asyncio.run(run(src, out, png_dir))


if __name__ == "__main__":
    main()
