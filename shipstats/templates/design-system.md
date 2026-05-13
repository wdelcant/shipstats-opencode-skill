# Design System — Fallback Template

Minimal token set the shipstats skill will use if the user has no design system.
Replace any of these with your brand's real tokens — the structure (not the values) is what the prompt needs.

## Typography

- **Sans**: `Inter`, weights 400 / 500 / 700 / 800
- **Mono**: `JetBrains Mono`, weights 400 / 500

## Primary palette

| Token | Value |
|---|---|
| `--p-50`  | `#eef2ff` |
| `--p-100` | `#e0e7ff` |
| `--p-200` | `#c7d2fe` |
| `--p-300` | `#a5b4fc` |
| `--p-400` | `#818cf8` |
| `--p-500` | `#6366f1` |
| `--p-600` | `#4f46e5` |
| `--p-700` | `#4338ca` |
| `--p-800` | `#3730a3` |
| `--p-900` | `#312e81` |

## Neutral palette

| Token | Value |
|---|---|
| `--n-0`   | `#ffffff` |
| `--n-50`  | `#f8fafc` |
| `--n-100` | `#f1f5f9` |
| `--n-200` | `#e2e8f0` |
| `--n-400` | `#94a3b8` |
| `--n-600` | `#475569` |
| `--n-800` | `#1e293b` |
| `--n-900` | `#0f172a` |

## Semantic

- `--success` `#10b981`
- `--warning` `#f59e0b`
- `--error`   `#ef4444`

## Gradients

- `--g-brand`: `linear-gradient(135deg, var(--p-500) 0%, var(--p-700) 100%)`
- `--g-progress`: `linear-gradient(90deg, var(--p-400) 0%, var(--p-600) 100%)`

## Spacing scale

`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96` (in pixels)

## Radius

`--r-sm: 8px · --r-md: 12px · --r-lg: 20px · --r-xl: 28px`

## Shadows

- `--shadow-sm`: `0 1px 2px rgba(15, 23, 42, 0.06)`
- `--shadow-md`: `0 8px 24px rgba(15, 23, 42, 0.08)`

## Theme

Light (default). Background `var(--n-50)`, ink `var(--n-900)`, body `var(--n-600)`.

## Anti-patterns

- More than one decorative gradient per screen
- Per-category color coding in the breakdown bars
- Hardcoded hex outside `:root`
- Serif fonts (this system is sans-only)
