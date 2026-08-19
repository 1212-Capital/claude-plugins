---
name: 1212-fact-sheet
description: >
  This skill should be used when producing or updating a 1212 Capital product
  fact sheet: "the fact sheet", "1212.Stable fact sheet", "monthly fact sheet",
  "factsheet for June", "update the fact sheet with this month's numbers",
  "fiche produit", or when asked to turn NAV / allocation / performance data
  into the investor-facing PDF. Covers both the Pencil build and the
  self-contained HTML to PDF build.
metadata:
  version: "1.0.0"
  source: "1212.pen — Fact Sheet · Monthly"
---

# 1212.Stable — monthly fact sheet

Cover + 4 numbered pages, 794 × 1123 (true A4 at 96 dpi), 56 px margins, 682 px
measure. Read `1212-brand-kit` first if the palette and type rules are not
already loaded.

## Intake, before anything else

1212 runs **more than one fund** and they are not alike. Producing the wrong
wording for the wrong fund is the one failure this skill exists to prevent.

**First, read the funds.** `assets/schemas/funds.json` holds every known vault
with its Lagoon address. Fetch each one with WebFetch at
`https://app.lagoon.finance/vault/{chain}/{address}` so the options you show
carry today's strategy line and TVL rather than a memory. The GraphQL API at
`https://api.lagoon.finance/query` is open and needs no key, and returns richer
data (`vaultByAddress`, `stateAt`, `stateHistory`); use it if the environment
can reach it, and fall back to the vault page if it cannot.

**Then ask, one round:**

| Question | Options |
|---|---|
| Which fund? | **1212.Stable** (non-directional, stablecoins) · **1212.Alpha** (systematic directional) · **another** |
| Which period? | month ending *last completed month end*, pre-selected · another range |
| Cover image? | dawn · noon · dusk · pick for me |
| Where do the figures come from? | I will paste the NAV pack · pull what you can from Lagoon and flag the gaps |

If the answer to the first is **another**, ask for the Lagoon vault address,
read it, and add the fund to `funds.json` with its own `copy` block before
building. Never reuse another fund's description.

## The wording follows the fund

`funds.json` carries, per fund: kicker, standfirst, description, key facts,
asset class, the label and headers of the comparison table, the allocation
heading, the glossary and the risk considerations. Pass `"fund": "stable"` or
`"fund": "alpha"` in the JSON and the builder loads the right ones.

This matters because the two products are opposites. 1212.Stable eliminates
directional exposure and its risk pages talk about depeg and protocol failure.
1212.Alpha **takes** directional exposure, so its pages have to lead with market
risk and drawdown, its comparison table shows benchmarks rather than yields, and
its glossary defines signals and model risk. Pasting Stable's copy onto Alpha
would not be incomplete, it would be false.

## Decide the route

- **Pencil** when the Pencil app is open on `1212.pen` and an editable design
  file is wanted. Duplicate the page set, override text on the instances, export
  a PDF. Recipe: `1212-brand-kit/references/pencil.md`.
- **HTML → PDF** otherwise, or whenever the job is "same document, new numbers".
  This is the default for a monthly refresh.

## The monthly refresh, HTML route

1. Collect the month's figures into a JSON file. Start from
   `${CLAUDE_PLUGIN_ROOT}/assets/schemas/factsheet.example.json` and overwrite
   the values. The full contract is in `references/data-contract.md`.
2. Build and render:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/build_factsheet.py \
        june.json out/factsheet-2026-06.html \
        --pdf out/1212.Stable-Factsheet-June-2026.pdf
```

3. Review the PNGs before delivering:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/render_pdf.py \
        out/factsheet-2026-06.html /dev/null --png out/review
```

Pages 3 and 4 (glossary, risk considerations, important information) come from
`assets/schemas/factsheet.defaults.json` and stay identical month to month.
Override them in the JSON only when the education or legal copy actually
changes.

For a one-off variant the builder does not cover, start from the template and
edit the markup directly. The classes are documented in
`1212-brand-kit/references/tokens.md`.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/new_doc.py factsheet variant.html
```

## What goes on each page

**Cover.** Full-bleed brand image (default `midi/opt-02.jpg`) under the 5-stop
scrim. Logo top left, `FACT SHEET · MMM YYYY` top right. Then kicker, product
name in Lora 56, standfirst, a hairline, four headline figures, and the
confidentiality notice.

**Page 1 — Overview & Performance.** Two aligned rows: Fund Description (408) ‖
Key Facts (246), then Net Performance (408) ‖ Terms (246). The rows exist so the
second pair starts on the same baseline; do not collapse them into two vertical
columns. Then Current Yield Environment (table, 1212.Stable on the lilac row
with the accent figure) and Risk Metrics (dusk stat band). Content gap 40.

**Page 2 — Allocation & Monthly Returns.** Strategy Allocation (donut 210 +
legend + note), Stablecoins Exposure (bars), Protocols Exposure (two columns),
source footnote, Monthly Returns vs BTC. Content gap 34.

**Page 3 — Glossary & Risk Considerations.** Investor education, static. 10
glossary entries and 7 risk considerations, two columns each.

**Page 4 — Important Information.** 7 legal paragraphs then Issuer & Contact.
No panel, no tinted box. Content gap 40.

## Rules that are specific to this document

- **Figures.** IBM Plex Mono everywhere. Two decimals for percentages.
  Right-align every figure column and its header.
- **Donut.** `sweepAngle = pct × 3.6`, clockwise from 12 o'clock, segments in
  ramp order lavender → gold-sun → terracotta → periwinkle → amber. Never more
  than five segments; group the tail into "Other".
- **Exposure bars.** Width = `pct ÷ max_pct × 420`. Bars are always lavender.
  Only the dot carries the ramp colour.
- **Monthly returns.** Column count is free. Six months is the house default.
- **Placeholders.** The shipped template carries `XX.XX%`, `DD MMMM YYYY`,
  `MMM YYYY`, `FS-YYYY-MM · vN`. Replace values, never reflow the layout around
  them.
- **[TBD] is a real state.** Max drawdown and Sharpe ratio ship as `[TBD]` until
  computed from the weekly NAV series, and Sharpe additionally needs a stated
  risk-free rate. Do not invent them.
- **Issuer block.** Bracketed placeholders are deliberate. Fill them only from
  something authoritative, and flag that counsel should confirm before any
  distribution.
- Every table and chart carries a named source and an as-of date beneath it.

## Overflow

Keep each Content stack under 988 px. Measure by summing the heights of
Content's direct children plus the gaps. When a page overflows, in this order:
move the whole section to the next page, reduce the Content gap, split the
section. Pages 3 and 4 take no data blocks. Never shrink type.

## Before delivering

1. Every figure traces to a source named in the document.
2. Percentages that should sum do, or the rounding note is present.
3. The as-of date is identical on the cover, all four running heads, and every
   source line.
4. Page numbers read `1 / 4` … `4 / 4`.
5. Document version bumped (`FS-YYYY-MM · vN`).
6. No em dash anywhere.
7. `check_pdf.py` passes on the exported PDF, and the cover has been
   eyeballed in an actual viewer, not only in the render PNGs.

## References

- `references/data-contract.md` — the JSON schema, field by field
- `1212-brand-kit/references/tokens.md` — CSS classes and component specs
- `1212-brand-kit/references/pencil.md` — the Pencil build
