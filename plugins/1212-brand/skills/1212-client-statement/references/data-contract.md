# Client statement — JSON data contract

Input for `assets/scripts/build_statement.py`. A working example ships at
`assets/schemas/statement.example.json`; the legal paragraphs, contact rows and
table notes at `assets/schemas/statement.defaults.json`. Any key absent from
your file falls back to the defaults.

## Per account, every period

| Key | Type | Notes |
|---|---|---|
| `period` | string | `"1 – 31 July 2026"`. Shown on the cover. |
| `as_of` | string | `"31 Jul 2026"`. Upper-cased into the running head. |
| `reference` | string | `"CS-2026-07"`. The account number is appended automatically. |
| `client.name` | string | Appears as the cover headline and in the running head. |
| `client.account` | string | `"0000-0000"` |
| `client.type` | string | Individual, Trust, Company … |
| `client.opened` | string | `DD/MM/YYYY` |
| `client.manager` | string | Name, role |
| `headline` | 4 × `{label, value}` | Portfolio value, net contributions, gain/loss, return. |
| `performance` | list of `[label, value]` | Five rows, the last being `Fund, same period`. |
| `positions` | list of `{strategy, units, nav, value, weight}` | Cash carries `—` for units and NAV. |
| `movements` | list of `{date, type, strategy, amount}` | Grows freely. |
| `fees` | list of `{item, basis, amount}` | Last row is the total, with an empty basis. |
| `commentary.title` | string | One sentence, Lora. |
| `commentary.body` | list of string | One or two paragraphs. |

## Optional, defaults supplied

| Key | Type | Notes |
|---|---|---|
| `currency` | string | Default `"USD"`. |
| `cover_image` | string | Path under `assets/img/`, default `"matin/opt-03.jpg"`. |
| `legal` | list of string | Five paragraphs. |
| `contact` | list of `[label, value]` | Six rows. `Statement reference` is overwritten with `reference · account`. |
| `positions_note` / `movements_note` | string | The italic line under each table. |

## Batch shape

```json
{
  "common": { "period": "1 – 31 July 2026", "as_of": "31 Jul 2026", "reference": "CS-2026-07" },
  "accounts": [ { "client": {...}, "headline": [...], ... }, { ... } ]
}
```

`common` is merged under each account, so anything an account restates wins.
Output files are named `<reference>-<account>.html` / `.pdf`.

## Formatting conventions

- Values are **pre-formatted strings**. The builder does no arithmetic and no
  rounding, deliberately: the numbers must come from the book of record, not
  from a template engine.
- Thousands separated with a comma, no currency symbol inside the tables. The
  currency is stated once, on the cover and in the Account block.
- Gains and subscriptions carry `+`. Redemptions and fees carry `−` (U+2212).
- An empty cell is `—`.
- Percentages carry two decimals.
- Dates: `DD/MM/YYYY` in tables, `DD MMM YYYY` in the running head, and a
  spelled range on the cover.

## Checks the builder does not run

- Positions value column sums to the portfolio value.
- Net contributions plus gain equals portfolio value.
- Fee lines in the movements table equal the fees table total.
- Weights sum to 100% or the rounding note covers it.
- One statement per account, and no account silently missing from a batch.
