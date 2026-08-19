#!/usr/bin/env python3
"""Check a 1212 PDF for the colour bug that makes brand photographs go magenta.

    python3 check_pdf.py doc.pdf [more.pdf ...]

Chromium embeds JPEGs byte for byte and tags them `/ColorTransform 0`, meaning
"these three components are already RGB". They are YCbCr. A reader that honours
the flag renders Y, Cb, Cr as R, G, B, which turns every cover pink. Readers
differ, so a PDF can look correct in one viewer and wrong in another. This
checks the declaration against the actual JPEG data and exits non-zero on a
mismatch.
"""
import sys, re, struct, pathlib


def jpeg_components(buf):
    i, n = 2, len(buf)
    while i + 4 <= n and buf[i] == 0xFF:
        marker = buf[i + 1]
        if marker in (0xD8, 0xD9):
            i += 2
            continue
        ln = struct.unpack(">H", buf[i + 2:i + 4])[0]
        seg = buf[i + 4:i + 2 + ln]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            ncomp = seg[5]
            return [seg[6 + 3 * k] for k in range(ncomp)]
        if marker == 0xDA:
            return None
        i += 2 + ln
    return None


def check(path):
    data = pathlib.Path(path).read_bytes()
    images = bad = 0
    for m in re.finditer(rb"/Subtype\s*/Image(.{0,600}?)stream", data, re.S):
        head = m.group(1)
        if b"DCTDecode" not in head:
            continue
        s = m.end()
        while s < len(data) and data[s] in (0x0D, 0x0A):
            s += 1
        if data[s:s + 2] != b"\xff\xd8":
            continue
        images += 1
        ids = jpeg_components(data[s:s + 4096]) or []
        is_rgb_data = ids == [ord("R"), ord("G"), ord("B")]
        ct = re.search(rb"/ColorTransform\s+(\d)", head)
        ct = int(ct.group(1)) if ct else None          # None = PDF default applies
        declared_rgb = ct == 0
        if len(ids) == 3 and declared_rgb != is_rgb_data:
            bad += 1
            print(f"  ! image {images}: JPEG is {'RGB' if is_rgb_data else 'YCbCr'}, "
                  f"stream declares /ColorTransform {ct}")
    status = "FAIL" if bad else "ok"
    print(f"{status:4s} {path}  ({images} JPEG image{'s' if images != 1 else ''}, {bad} mismatched)")
    return bad


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(1 if sum(check(p) for p in sys.argv[1:]) else 0)
