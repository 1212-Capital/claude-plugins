# 1212 Capital — tokens and component specs

Every value is transcribed from `1212.pen`. The CSS class named on each row is
implemented in `assets/css/1212.css` and renders pixel-identically to Pencil.

## Page geometry (all four documents)

| | |
|---|---|
| Page | 794 × 1123 px — true A4 at 96 dpi |
| Margins | 56 px (14.8 mm) |
| Measure | 682 px |
| Content stack max height | 988 px (fact sheet, internal doc) · 987 px (newsletter) |
| Content stack gap | 40 (FS pages 1 & 4) · 34 (FS pages 2 & 3) · 26 (newsletter) · 30 (internal doc, statement pages 1-2) · 34 (statement page 3) |
| Section label → its content | 12 px, everywhere |

Measure a stack by summing the heights of `Content`'s direct children plus the
gaps. When a page overflows: move the whole section to the next page first,
then reduce the Content gap, then split the section. Never shrink type.

## Line-height convention

Pencil stores line-height as a ratio and renders `Math.round(fontSize × ratio)`
pixels. The CSS therefore uses integer px, not ratios. When adding a new rule,
compute `round(size × ratio)` with **round-half-up** (11 × 1.5 = 16.5 → 17).

## Shared components

| Pencil component | CSS | Spec |
|---|---|---|
| `1212 · Logo` | `.logo` | row, gap 7, align end. `1212` Lora 19/600 ink · `CAPITAL` Lora 19/400 lavender, ls 1. lh 1 |
| — on a cover | `.logo.logo--cover` | size 20, `1212` ivory, `CAPITAL` #FBF8EFB3 |
| `1212 · Cover Masthead` | `.masthead` | column, gap 14. Kicker mono 11 ls 2 lilac lh 14 · Headline Lora 56/500 lh 59 ivory · Standfirst Inter 14 lh 22 #FBF8EFCC, width 540 |
| `1212 · Section Label` | `.tag` | lilac pill, r999, padding 6/14, Inter 11/500 lh 14, tint-lilac |
| `1212 · Tag` | `.pill` | periwinkle, r999, 1px lavender inner stroke, padding 5/12, Inter 11/500 lh 14, tint-periwinkle |
| `1212 · Section Heading` | `.heading` | row gap 7 align end. Main Lora 15/500 lh 18 ink · Suffix Inter 10.5 lh 16 ink-soft |
| `1212 · Stat Row` | `.statrow` | dusk, r10, padding 20/26, gap 24, space-between, align center |
| `1212 · Stat Card` | `.stat` | column gap 7. Key mono 9 ls 1.1 lh 12 lavender · Value mono 21/500 lh 23 paper |
| `1212 · Cell · Head` | `.cell.cell--head` | padding 7/11 (9/12 in the internal doc), Inter 9/600 ls 1 lh 13 ink-soft |
| `1212 · Cell · Text` | `.cell.cell--text` | Inter 10.5 lh 15 ink |
| `1212 · Cell · Figure` | `.cell.cell--fig` | mono 10.5 lh 15 ink, right aligned |
| `1212 · Cell · Figure Accent` | `.cell.cell--fig-accent` | mono 10.5/700 lh 15 ink, right aligned |
| `1212 · Page Header` / `NL ·` / `DOC ·` | `.pagehead` | column gap 13: row (logo ‖ meta mono 10.5 ls 1.2 lh 14 ink-soft) then a 1px `line` rule |
| `1212 · Page Footer` / `DOC ·` | `.pagefoot` | column gap 9: 1px rule then row, mono 9 ls .6 lh 13 ink-soft both sides |
| `NL · Page Footer` | `.pagefoot.pagefoot--nl` | same, lh 12 (the newsletter sets ratio 1.3, not 1.4) |
| `1212 · Footnote` | `.footnote` | Inter 8.5 italic lh 13 ink-soft |
| `1212 · Commentary` | `.commentary` | column gap 10. Title Lora 20/500 lh 24 ink · Body Inter 10.5 lh 17 justified ink-soft |
| `1212 · Disclaimer Paragraph` | `.disclaimer` | Inter 9.5 lh 15 justified |

## Fact-sheet blocks

| Pencil component | CSS | Spec |
|---|---|---|
| `1212 · Key Fact Row` | `.kv` | space-between, align center, gap 14. Label Inter 11 lh 17 ink-soft · Value Inter 11/600 lh 17 ink |
| `1212 · Metric Row` | `.kv.kv--metric` | same, Value mono 11.5/700 lh 17 |
| small variant (issuer block) | `.kv.kv--sm` | 10 px, lh 15 |
| `FS · Glossary Entry` | `.glossary` | column gap 4. Term Inter 10.5/700 lh 15 ink · Definition Inter 10 lh 16 justified ink-soft |
| two-column body | `.columns` | gap 30, columns 326 px. Inner gap 19 (glossary), 15 (risks), 11 (protocols), 9 (issuer) |
| `FS · Donut` | `.donut` | square, innerRadius 0.62. Segments clockwise from 12 o'clock, `sweep% = pct` |
| `FS · Legend Item` | `.legend` | gap 7, dot 10, Label Inter 11.5 lh 16 ink, Value mono 11.5/700 lh 16 ink-soft, right aligned |
| `FS · Exposure Row` | `.exposure` | gap 8, dot 12, Name Inter 11/600 width 76, **bar always lavender**, Value mono 10.5 right aligned |
| `FS · Protocol Row` | `.protocol` | gap 8, mark 12, Name Inter 11.5 lh 16 ink |
| `FS · Bar Chart` | `.barchart` | 1px bottom rule, gap 10, columns h132, bar w26 lavender, current month bar terracotta with ink labels |
| `FS · Table` | `.table` | paper, r10, clipped. Rows separated by a 1px inner bottom `line`; last row none. Highlight row `lilac` |

**Donut maths.** `sweepAngle = pct × 3.6`, clockwise, each segment starting
where the previous ended. In CSS this is a `conic-gradient` with cumulative
percentage stops. Disable unused segments, do not delete them.

**Exposure bar maths.** `bar width = pct ÷ max_pct × 420`. The value cell is
`flex:1 1 auto; text-align:right` so it holds a clean column. All bars are
lavender — only the dot carries the ramp colour.

## Newsletter blocks

| Pencil component | CSS | Spec |
|---|---|---|
| `NL · Article Title` | `.nl-title` | column gap 11: section tag, then headline |
| `NL · Headline` | `.nl-headline` | Lora 40/500 lh 43 ink |
| `NL · Body Text` | `.nl-body` | Inter 12.5 lh 19 justified ink-soft |
| `NL · Body Columns` | `.nl-cols` | 2 × 328, gutter 26 |
| `NL · Image` (hero) | `.nl-hero` | r10, cover. Height 320 / 286 / 262 depending on headline length |
| `NL · Coverline` | `.nl-coverline` | 210 wide, column gap 8. Topic mono 10 ls 1.6 lh 13 lavender · Head Lora 15/400 lh 19 ivory |
| `NL · Coverline Row` | `.nl-coverlines` | 3 × 210, gap 26 |
| `NL · Brief` | `.brief` | row gap 24. Image 200 × 126 r10 · Kicker mono 10 ls 1.6 lh 13 ink-soft · Headline Lora 21/500 lh 24 ink · Body Inter 11.5 lh 18 justified ink-soft · then its own source |
| `NL · Source` | `.nl-source` | mono 9 ls 1.4 lh 12 ink-soft, full width |
| article stack | `.nl-article` | column gap 11: body columns, then the source |
| two briefs | `.briefs` | column gap 24 |

## Internal-document blocks

| Pencil component | CSS | Spec |
|---|---|---|
| `DOC · Body` | `.doc-body` | Inter 10.5 lh 17 ink, **not** justified |
| `DOC · Bullet` | `.bullet` | row gap 10. Marker 10 wide, padding-top 7, dot 4 lavender. Term Inter 10.5/700 lh 16 ink · Text Inter 10.5 lh 16 ink-soft, column gap 3 |
| `DOC · Meta Item` | `.metaitem` | row gap 6. Label Inter 9.5/700 lh 13 ink · Value Inter 9.5 lh 13 ink-soft |
| `DOC · Table` | `.table` with `.cell--pad9` | 3 columns 200 / 90 / fill, cells padding 9/12, heads left aligned |
| cover meta strip | `.coverstrip.coverstrip--meta` | 4 columns gap 28. Label mono 8.5 ls 1.1 lh 11 #FBF8EF99 · Value mono 13/500 lh 16 ivory |

## Cover figure strip (fact sheet)

`.coverstrip` — 4 columns gap 28, column gap 7. Label mono 8.5 ls 1.1 lh 11
`#FBF8EF99`, Value mono 20/700 lh 22 ivory.

## Known inconsistency in the source file

`Assets → Stat · Light` sets its label in `accent-blue #6E6796`, which the
document rules list as not-a-brand-colour. The CSS ships `lavender` instead.
Worth fixing in the .pen so the two agree.


## Client statement

Introduces no component of its own. Size variants only:

| Block | CSS | Spec |
|---|---|---|
| cover meta strip | `.coverstrip.coverstrip--sm` | value mono 12/500 lh 15 ivory |
| legal paragraph | `.disclaimer.disclaimer--soft` | Inter 10 lh 16 justified ink-soft |
| two columns | `.cols327` | gap 28, columns 327 px |
| tables | `.table` + `.cell--pad9` | numeric columns use `.cell--fig` (mono), dates and labels `.cell--text` (Inter), headers `.cell--head` take their column's alignment |

Positions columns: Strategy fill / Units 110 / NAV 110 / Value 130 / Weight 90.
Movements: Date 110 / Type 170 / Strategy fill / Amount 150.
Fees: Item fill / Basis 220 / This period 150.

## Data plates, extension

Not in the .pen. Mirror before treating as system.

| Block | CSS | Spec |
|---|---|---|
| plate | `.plate` | paper r10, padding 24, column gap 16, height set to the hero it replaces |
| dark plate | `.plate.plate--dusk` | dusk, label in lavender |
| plate header | `.plate__label` / `.plate__source` | mono 10 ls 1.6 / mono 9 ls .6 |
| zero-axis bar | `.hbar` | name 104, track fills, value 66 right. Positive lavender, negative terracotta |
| big figure | `.plate__big` | Lora 76/500 lh 76 paper |
| composition | `.stackbar` | height 44, r6, segments in ramp order, `.plate__legend` below |
| entity chip | `.chip` | paper, 1px line, r999, padding 5/12, Inter 10.5/600 |
