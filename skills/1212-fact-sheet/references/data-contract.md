# Fact sheet — JSON data contract

Input for `assets/scripts/build_factsheet.py`. A working example ships at
`assets/schemas/factsheet.example.json`; defaults for the static pages at
`assets/schemas/factsheet.defaults.json`. Any key absent from your file falls
back to the defaults.

## Required each month

| Key | Type | Notes |
|---|---|---|
| `as_of` | string | `"30 June 2026"`. Appears on the cover, in all four running heads (upper-cased automatically) and in the notice. |
| `issue` | string | `"FACT SHEET · JUN 2026"` |
| `product.name` | string | `"1212.Stable"` |
| `product.kicker` | string | Sentence case, e.g. `"Stable Digital Asset Fund"` |
| `product.standfirst` | string | 2 to 3 lines. Wraps at 540 px. |
| `headline` | 4 × `{label, value}` | Cover strip. Labels UPPERCASE. |
| `description` | string | Fund description, justified, ~5 lines at 408 px. |
| `key_facts` | list of `[label, value]` | 5 rows fits the block cleanly. |
| `performance` | list of `[label, value]` | Values render in mono bold. |
| `terms` | list of `[label, value]` | 4 rows. |
| `yield_environment.header` | `[string, string]` | Left column, right column. |
| `yield_environment.rows` | list of `{label, value, highlight?}` | `highlight: true` puts the row on lilac with the accent figure. Exactly one row should be highlighted, and it is always 1212.Stable. |
| `yield_environment.source` | string | |
| `risk_metrics.items` | 4 × `[key, value]` | Dusk stat band. `[TBD]` is a valid value. |
| `risk_metrics.source` | string | |
| `allocation.segments` | list of `{label, pct, color?}` | Donut plus legend. Percentages, not fractions. Colours default to the ramp in order. |
| `allocation.note` | string | |
| `allocation.heading` / `.suffix` | string | Default `"Strategy Allocation"` / `"% of NAV"`. |
| `stablecoins` | list of `{name, pct, color?}` | Bar width is computed as `pct ÷ max_pct × 420`. Values print with two decimals. |
| `protocols` | list of string | Split into two columns automatically; marks follow the ramp. |
| `allocation_source` | string | |
| `monthly_returns.months` | list of string | `"Jan 2026"`. Column count is free. |
| `monthly_returns.fund` | list of string | Same length as `months`. Pre-formatted, e.g. `"1.24%"`. |
| `monthly_returns.btc` | list of string | Same length. |
| `monthly_returns.source` | string | |

## Optional, defaults supplied

| Key | Type | Notes |
|---|---|---|
| `cover_image` | string | Path under `assets/img/`, default `"midi/opt-02.jpg"`. |
| `glossary` | list of `{term, def}` | 10 entries, split into two columns. |
| `risks` | list of `{term, def}` | 7 entries. |
| `legal` | list of string | 7 paragraphs. |
| `issuer` | list of `[label, value]` | 6 rows, split into two columns. |
| `css` / `cover_image_base` | string | Overridden automatically with absolute paths; set only if relocating assets. |

## Formatting conventions

- Values are **pre-formatted strings**, not numbers, except `pct` fields which
  are numeric so the geometry can be computed. This keeps sign, decimals and
  the `%` under the author's control.
- Percentages carry two decimals on this document.
- Negative returns use a hyphen-minus, not an en dash: `"-10.20%"`.
- Dates: `DD MMMM YYYY` in prose, `DD/MM/YYYY` in Key Facts, `MMM YYYY` in
  month columns.
- No em dashes in any string.

## Where the numbers come from

Named in the shipped source lines, so keep them accurate:

- **Lagoon** — 1212.Stable NAV, performance, allocation
- **on-chain positions** — stablecoin and protocol exposure
- **iShares** — comparator ETF SEC yields
- **Kraken** — USDC reference rate
- **coinglass** — BTC monthly returns and correlation

NAV is struck weekly; monthly returns derive from the last published NAV of
each month. If a figure cannot be traced to one of these, do not publish it.

## Sanity checks the builder does not run

- Allocation segments sum to 100 (or the rounding note is present).
- `monthly_returns` lists are the same length.
- Exactly one highlighted row in the yield table.
- The as-of date is consistent everywhere.
