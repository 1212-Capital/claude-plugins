---
name: 1212-client-statement
description: >
  This skill should be used when producing a 1212 Capital client statement:
  "client statement", "statement of account", "monthly statement", "relevé
  client", "send the statements", "statement for [client]", or when turning
  per-account holdings, movements and fees into the confidential A4 PDF sent to
  an individual account holder. Covers a single statement and a batch across
  every account.
metadata:
  version: "1.0.0"
  source: "1212.pen — Client Statement · Monthly"
---

# 1212 Capital — client statement

One statement per client per period. Cover + 3 pages, 794 × 1123 (true A4 at
96 dpi), 56 px margins, 682 px measure. Read `1212-brand-kit` first if the
palette and type rules are not already loaded.

## The distinction that governs this document

The fact sheet reports **the strategy**. This reports **the client**. Every
figure is specific to one account: their units, their subscription dates, the
fees actually charged to them. A client's return will differ from the strategy
return published in the fact sheet, because it depends on when they came in and
out. Page 3 says so explicitly. Do not delete that paragraph, and do not paste
strategy-level performance into the performance block.

## Intake, before anything else

One round, four questions:

| Question | Options |
|---|---|
| One account or the whole book? | a named client · every account for the period |
| Which client? | ask only when the answer above is a named client |
| Which period? | *last completed month*, pre-selected · another range |
| Cover image? | dawn · noon · pick for me (figures are allowed here, this document is personal) |

Then ask where the account data comes from: the fund administrator's pack, a
CSV, or the Lagoon position data. Never compute a client return from a strategy
return; it depends on their own subscription and redemption dates.

## Build

One account:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/build_statement.py \
        meridian.json out/meridian.html --pdf out/meridian.pdf
```

Every account in one pass, one PDF per client:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/build_statement.py \
        july-accounts.json out/2026-07/ --batch --pdf
```

In batch form the JSON is `{"common": {...}, "accounts": [{...}, {...}]}`, or a
bare list. `common` carries whatever every account shares that period: the
period string, the as-of date, the reference prefix. Files are named from the
reference and the account number. Schema: `references/data-contract.md`.

For a one-off shape the builder does not cover, start from the template:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/new_doc.py client-statement work.html
```

Pencil route: duplicate `U6CYQ` and override the instances. See
`1212-brand-kit/references/pencil.md`.

## What goes on each page

**Cover.** Brand image (default `matin/opt-03.jpg`) under the 5-stop scrim.
Logo top left, `CONFIDENTIAL · CLIENT STATEMENT` top right. Then the kicker,
the client name in Lora 56, a standfirst, a hairline, a four-column meta strip
(account, period, currency, relationship manager), and the notice.

**Page 1 — Portfolio Summary.** The dusk stat row with four headline figures,
then Account and Your Performance side by side at 327 px each, then the
Positions table. Your Performance carries a `Fund, same period` line so the
client sees the gap between their return and the strategy's. Content gap 30.

**Page 2 — Activity & Fees.** Movements for the period, then fees and costs,
then a commentary written for this account. Content gap 30.

**Page 3 — Important Information.** Five paragraphs and a contact block.
Content gap 34.

## Rules specific to this document

- **This document introduces no component of its own.** Everything comes from
  the shared group. If a block is missing, build it from the cell components,
  do not invent one.
- **Every numeric cell is IBM Plex Mono**, right-aligned, with its column
  header right-aligned too. Dates and type labels stay Inter, left-aligned.
- **The movements table is the block that grows.** Add rows freely. If the page
  passes 988 px, move the commentary to page 3 rather than shrinking anything.
- **Signs are explicit.** Subscriptions and gains carry `+`, redemptions and
  fees carry `−` (U+2212, not a hyphen). An empty cell is an em dash `—`, which
  is the one place the no-em-dash rule does not apply because it is a glyph and
  not prose.
- **Issuer and Regulatory status ship as bracketed placeholders.** Fill them
  before any statement is sent and have counsel confirm the wording for the
  jurisdiction.
- The commentary is written for this account, not copied from the fact sheet.
  If nothing account-specific happened, say that in one line.

## Before delivering

1. The account number on the cover, in every running head, in the Account
   block and in the statement reference all match.
2. Positions value column sums to the portfolio value in the stat row.
3. Net contributions plus gain equals portfolio value.
4. Movements for the period reconcile with the change in net contributions.
5. The `Fund, same period` line is the strategy return, and any gap to the
   client return is explained by the commentary or by a dated movement.
6. Fees shown equal the fee lines in the movements table.
7. No placeholder left unfilled, no lorem text, no em dash in prose.
8. `check_pdf.py` passes, and one statement has been opened in a real viewer.

## References

- `references/data-contract.md` — the JSON schema, field by field
- `1212-brand-kit/references/tokens.md` — CSS classes and component specs
- `1212-brand-kit/references/pencil.md` — the Pencil build
