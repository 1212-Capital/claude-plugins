---
name: 1212-brand-kit
description: >
  This skill should be used for anything involving 1212 Capital's visual identity:
  "1212 brand", "brand kit", "brand guidelines", "what are our colours",
  "which font", "make this on-brand", "a social post for 1212", "an Instagram /
  LinkedIn / X visual", "a cover image", or when checking whether a design,
  deck, page or document follows the 1212 Capital brand. It is also the shared
  foundation loaded by the 1212 fact sheet, newsletter, internal document and
  client statement skills.
metadata:
  version: "1.0.0"
  source: "1212.pen — Brand System, Brand Kit, Assets"
---

# 1212 Capital — brand kit

The single source of truth is `1212.pen` (Pencil), frames *Brand System*,
*Brand Kit* and *Assets*. Everything below is transcribed from it. Treat these
as rules, not preferences. When a request conflicts with a rule, say so and
propose an on-brand alternative rather than silently deviating.

## Start with intake

Never produce one of these documents from a bare request. Ask first, in **one
round**, with `AskUserQuestion`, four questions maximum, defaults already
selected. Three rules keep it short:

- **Look up rather than ask.** Anything readable from a source, read it and put
  the answer in the options rather than making the operator recall it.
- **Default rather than ask.** A period, a month, an issue number: propose the
  obvious value pre-selected instead of asking for a date.
- **One round.** If producing a document costs six questions, people stop using
  it. Anything still missing after the round, infer it and say what you assumed.

If the session is unattended, a scheduled run or a batch, do not block. Take the
defaults, produce the document, and state every assumption at the top of your
reply.

### The cover image

**Documents do not get a cover question.** Each document type has one fixed
cover, listed in `assets/img/catalogue.json` under `rules.covers`: fact sheet
`midi/opt-02`, newsletter `midi/opt-01`, internal document `midi/opt-06`,
client statement `matin/opt-03`. A client who receives the same document every
month should recognise it; varying the cover made each issue look like a
different publication. Change it only if asked, and say which image you used.

**Social assets still get the question**, because each post is a one-off. Ask
dawn, noon, dusk, or pick for me, then apply the catalogue's rules: no figures
on anything that reads as a document, and recheck the scrim after a swap.

## The brand in one paragraph

1212 Capital is a crypto-native family office. The identity is warm and
editorial, not fintech-cold: painterly golden-hour landscapes, a serif voice,
and a calm palette that stays clear while the market is loud. Positioning line:
**"Anchored in traditional finance. Fluent in digital asset markets."**
Signature line: **"Clarity, compounded, since 2022."**

## Non-negotiables

- **Palette only.** ivory · paper · sand · ink · ink-soft · line · terracotta ·
  lavender · lilac · periwinkle · amber · gold-sun · dusk · mint · peach.
  `vermilion`, `teal`, `accent-blue` and `paper-2` still exist as variables in
  the .pen file but are **not** brand colours. Never reintroduce them.
- **Surfaces.** Page background is `ivory`. Cards, tables and tiles sit on
  `paper`. Data bands are `dusk`. `sand` is for working surfaces only (the
  block libraries), never a published page.
- **Type roles.** Lora = display only, weight 500 (600 only in the logotype).
  Inter = body and UI. IBM Plex Mono = labels and every figure. A number set in
  Lora or Inter inside a document is a bug.
- **Radii.** 999 for tags and pills. 10 for every surface (cards, tables,
  tiles, data bands). 24 for social canvases. 6 for buttons. 0 for everything
  else.
- **Rules.** Every hairline in a document is `line` (#D9D2C3), 1px. No black
  rules, no heavier weights.
- **Warm accents are reserved.** amber, gold-sun and terracotta belong to data
  and highlights. They do not decorate.
- **No em dashes in anything a reader receives.** Document copy, headings,
  captions, social text, and the `<title>` that lands in the PDF metadata:
  use a period, a comma, or a middle dot. This is checked by grepping the
  templates, the builders and the CSS. Prose inside these skill files is
  instruction for Claude, not copy, and is out of scope.
- **Data ramp, always in this order:** lavender → gold-sun → terracotta →
  periwinkle → amber. Donut segments, exposure dots, protocol marks and legends
  all draw from it.
- **On an inner page, an image must carry information.** The painterly
  landscapes are the cover's job. Inside a document the hero slot takes a data
  plate, and a brief names its subject with `.chip` rather than a decorative
  thumbnail. Never lift a photograph from a source article: press images are
  licensed, and reuse in a distributed document is a reproduction, not a
  citation.

## Colour

| Token | Hex | Role |
|---|---|---|
| `ivory` | `#FBF8EF` | page background, light panels |
| `paper` | `#F2EEE4` | cards, tables, tiles |
| `sand` | `#F2E8D5` | working surfaces only |
| `ink` | `#1C1A17` | primary text |
| `ink-soft` | `#6F685C` | secondary text, labels |
| `line` | `#D9D2C3` | every rule and hairline |
| `accent` (terracotta) | `#B05A3C` | data, highlight |
| `lavender` | `#9B94C7` | wordmark "CAPITAL", primary data colour |
| `lilac` | `#D8D2E6` | section tag background, highlighted table row |
| `periwinkle` | `#CDD6EC` | pill background, data |
| `amber` | `#EBA23A` | data |
| `gold-sun` | `#F2CE97` | data |
| `dusk` | `#262233` | data bands, dark surfaces |
| `mint` | `#D6EACF` | pastel tag |
| `peach` | `#F3DAC8` | pastel tag |

Text on pastels uses the matching tint, never `ink`: `tint-lilac #4A4370`,
`tint-mint #2E4A2A`, `tint-peach #6E3B26`, `tint-periwinkle #3A4166`.

## Type

| Family | Role | Where |
|---|---|---|
| **Lora** | display, headlines, figures on social | headlines, cover masthead, section headings, logotype |
| **Inter** | text, UI | body copy, labels, table text, buttons |
| **IBM Plex Mono** | labels and data | eyebrows, meta lines, every figure in a document |

All three are free on Google Fonts. Offline copies ship in
`${CLAUDE_PLUGIN_ROOT}/assets/fonts/`.

## Logotype

`1212` in Lora 600 + `CAPITAL` in Lora 400 with `letter-spacing: 1px`, bottom
aligned, gap 7 (gap 8-9 at larger sizes). `1212` takes `ink` on light and
`ivory`/`paper` on dark; `CAPITAL` is always `lavender` (or `lilac` at large
display sizes on dark). Give it room to breathe. Never redraw or restyle it.

## Imagery

18 painterly golden-hour landscapes in three sets, shipped in
`${CLAUDE_PLUGIN_ROOT}/assets/img/`:

- `matin/opt-01…06.jpg` — Dawn, 06:00
- `midi/opt-01…06.jpg` — Noon, 12:12
- `soir/opt-01…06.jpg` — Dusk, 18:00

The light tells the time. Documents use them **on the cover**; the fact sheet
defaults to `midi/opt-02`, the newsletter to `midi/opt-01`, the internal
document to `midi/opt-06` and the client statement to `matin/opt-03`. Every
full-bleed image carries a scrim so light type stays legible; the document
scrim is a 5-stop gradient, `linear-gradient(180deg, #201C2B8C 0%, #201C2B1A
24%, #201C2B26 44%, #201C2BD9 72%, #201C2BFC 100%)`. Recheck contrast whenever
the image changes. Never generate a new brand image without being asked; use
the library.

## Two ways to produce a 1212 artefact

**A. Pencil** — highest fidelity, stays editable, requires the Pencil app open
on `1212.pen`. Duplicate an existing page set and override text on the
instances. Never detach an instance. Component IDs and the full build recipe are
in `references/pencil.md`.

**B. Self-contained HTML → PDF/PNG** — works anywhere, no Pencil needed:

```bash
S=${CLAUDE_PLUGIN_ROOT}/assets/scripts
python3 $S/new_doc.py factsheet|newsletter|internal-doc|social  work.html
# edit work.html
python3 $S/render_pdf.py work.html out.pdf --png review   # A4 pages
python3 $S/render_png.py work.html outdir                 # social canvases
python3 $S/check_pdf.py out.pdf                           # colour sanity, always
```

**The magenta trap.** Chromium embeds JPEGs byte for byte but tags the stream
`/ColorTransform 0`, meaning "these three components are already RGB". They are
YCbCr. Lenient PDF readers ignore the flag, strict ones honour it and every
brand photograph renders bright pink. `render_pdf.py` repairs the flag after
writing the file; `check_pdf.py` verifies it. A PDF that looks right in one
viewer can still be broken in another, so never sign off on a single preview.

The stylesheet `${CLAUDE_PLUGIN_ROOT}/assets/css/1212.css` is verified
pixel-identical to the Pencil rendering. Do not invent CSS values; every number
in that file exists in the .pen. Always start from a template via `new_doc.py`
rather than writing markup from scratch. Requires Python with Playwright and a
Chromium build; no network is needed, the fonts and images ship with the plugin.

## Social formats

**Ask before building one.** Nothing in a social asset is fixed: the headline,
the figure, the label, the eyebrow and the call to action are all content, and
the image is a choice. One round, three questions: which format, what the post
has to say (the claim and the figure behind it), and the image mood. Do not
invent a percentage to fill the slot; if the figure is not supplied, ask for it
or use a format that does not need one.

Four canvases, all in `assets/templates/social.html`, exact specs in
`references/social.md`:

| Format | Size | Use |
|---|---|---|
| Announcement | 1920×1080 | launches, positioning, news |
| Stat · Light | 1920×1080 | metric callout on light surfaces |
| Split Block · Dusk | 1920×1080 | editorial statement on dark |
| Stat | 1080×1080 | single metric, square placements |

## Data plates, for inner pages

| Block | CSS | Use |
|---|---|---|
| Comparison | `.plate` + `.hbar` | several series around a zero axis, lavender positive, terracotta negative |
| Single figure | `.plate.plate--dusk` + `.plate__big` | one number carries the page |
| Composition | `.plate` + `.stackbar` | market share or allocation, ramp order, legend below |
| Entities | `.chips` + `.chip` | the companies and protocols a story names |

Every plate carries a `.plate__label` naming what is measured and a
`.plate__source` naming where it came from.

## Before delivering anything

1. Every colour is in the palette table above.
2. Every figure is IBM Plex Mono; no headline is set in Inter.
3. Radii are 999 / 10 / 24 / 6 / 0 and nothing else.
4. No em dash in the copy.
5. Contrast holds on any scrimmed image.

## What you need to run this

The HTML route needs Python with **Playwright** and a **Chromium** build. That
is all: the fonts and the 18 images ship inside the plugin, so nothing is
fetched at render time and it works offline.

```bash
pip install playwright && playwright install chromium
```

Everything else is optional and nobody needs it to produce a document. The
Pencil app and its MCP server matter only to whoever maintains the design file.
The Lagoon lookups in the fact sheet skill use WebFetch, and degrade to asking
the operator for the figures if the network refuses. If a script reports a
missing dependency, say so plainly rather than working around it.

## References

- `references/tokens.md` — every token, component spec and CSS class
- `references/voice.md` — positioning, tone, approved copy lines
- `references/social.md` — the four social canvases, exact geometry
- `references/pencil.md` — Pencil component IDs and how to build in the .pen (optional route)
- `../../assets/img/catalogue.json` — the 18 landscapes, with scene, figures and per-document rules
- `../../assets/schemas/funds.json` — the 1212 vaults and the wording each one takes
