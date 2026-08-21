# Building in Pencil (`1212.pen`)

**This route is optional.** It needs the Pencil desktop app open on the shared
`1212.pen`, reached through the Pencil MCP server. Most people at 1212 will not
have it, and they do not need it: the HTML route produces the same document,
byte for byte on the page. Use Pencil when you want the design file itself to
carry the new issue.

Tools: `mcp__remote-devices__pencil__execute` (and `get_app_state`,
`get_guidelines`). Call `get_app_state` first: it reports the path of the open
file, which differs per machine. Do not assume a path.

One warning that has already cost time: the app holds unsaved edits. If you read
the `.pen` from disk you may be reading a stale file. Read the live document
through `execute`, or ask whoever has it open to save first.

## Golden rules

1. **Duplicate, never rebuild.** `Copy` an existing page set, then override
   text. The three documents are built entirely from component instances.
2. **Never detach an instance.** Override the descendant's `content`.
3. Emulate deleting a descendant with `enabled: false`, never `Delete`.
4. Set `placeholder: true` on any new or copied root frame for the whole time
   you work on it, and clear it when done.
5. Verify with `Get(page, (n,c) => c.problems && Print(...))` before
   screenshotting.

## IDs are a cache, not a contract

The IDs below were read from the file. If anyone recreates a component its ID
changes. **Always re-resolve before a build:**

```js
Get(n => n.reusable && Print(n.id, "=", n.name))
```

and match on the name. If a name no longer resolves, stop and ask rather than
guessing.

## Components

| ID | Name |
|---|---|
| `vMXTP` | 1212 · Logo — children `t84J4M` (1212), `s3X54` (CAPITAL) |
| `bVeDT` | 1212 · Cover Masthead — `XtkcH` kicker, `ga5Rh` headline, `XOv2Z` standfirst |
| `RPmSh` | 1212 · Stat Card — `u5dN3K` key, `U2ahEe` value |
| `D7kwbd` | 1212 · Stat Row — cells `WysJW`, `C9z3O`, `wKsMs`, `uft2t` (address as `WysJW/u5dN3K`) |
| `ctMst` | 1212 · Cell · Head — `X1WAX` |
| `j6algT` | 1212 · Cell · Text — `PLwSZ` |
| `itKhJ` | 1212 · Cell · Figure — `u5aet` |
| `FCzTN` | 1212 · Cell · Figure Accent — `msEZ1` |
| `ZO91j` | 1212 · Tag — `WZ3fN` |
| `NJ0jy` | 1212 · Section Label — `UxV6N` |
| `Z24lwV` | 1212 · Section Heading — `JjtIA` main, `qLWlu` suffix |
| `k50Fcr` | 1212 · Footnote — `d7i1dj` |
| `z3jOJy` | FS · Product Title — `M3v8Uu` name, `eo7TO` desc, `BgHJq` pill |
| `OHU6g` | 1212 · Key Fact Row — `KdVzs` label, `BcIRO` value |
| `vmCpS` | 1212 · Metric Row — `vV713` label, `LSYU7` value |
| `a82gF4` | FS · Donut — `ZlEp3`, `nXrTq`, `CVWM0` |
| `d8Xcfw` | FS · Legend Item — `ph2HT` dot, `v6LaRs` label, `A45ejp` value |
| `VODO5` | FS · Exposure Row — `e7qI7` dot, `kqlBv` name, `kX8mA` bar, `d2Z1d3` value |
| `iO6Ol` | FS · Protocol Row — `D6lGw` mark, `u1r8u` name |
| `xLVSj` | FS · Bar Chart |
| `h6NmQ` | FS · Table |
| `z7vVS` | FS · Legend Row |
| `H0tHAR` | FS · Glossary Entry — `uanvK` term, `dAV1B` definition |
| `s06jr` | 1212 · Disclaimer Paragraph — `q4uXsD` |
| `R02IjC` | 1212 · Commentary — `P3N2it` title, `Yj0pB` body A, `haL5r` body B |
| `y6XJpb` | 1212 · Page Header — `SBnn1` meta |
| `FjFXU` | 1212 · Page Footer — `negCd` meta, `wvgBq` page number |
| `OXIr2` | NL · Section Label — `BVfrb` |
| `E5RjY` | NL · Headline — `nqyCe` |
| `BqtYI` | NL · Body Text — `Q7Fn4o` |
| `t8z0mA` | NL · Source — `j1UzXg` |
| `Rg5sa` | NL · Image |
| `lokaW` | NL · Coverline — `EO4cI` topic, `euN9N` head |
| `sf5zH` | NL · Brief — `F7Z76` image, `j4OPo` kicker, `nbqtv` headline, `u00rs` body, `EMb7w` source (→ `EMb7w/j1UzXg`) |
| `EQti4` | NL · Page Header — `RLzb2` meta |
| `MdUaW` | NL · Page Footer — `TXEBg` pub, `uToIE` source |
| `RXPRu` | NL · Article Title — `Y5qgDZ` section (→ `Y5qgDZ/BVfrb`), `f4idDU` headline (→ `f4idDU/nqyCe`) |
| `IkrIZ` | NL · Body Columns — `aJ9k6`, `gJQfP` (→ `aJ9k6/Q7Fn4o`) |
| `g4gsAC` | NL · Coverline Row — `e1cz4`, `cxVwA`, `g6nl6` |
| `J6i8l` | DOC · Body — `NijnJ` |
| `u94L6l` | DOC · Bullet — `dCwZs` term, `a6cjp` text |
| `oruqj` | DOC · Meta Item — `ADyY3` label, `w8PRQl` value |
| `RIMnY` | DOC · Page Header — `EbIib` meta |
| `fYLvd` | DOC · Page Footer — `vFfxn` meta, `inIdi` page number |
| `ACMOa` | DOC · Table |
| `pEjnp` | Auth · Brand Panel (app screens) |

## Document frames

| ID | Frame |
|---|---|
| `j6tjdE` | Fact Sheet · Monthly (wrapper) — `mLTsz` Pages, `mAkad` Blocks Library, `H1Rpi` guide note |
| `X4TnaF` | Fact Sheet · Cover |
| `OM2R4` | Page 1 — Overview & Performance |
| `oHw6r` | Page 2 — Allocation & Monthly Returns |
| `H6RJjr` | Page 3 — Glossary & Risk Considerations |
| `Rw8d0` | Page 4 — Important Information |
| `DV2oS` | Newsletter · Monthly — `Ggi9M` Pages, `O93dZ` library, `uwdqK` guide |
| `rPmKq` | Newsletter · Cover |
| `GlrbA` / `ozOoc` / `Y6tqgC` | Section pages 02 / 03 / 04 |
| `uJDkW` | Client Statement · Monthly — `U6CYQ` Pages, `NDrFF` library, `kHTtK` guide |
| `VOEgM` | Statement · Cover |
| `mPWg2` | Statement · Page 1 — Portfolio Summary |
| `UXzG1` | Statement · Page 2 — Activity & Fees |
| `i090HC` | Statement · Page 3 — Important Information |
| `QGi77` | Internal Document · Template — `lgWp3` Pages, `i7NDt` library, `RI7iM` guide |
| `OEVK1` | Doc · Cover |
| `hsYrQ` | Doc · Page — Analysis |
| `DLADJ` | Doc · Page — Decision & Appendix |
| `nN6Nd` | Brand System · `YJU4f` Brand Kit · `Lg6zU` Assets · `u69Ren` Landing |

## What changed in August 2026

Seven components lost the `FS ·` prefix and now read `1212 ·`, because the
client statement uses them too: Page Header, Page Footer, Footnote, Commentary,
Disclaimer Paragraph, Key Fact Row and Metric Row. The IDs did not change.
`NL · Source` was added and the newsletter's source line moved out of the page
footer into the article and brief blocks. The newsletter Content gap went from
30 to 26.

Later in the month the logotype changed weight: `CAPITAL` in `1212 · Logo`
(`s3X54`) went from Lora 400 to Lora 600, so both words are now semibold, with
`CAPITAL` still letter-spaced. The square lockup in the Brand Kit frame was
redrawn as `1212` large over `CAPITAL` in spaced capitals, on four grounds
(paper, ivory, sand, dusk); the ink ground was removed.

## Monthly build recipe

```js
// 1. park the new set in free space, next to last month's
const pos = FindEmptySpace({width: 4400, height: 1400, nodeId: "j6tjdE", padding: 120})
setId = Copy("mLTsz", document, {name: "Fact Sheet · July 2026", x: pos.x, y: pos.y, placeholder: true})

// 2. read the copy's children — Copy assigns new ids to every descendant
pages = Get(setId, {depth: 1}).children.map(c => c.id)
Print(pages)
```

Then, per page, `Update(instancePath, {content: "..."})` on the descendant
paths, for example:

```js
Update(coverId + "/" + issueId, {content: "FACT SHEET · JUL 2026"})
Update(p1Id + "/" + headerRef + "/SBnn1", {content: "1212.STABLE · FACT SHEET · AS OF 31 JULY 2026"})
```

Because the copy re-ids descendants, drive updates from a `Get` of the copy
rather than from the table above:

```js
Get(setId, n => n.type === "text" && /XX\.XX%|DD MMMM YYYY|MMM YYYY/.test(n.content || "") && Print(n.id, n.content))
```

Finish with `Update(setId, {placeholder: false})` and a `TakeScreenshot` of one
page.

## Exporting

```js
Export([coverId, p1, p2, p3, p4], "pdf", "./exports")           // one multi-page PDF
Export([coverId], "png", "./exports")                            // 2x PNG per node
Export([p1], "html-css", "./exports/page1.html")                 // markup handoff
```

Paths are relative to the .pen file. `export_html` as a standalone MCP method
is not available in every Pencil build; the `Export` function inside `execute`
is.
