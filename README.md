# shipstats — OpenCode Skill

> A single skill that turns your weekly metrics into a brand-aligned poster for X. JSON in, screenshot-ready HTML out. No install, no SDK, no API key.

![shipstats example](../examples/tegu-may-26.jpeg)

## What It Does

Drop your numbers, your design system, and (optionally) your logo — get back a self-contained `1080×1200` HTML poster ready to screenshot and tweet.

## Install

### Option 1 — Via skills.sh (recommended)

```bash
# Install directly from the skill registry
opencode skill add mativallej/shipstats
```

### Option 2 — Manual install

Clone or copy the `shipstats/` folder into your OpenCode skills directory:

```bash
# Global skills
cp -r shipstats ~/.config/opencode/skills/shipstats

# Or project-local
cp -r shipstats .opencode/skills/shipstats
```

### Option 3 — Upload to claude.ai (Pro+)

Zip the skill folder and upload via Settings → Capabilities → Skills:

```bash
cd opencode-skill && zip -r shipstats-skill.zip shipstats
```

## Usage

Once installed, the skill auto-invokes when you ask for:

- A weekly recap or stats post
- A metric summary for X / Twitter
- A "ship report" or progress dashboard
- Visualizing numbers in a screenshot-ready format

### Example prompt

> "Armame el poster semanal con estas métricas: [paste your JSON or prose]"

The skill will:
1. Ask for missing inputs (design system, locale, logo)
2. Run the logo prep script if a logo is provided
3. Generate `shipstats-poster.html` in your working directory
4. Print a short narrative summary of what the dashboard tells

## What You Bring

| Input | Required | Format |
|---|---|---|
| **Metrics** | Yes | JSON or prose (period + at least one hero number) |
| **Design system** | No | Markdown spec with tokens (palette, fonts, spacing, etc.) |
| **Logo** | No | PNG/JPG/WebP file path |
| **Context** | No | Language, number format, tone |

No design system? The skill ships with a fallback. Pass nothing and you get sensible defaults.

## Structure

```
shipstats/
├── SKILL.md                  # Skill definition (auto-loaded by OpenCode)
├── scripts/
│   └── prepare_logo.py       # Logo resize + base64 encoding
└── templates/
    ├── design-system.md      # Minimal design system fallback
    └── sample-metrics.json   # Example data shape
```

## License

MIT — see [LICENSE](../LICENSE).

## Author

[Matías Vallejos](https://matiasvallejos.com) · [@mativallej_](https://x.com/mativallej_)

> "Ship daily. Tell the story weekly."
