---
name: 1212-internal-document
description: >
  This skill should be used for any long-form internal 1212 Capital document:
  "due diligence", "DD memo", "investment review", "IC memo", "framework",
  "internal memo", "note interne", "protocol review", "write this up as an
  internal doc", or when turning research and analysis into the branded
  confidential A4 PDF. Covers both the Pencil build and the self-contained HTML
  to PDF build.
metadata:
  version: "1.0.0"
  source: "1212.pen — Internal Document · Template"
---

# 1212 Capital — internal document

One skeleton for every long-form internal document: due diligence, investment
reviews, frameworks, memos. Cover plus as many section pages as the content
needs. 794 × 1123 (true A4 at 96 dpi), 56 px margins, 682 px measure. Same
geometry, palette, radii and furniture as the fact sheet and newsletter.
**English throughout**, whatever language the conversation is in. Read
`1212-brand-kit` first if the palette and type rules are not already loaded.

This is not a Markdown export dressed up. It is built the way the other two
documents are built.

## Intake, before anything else

One round:

| Question | Options |
|---|---|
| What kind of document? | due diligence · investment review · framework · memo |
| What does it decide, and for whom? | free text, one line. If it cannot be answered the document is not ready |
| Classification and status? | Confidential / Draft, pre-selected · another combination |
| Cover image? | dawn · noon · dusk · pick for me |

Take the owner from the person asking unless they say otherwise.

## Build

Start from the template, duplicate the `Doc · Page — Analysis` section as many
times as the content needs, renumber the footers, then render:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/new_doc.py internal-doc review.html
# edit review.html
python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/render_pdf.py \
        review.html 1212-Protocol-Review-v1.0.pdf --png review
```

Pencil route: duplicate `lgWp3` and override the instances. See
`1212-brand-kit/references/pencil.md`.

## Structure

**Cover.** Full-bleed brand image (default `midi/opt-06.jpg`) under the 5-stop
scrim. Logo top left, `CONFIDENTIAL · vX.X` top right. Then kicker (the document
class, e.g. `DUE DILIGENCE · INVESTMENT REVIEW`), title in Lora 56, a one-line
standfirst stating what this document decides, for whom, and over what scope. A
hairline, then a four-column meta strip (DATE · CLASSIFICATION · STATUS ·
OWNER), then the internal-only notice.

**Section pages.** Content gap 30. Sections are marked by the lilac tag, not by
numbered headings. Inside a section, the Lora section heading with its muted
suffix marks a sub-part.

A page is assembled from these blocks, in any order the argument needs:

| Block | Class | Use |
|---|---|---|
| Section label | `.tag` | opens every section |
| Sub-heading | `.heading` | Lora with a muted suffix in parentheses |
| Body | `.doc-body` | Inter 10.5, not justified |
| Bullets | `.bullets` / `.bullet` | bold lead-in then explanation, dot in lavender |
| Table | `.table` + `.cell--pad9` | paper, r10, hairlines, no vertical rules |
| Headline figures | `.statrow` | the dusk band, four keys |
| Commentary | `.commentary` | Lora title plus two justified paragraphs, for a recommendation |
| Source line | `.footnote` | italic, under every table |

Default section order for a review or DD: **SUMMARY → headline figures →
ASSESSMENT (heading, table, source) → RISKS & MITIGANTS (bullets) →
RECOMMENDATION (commentary) → APPENDIX A · DECISION LOG (table)**. Add,
reorder or drop sections to fit the argument; the skeleton is not a checklist to
fill.

## Rules specific to this document

- **The bold lead-in is its own node.** Pencil has no inline mixed weight, so a
  bullet carries the claim in the Term and the explanation in the Text. Keep
  that split in HTML too, so the two routes stay interchangeable.
- **Tables.** Three columns is the shipped shape (200 / 90 / fill). Any other
  shape is built at page level from the head and text cells with fixed widths
  except one, which fills. Head cells are left aligned in this document.
- **Figures** are IBM Plex Mono. Lora is display only at weight 500. Inter is
  body.
- Page background `ivory`, tables and cards `paper`, stat bands `dusk`.
- Radii 999 for tags, 10 for every surface, 0 for everything else. Every rule
  is `line`.
- No em dashes.
- Footer reads `1212 CAPITAL · CONFIDENTIAL · NOT FOR DISTRIBUTION`, page
  numbers `N / N`, renumbered by hand.
- The running head carries `DOCUMENT TITLE · CONFIDENTIAL · vX.X`. Update the
  version on every material revision and keep it identical on the cover.

## Variable length

Not a fixed page count. Keep each Content stack under 988 px, measured by
summing the heights of Content's direct children plus the gaps. When a section
overflows, **start a new page rather than shrinking type**. A section may span
pages; repeat the tag only if the reader would otherwise lose the thread.

## Writing an internal document well

- The standfirst states the decision, the audience and the scope. If you cannot
  write it, the document is not ready.
- Lead with the conclusion. SUMMARY says what you found and what you recommend;
  the rest is evidence.
- Every claim in RISKS carries a mitigant, or it is stated as unmitigated.
- The decision log records open questions and how they were resolved. Supersede
  rows rather than deleting them when a decision is revisited.
- Name the source and as-of date under every table. Internal is not an excuse
  for unsourced numbers.

## Before delivering

1. Version and date match on the cover, every running head, and the filename.
2. Footers renumbered after any page added or removed.
3. Every table has a source line.
4. Owner and status on the cover reflect reality (Draft vs Final).
5. No lorem text, no em dash, no placeholder left unfilled.
6. `check_pdf.py` passes on the exported PDF, and the cover has been
   eyeballed in an actual viewer, not only in the render PNGs.

## References

- `1212-brand-kit/references/tokens.md` — CSS classes and component specs
- `1212-brand-kit/references/voice.md` — tone and mechanics
- `1212-brand-kit/references/pencil.md` — the Pencil build
