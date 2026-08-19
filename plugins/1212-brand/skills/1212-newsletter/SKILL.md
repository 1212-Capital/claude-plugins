---
name: 1212-newsletter
description: >
  This skill should be used when producing a 1212 Capital monthly newsletter or
  market report: "the newsletter", "monthly newsletter", "monthly report",
  "newsletter for July", "write up this month's market roundup", "la
  newsletter", or when turning market news into the branded A4 PDF. Covers both
  the Pencil build and the self-contained HTML to PDF build.
metadata:
  version: "1.0.0"
  source: "1212.pen — Newsletter · Monthly"
---

# 1212 Capital — monthly newsletter

Cover + 3 section pages, 794 × 1123 (true A4 at 96 dpi), 56 px margins, 682 px
measure. Same geometry as the fact sheet, so the two documents read as one
system. Read `1212-brand-kit` first if the palette and type rules are not
already loaded.

## Intake, before anything else

One round, four questions, defaults pre-selected:

| Question | Options |
|---|---|
| Which month? | *last completed month*, pre-selected · another |
| Where does the material come from? | I will paste the article links · search for them · both |
| How many section pages? | 3 · 4 · 5 (cover excluded) |
| Cover image? | dawn · noon · dusk · pick for me |

If links are supplied, read each one and credit that publication on the block
that uses it. If not, search, and tell the operator which publications you
settled on before writing. Ask for the issue number only if it cannot be
inferred from the previous issue.

## Build

**HTML route (default).** Start from the template, replace the lorem copy, then
render:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/new_doc.py newsletter newsletter-2026-07.html
# edit newsletter-2026-07.html
python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/render_pdf.py \
        newsletter-2026-07.html 1212-Capital-Newsletter-July-2026.pdf --png review
```

`new_doc.py` rewrites the stylesheet and image references to absolute paths
inside the plugin, so the copy renders from any directory.

**Pencil route.** Duplicate `Ggi9M` (the Pages frame) and override the text on
the instances. Never detach an instance. See
`1212-brand-kit/references/pencil.md`.

## Page anatomy

**Cover, unnumbered.** Full-bleed brand image (default `midi/opt-01.jpg`) under
the 5-stop scrim. Logo top left, `MMM YYYY · Nº XX` top right. Bottom: kicker
(UPPERCASE mono, ls 2), headline in Lora 56, standfirst, a hairline, then three
coverlines under "In This Issue", one per section page.

**Section pages 02 · 03 · 04.** Each runs the same stack, content gap **26**:

```
Page Header → Article Title (lilac tag + Lora 40 headline)
            → Hero block → Article (2 × 328 gutter 26, then its source line)
            → optional dusk data band → one or two Briefs → Page Footer
```

**Sources sit with the block they belong to, not in the footer.** Every article
carries a `.nl-source` line under its body columns, inside a `.nl-article`
stack with an 11 px gap, and every brief carries one under its own body. The
footer's right slot holds the page number alone. A page with two stories from
two publications therefore credits both correctly.

- **The hero slot carries information, not scenery.** Default to a data plate:
  `.plate` with horizontal bars around a zero axis for a comparison, `.plate
  --dusk` with one large figure when a single number is the story, or a
  `.stackbar` for a composition. Photography in this slot is the exception, not
  the default. See the imagery rule in `1212-brand-kit`.
- **Hero height is the tuning knob.** 320 px when the headline holds on one
  line, 286 or 262 when it wraps to two. A plate takes the same heights.
- **Body columns** are 328 px each. Keep them roughly even; the layout will not
  balance them for you. Aim for ±1 line.
- **Data band** (Market Snapshot, Partners Band) is an instance of the shared
  dusk stat row, four keys, space-between. Use it when the story carries
  figures. Drop it when it doesn't and give the space to a second brief.
- **Briefs**: kicker, headline, body, source. Use `.brief--wide` with a row of
  `.chip` naming the companies and protocols in the story instead of a
  decorative thumbnail. Two briefs stack with a 24 px gap.

## Editorial rules

- **One lead per page, then briefs.** The lilac tag plus a Lora headline marks
  the page's lead story. Briefs use a plain mono kicker in ink-soft, then a
  smaller Lora headline, so the tag stays the page-level marker.
- **No horizontal rules between blocks.** The only two rules in the document
  are under the page header and above the footer.
- Section numbering (`01 ·`, `02 ·`, `03 ·`) and the footer page number are
  manual. Renumber both if you add, drop or reorder a page.
- The footer's right slot names the source, e.g. `SOURCE · CRYPTOAST  ·  03`.
  Name the actual source used.
- Headlines are sentence case. Figures inside body copy are Inter; figures in
  the data band are mono.
- **The brand landscapes belong on the cover.** On an inner page an image has
  to earn its space by carrying information. Prefer the **midi** (noon) set for
  the cover; never repeat the cover image inside.
- No em dashes.

## Rebalancing

The three section pages are interchangeable. Every block is a self-contained
frame built only from library components with nothing positioned by hand, so a
block dragged to another page re-flows on its own and takes that page's 682 px
measure.

Keep each Content stack under 987 px. Measure by summing the heights of
Content's direct children plus the gaps. When a page overflows, in this order:
shorten the hero image, move a brief to the next page, reduce the Content gap,
split the story across two pages.

## A typical month

1. Agree the three section themes with the desk. One theme per page.
2. Write the cover: kicker, headline, standfirst, three coverlines that each
   point at one section page.
3. Per page: lead story (headline + 2 columns), then either a data band plus
   one brief, or two briefs.
4. Pick the cover image, then build one data plate per section page from that
   page's own figures.
5. Render, review the PNGs, check every stack fits, then export the PDF.

## Before delivering

1. Issue line (`MMM YYYY · Nº XX`) identical on the cover and all three running
   heads.
2. Coverlines match the actual section pages, in order.
3. Section numbers and page numbers are sequential.
4. Every figure in a data band or a plate has a source, on the block itself.
5. Body columns are visually even; no orphan line at the foot of a column.
6. No em dash, no lorem text left anywhere.
7. `check_pdf.py` passes on the exported PDF, and the cover has been
   eyeballed in an actual viewer, not only in the render PNGs.

## References

- `1212-brand-kit/references/tokens.md` — CSS classes and component specs
- `1212-brand-kit/references/voice.md` — tone and approved lines
- `1212-brand-kit/references/pencil.md` — the Pencil build
