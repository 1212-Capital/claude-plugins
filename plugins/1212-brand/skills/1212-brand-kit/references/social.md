# 1212 Capital — social formats

Four canvases, transcribed from `1212.pen → 1212 Capital — Assets`. All live in
`assets/templates/social.html`; render with
`python3 assets/scripts/render_png.py social.html outdir`.

Corner radius 24 is a canvas convention for the preview. Export flat if the
platform crops or applies its own mask.

## Announcement — 16:9, 1920 × 1080

Launches, positioning, news.

- Full-bleed brand image plus a two-layer scrim:
  `linear-gradient(0deg,#0E122000 44%,#0E122099 100%)` over
  `linear-gradient(180deg,#0E122000 38%,#0E1220E8 100%)`
- Top bar, padding 55 / 65: logo Lora 23/600 (`1212` paper, `CAPITAL` lavender) on
  the left, eyebrow mono 16 ls 2 lavender on the right
- Bottom, padding 0 / 65 / 62, column gap 22:
  headline Lora 96/500 lh 94 paper, width 1440, line break authored by hand;
  subline Inter 23 lh 35 `#E7D8C6`, width 912

## Stat · Light — 16:9, 1920 × 1080

Metric callout on light surfaces.

- Left panel 1080 × 1080, ivory, padding 113 / 96, space-between:
  label mono 19 ls 2 lavender · value Lora 180/500 lh 180 ink ·
  footer row: logo Lora 20/600 ‖ CTA mono 18 ls 1 ink-soft
- Right: brand image, 840 wide, full bleed
- The source file uses `accent-blue` for the label. Use `lavender`.

## Split Block · Dusk — 16:9, 1920 × 1080

Editorial statement on dark.

- Dusk canvas. Image band on top, full width, height 595, with
  `linear-gradient(180deg,#181228A8 0%,#18122800 34%)` over it
- Logo absolutely placed at 77 / 77 inside the image, Lora 33/600,
  `1212` `#FBF8EF`, `CAPITAL` `#D8D2E6`
- Block below, padding 0 / 77 / 77, space-between, bottom aligned:
  headline Lora 102/400 lh 104 `#FBF8EF` width 883 ‖
  body Inter 27 lh 41 `#C8C3D6` width 691

## Stat — 1:1, 1080 × 1080

Single metric, square placements.

- Brand image plus scrim:
  `linear-gradient(0deg,#0E122000 60%,#0E1220A6 100%)` over
  `linear-gradient(180deg,#0E122000 35%,#0E1220ED 100%)`
- Padding 43 / 43 / 48. Top: logo Lora 20/600 ‖ eyebrow mono 13 ls 2 lavender
- Stat block, column gap 9: label mono 13 ls 2 `#E7D8C6` ·
  figure Lora 112/500 lh 101 paper · note Inter 22 `#E7D8C6`

## 9:16, 1080 × 1920

The source file also holds 9:16 variants (Stat · Light, Stat · Dark, Repeat ·
Light, Repeat · Dark). They are the same devices at portrait proportions. Build
them from the 1:1 canvas by keeping the padding and scaling the figure; the
`.post--916` class is defined in the stylesheet.

## Rules that apply to every social asset

- One idea per canvas. A figure or a statement, not both fighting.
- Figures on social are Lora, not mono. This is the one place display type
  carries numbers, because the figure *is* the image.
- The eyebrow always names the product or the category, never the platform.
- Prefer the **midi** (noon) image set for product posts, **soir** (dusk) for
  editorial statements, **matin** (dawn) for launches.
- Recheck legibility after any image swap. The scrims are tuned per format.
