# 1212 Capital — Claude plugins

The marketplace 1212 Capital uses to distribute its Claude plugins internally.
Add it once, install what you need, and updates arrive when we push here.

## Install

**In Cowork**, which is what most people at 1212 use. Open **Customize** in the
sidebar, then **Plugins**, then **Add marketplace**, and enter:

```
1212-Capital/claude-plugins
```

The catalogue appears as **1212-capital**. Open it and click **Install** on
**1212-brand**. Nothing to authenticate: the repository is public, so no GitHub
account or credentials are involved.

When a new version ships, click **Update** on the marketplace, then reinstall.
Installing without updating first replays the cached catalogue.

**In Claude Code**, the CLI or the Code tab, the same thing in two commands:

```
/plugin marketplace add 1212-Capital/claude-plugins
/plugin install 1212-brand@1212-capital
```

Both surfaces need a paid Claude plan. Plugins run in Cowork and Code, not in
Chat.

## Plugins

| Plugin | What it does |
|---|---|
| **1212-brand** | The brand system and the four A4 document templates: fact sheet, newsletter, internal document, client statement. Plus the four social canvases. See [its README](plugins/1212-brand/README.md). |

## Layout

```
.claude-plugin/marketplace.json    the catalogue
plugins/<name>/                    one folder per plugin, each with its own
                                   .claude-plugin/plugin.json
```

To add a plugin, drop its folder under `plugins/` and add an entry to
`marketplace.json`. `metadata.pluginRoot` is already `./plugins`, so the entry's
`source` is just the folder name.

## Publishing an update

Bump `version` in the plugin's `plugin.json`, commit, push. Team members pick it
up on their next `/plugin marketplace update`, or automatically if they have
auto-update enabled for this marketplace.

The plugin ships **derivatives**, not masters: the 18 brand images here are
optimised 1600x900 JPEGs and the fonts are subset woff2. The masters live in
`1212-Capital/brand-kit`. When a master changes there, re-export, drop it in,
and bump the version.

## Licence

Copyright © 2026 1212 Capital Inc. All rights reserved. This repository is
public so the team can install the plugin without managing repository access,
not to license its contents for reuse. The brand images and the design system
are proprietary; see [LICENSE](LICENSE).

The bundled typefaces are the exception: third-party software under the SIL
Open Font License 1.1, see
[plugins/1212-brand/assets/fonts/LICENSE.md](plugins/1212-brand/assets/fonts/LICENSE.md).
