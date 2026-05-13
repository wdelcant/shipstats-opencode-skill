---
name: shipstats
description: >
  Generate a brand-aligned weekly stat poster as a self-contained 1080x1200 HTML
  from metrics JSON + design system. Trigger: weekly recap, stats post, metric
  summary for X, "ship report", or visualizing numbers in a screenshot-ready format.
license: MIT
metadata:
  author: mativallej
  version: "1.0"
---

# shipstats

You generate standalone HTML dashboards for social media, aligned to a provided design system and provided data. Zero invention.

## Inputs

Ask the user for these if missing. Do not fill placeholders — ask.

- **data** — JSON or prose. Required: `period`, `hero_metric` (name + value + optional delta), `support_metrics` (2-3 name/value pairs), `breakdown` (list ordered by volume). Optional: `daily_series` (for peak detection), `traffic` (for complementary stat), `cumulative` (for timeline).
- **design_system** — markdown spec with: typography (sans + mono with weights), primary palette 50-900, neutral palette, semantic colors (success/warning/error), named gradients, spacing scale, radius tokens, shadows, theme (light/dark), anti-patterns. If the user has none, point them to [getdesign.md](https://getdesign.md/) or use the `templates/design-system.md` shipped with this skill as a fallback.
- **logo** — optional file path (PNG/JPG/WebP). If provided, run the logo prep script (see below) and embed the returned base64 string. If empty, default to a typographic wordmark in sans extrabold.
- **context** — period covered, key events, tone (celebratory/sober/educational), output language, number format (e.g. `"1,234.56"` US, `"1.234,56"` EU, `"1.234"` AR), date format. If empty, ask for output language and number format.

When generating, verify locale consistency end-to-end:
- (a) thousands and decimal separators match across hero, support, breakdown and chart labels
- (b) date format including month casing and abbreviation is identical everywhere
- (c) currency placement and symbol match (e.g. `USD 8.420` vs `$8.420` — pick one)
- (d) negative-delta sign convention is consistent (`-12,4%` vs `▼ 12,4%`)

If `data` or `design_system` are empty or missing minimum fields (`period` + `hero_metric.value` + at least 1 breakdown item), ask the user for the missing pieces before generating.

## Logo preparation

If the user provides a logo file, run the bundled script:

```bash
python3 scripts/prepare_logo.py <path-to-logo>
```

It outputs a data URI (`data:image/webp;base64,...`) resized to 128x128, ready to inline as `<img src="...">`. Do not attempt PIL/base64 work yourself — the script is deterministic and saves tokens.

## Preflight

Layout budget pass: before writing the HTML, list each planned section with an estimated height and sum them (including gaps and canvas padding). If the total exceeds the canvas height (1200 default), shrink hero typography or reduce paddings until it fits with a 40-60px safety margin. Document the budget breakdown in `<flags>`.

## Rules

- Single HTML file, everything inline. Fonts via Google Fonts with preconnect. Images as data URIs. No external scripts except the canvas auto-scale.
- Fixed canvas 1080x1200 with auto-scale to fit viewport while preserving aspect ratio. Equal padding on all four sides of the canvas (use a value from the design system spacing scale, typically 48-64px). The last section must have the same bottom padding as the top — never let content touch the canvas edge.
- Canvas vertical budget: in 1080x1200, the sum of section heights + gaps + canvas padding must be ≤ 1200. Compute an approximate per-section budget before generating and validate. If it does not fit, shrink hero typography (reasonable range: 72-96px) or reduce paddings BEFORE generating, not after.
- Forbidden: `flex: 1` or `min-height: 0` on canvas sections to "fill space". Children size to their content. Leftover space stays as bottom air, and that is fine.
- Inline SVGs with `width: 100%` derive height from the viewBox aspect ratio. Use flat viewBoxes (minimum ratio 3:1, e.g. 520x140) for small charts, or set a fixed height in CSS. Never assume an SVG will "adapt" to the available space — it takes what it asks for.
- Captions with `max-width` smaller than the card width wrap to multiple lines. Reserve space for the worst case (3 lines) or trim the text.
- Design system tokens via CSS variables in `:root`. Zero hardcoded hex in `style=""`. Zero invented gradients — use only the ones named in the design system.
- **Inline SVG color tokens**: CSS vars do not resolve inside SVG attributes like `fill="..."` or `stop-color="..."`. Use `style="fill: var(--c-x)"` to reference tokens. Bare hex inside SVG attributes is acceptable only when that exact hex is also defined as a CSS var in `:root` and used in CSS elsewhere — the SVG hex is a mirror, never a new value.
- **Derived gradient fallback**: if the design system has no named gradient, derive ONE as `linear-gradient(135deg, <primary> 0%, <primary-active or primary-700> 100%)`, declare it in `:root` as `--g-brand`, and declare it in `<flags>`. Use this single gradient for both hero card background and progress bars.
- Typography, spacing, radius, shadows: ONLY from the design system. If a needed token is missing, fall back to the closest value in the defined scale and declare it in `<flags>`.
- Charts as inline SVG with `<defs>` for gradients and filters. No chart libraries.
- Numbers: only those present in `data`. Derived numbers (conversion %, ratios) only if the math is verifiable; otherwise omit.
- Use the number and date format declared in `context`.
- Anti-patterns to reject: more than one decorative gradient per screen, per-category color coding, emojis if the design system defines an iconset, serifs if the design system is sans-only, hardcoded hex outside `:root`.
- Anti-pattern: rendering temporal/cumulative comparisons as filled cards. Before→after metrics use a line connector with endpoints, not a chrome container. Card chrome competes with the directional read; the line carries it natively.

## Dashboard layout

Narrative hierarchy, not rigid structure. Include only what the data justifies:

1. **Header**: logo or wordmark + optional tagline + badge with period.
2. **Timeline** (only if `cumulative` is present): horizontal line connector, NOT a card. Two endpoints with: big number (display weight 700, ~32px) + uppercase sub-label + date caption. Previous endpoint in neutral grey (`--c-body` or equivalent), current in ink. Delta floats centered on the line with canvas-color background masking the line where it crosses. Small filled dots at each endpoint. No card chrome — the line IS the metaphor for progression.
3. **Hero metric + 2-3 support metrics** in a row. Hero in featured card with the brand gradient. Delta tag top-right if comparison exists.
4. **Main breakdown**: vertical list with horizontal bars. ALL bars use the same progress gradient from the design system. Hierarchy comes from width, not color.
5. **Mini-grid** (only if `daily_series` and/or `traffic` are present): bar chart with peak highlighted + complementary stat with sparkline.

Hero metric uses the largest type. Eyebrows in mono caps. Numbers in sans extrabold with negative letter-spacing.

Hero metric font-size: range 72-96px. Larger only if the vertical budget allows it and there are no critical sections below.

Hero card vertical padding: 2xl in normal budget, 3xl only if there is leftover height.

**Eyebrow default token** (use if the design system doesn't define one): `11px / weight 600 / 0.6px letter-spacing / uppercase / mono`. If the design system has no mono family, fall back to `'JetBrains Mono', ui-monospace, SFMono-Regular, monospace` and declare it in `<flags>`.

## Auto-scale

The canvas must scale down to fit the viewport while keeping its aspect ratio. Use this exact pattern — naive flex centering breaks in iframe contexts (claude.ai preview, embeds) because `min-height: 100vh` lets the body grow to contain the unscaled 1200px canvas, pushing the visual center outside the visible viewport.

```css
body {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: relative;
  margin: 0;
}
.canvas-wrap {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 1080px;
  height: 1200px;
  transform-origin: center center;
  transform: translate(-50%, -50%) scale(var(--scale, 1));
}
```

```js
function scaleCanvas() {
  var pad = 24;
  var sx = (window.innerWidth  - pad * 2) / 1080;
  var sy = (window.innerHeight - pad * 2) / 1200;
  var s = Math.min(sx, sy, 1); // never scale up
  document.getElementById('canvas-wrap').style.setProperty('--scale', s);
}
addEventListener('resize', scaleCanvas);
addEventListener('load', scaleCanvas);
scaleCanvas();
```

Key invariants:
- Body is exactly viewport-sized — never `min-height`.
- The wrap is taken out of flow with `position: absolute` so it cannot push the body taller.
- Centering and scaling travel in the same `transform` via a CSS variable; the JS only updates the scalar, never the translate.

## Output

1. Write the HTML to `./shipstats-poster.html` in the user's current working directory (or a path the user specifies). **Exception**: if running inside a Claude environment where `/mnt/user-data/outputs/` exists, write there instead — the user accesses the file via the file-sharing UI.
2. Print the path so the user can open it.
3. Then in chat, with no preamble:

```
<story>3-4 bullets with the narrative the dashboard tells.</story>
<gaps>Data that could not be shown due to missing info.</gaps>
<flags>Assumptions made (including any design token fallbacks and the layout budget breakdown).</flags>
```

## Templates available in this skill

- `templates/design-system.md` — minimal design system fallback if the user has none.
- `templates/sample-metrics.json` — example data shape the user can copy.
