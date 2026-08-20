# 1212 Capital — brand plugin

Everything needed to produce an on-brand 1212 Capital artefact without opening
the Pencil file: the design tokens, the voice, the three A4 document templates
and the four social canvases.

## Who this is for

Anyone at 1212 who needs to produce a branded document. You do not need Pencil,
you do not need the design file, and you do not need any of the connectors the
brand was built with. You need Python with Playwright and a Chromium build:

```bash
pip install playwright && playwright install chromium
```

The fonts and all 18 brand images ship inside the plugin, so rendering works
offline. The Pencil route is there for whoever maintains `1212.pen`; everyone
else can ignore it.

Every document skill **asks before it builds**: which fund, which month, which
client, which cover image. One round of questions, defaults pre-selected.

## Skills

| Skill | Ask for it with |
|---|---|
| **1212-brand-kit** | "what are our colours", "which font", "make this on-brand", "a social post for 1212", "brand guidelines" |
| **1212-fact-sheet** | "the monthly fact sheet", "update the fact sheet with June's numbers" |
| **1212-newsletter** | "the monthly newsletter", "this month's market roundup" |
| **1212-internal-document** | "a due diligence memo", "an investment review", "an internal framework" |
| **1212-client-statement** | "the client statements", "statement of account for [client]" |

The brand kit is the shared foundation; the other four load it for palette,
type and voice.

## What's in `assets/`

```
assets/
├── css/1212.css              the design system, verified against Pencil
├── fonts/                    Lora · Inter · IBM Plex Mono, offline
├── img/{matin,midi,soir}/    the 18 brand landscapes
├── templates/                factsheet · newsletter · internal-doc · client-statement · social
├── schemas/                  fact sheet and statement contracts, defaults, examples
└── scripts/
    ├── new_doc.py             template -> a working copy, paths made absolute
    ├── build_factsheet.py    JSON -> fact sheet HTML (+ PDF)
    ├── build_statement.py    JSON -> client statement, single or batch
    ├── measure_pages.py      how full each Content stack is, before exporting
    ├── render_pdf.py         HTML -> A4 PDF (and per-page PNGs)
    └── render_png.py         social HTML -> PNG per canvas
```

## Two production routes

**Pencil** — highest fidelity, stays editable, needs the app open on
`1212.pen`. Component IDs and the build recipe are in the brand kit's
`references/pencil.md`.

**Self-contained HTML → PDF** — works anywhere. Requires Python with
Playwright and a Chromium build; no network, since the fonts and images ship
with the plugin.

```bash
# start any document from its template, asset paths rewritten to absolute
python3 assets/scripts/new_doc.py newsletter out/newsletter-2026-07.html

# monthly fact sheet from data
python3 assets/scripts/build_factsheet.py june.json out.html --pdf out.pdf

# one client statement per account
python3 assets/scripts/build_statement.py july-accounts.json out/2026-07/ --batch --pdf

# page fill check before exporting
python3 assets/scripts/measure_pages.py doc.html

# any 1212 document
python3 assets/scripts/render_pdf.py doc.html doc.pdf --png review

# social canvases
python3 assets/scripts/render_png.py assets/templates/social.html out/

# colour sanity on any PDF before it leaves
python3 assets/scripts/check_pdf.py doc.pdf
```

## Fidelity

The stylesheet was checked against the Pencil renderer page by page, by
exporting every page of the four documents from `1212.pen` to HTML and running
a pixel diff. The fact sheet, newsletter, internal document and client
statement all render at 0.00% pixel difference, except the fact sheet's donut,
which differs by 0.08% of the page from mask antialiasing.

One thing a pixel diff cannot catch: Chromium embeds JPEGs byte for byte into
the PDF but tags them `/ColorTransform 0`, which declares the three components
already RGB when they are YCbCr. Strict PDF readers honour the flag and render
every brand photograph magenta, while lenient ones look correct.
`render_pdf.py` repairs the flag; `check_pdf.py` verifies it. Rendering to PNG
and diffing will never surface this, because both sides of the diff are PNG.

Two consequences worth knowing before editing `1212.css`:

- Pencil renders `Math.round(fontSize × lineHeight)` pixels, so the CSS uses
  integer px line-heights, not ratios. Round half **up**.
- Exposure bars in the fact sheet are all lavender. Only the dot carries the
  ramp colour.
- The newsletter Content gap is 26, not 30, since the source lines moved into
  the article and brief blocks.

## Data blocks

Data plates (`.plate`, `.hbar`, `.stackbar`) and entity chips (`.chip`) let an
inner page carry information where a decorative photograph used to sit. They
exist as Pencil components too, in the newsletter Blocks Library under
**MEDIA & DATA**: `NL · Plate · Comparison`, `NL · Plate · Figure`,
`NL · Plate · Composition`, `NL · Chip Row`, plus the `NL · Bar Row` and
`NL · Legend Item` bricks they are built from.

Three things differ from CSS because Pencil expresses them differently, and the
.pen is the authority:

- The zero axis is structural: a fixed-width negative half, a hairline, then a
  filling positive half. Not a percentage offset.
- `align-items: baseline` does not exist in Pencil. Plate heads use `end`.
- A row does not wrap, so a chip row stays on one line.

Inner pages carry no landscape. The cover keeps it.

## Source

`1212.pen` — frames *Brand System*, *Brand Kit*, *Assets*, *Fact Sheet ·
Monthly*, *Newsletter · Monthly*, *Internal Document · Template*, including the
three long guide notes attached to the document templates. When the .pen and
this plugin disagree, the .pen wins; update the plugin and re-run the diff.
