---
name: bnt-style-extract
description: Extracts UI/UX styles from target websites and converts them to Tailwind CSS. Triggers on requests mentioning style extraction, UI cloning, design copying, Tailwind conversion, or applying specific website component styles.
---

# BNT Style Extractor

Extracts computed styles from websites using Playwright and converts them to Tailwind CSS classes.

## Setup: Add to .gitignore

All output files are saved to `.style-extract/` directory by default. Add this to your project's `.gitignore`:

```
# Style extraction temp files
.style-extract/
```

## Workflow Checklist

Copy this checklist to track progress:

```
Style Extraction Progress:
- [ ] Step 1: Extract styles (extract.py)
- [ ] Step 2: Convert to Tailwind (convert.py)
- [ ] Step 3: Apply to component
- [ ] Step 4: Visual comparison (compare.py)
- [ ] Step 5: Auto-fix if needed (auto_fix.py)
```

## Quick Start

### 1. Full Page Style Extraction
```bash
# Output: .style-extract/styles.json (default)
python ~/.claude/skills/bnt-style-extract/scripts/extract.py --url "https://example.com"
```

### 2. Specific Element Style Extraction
```bash
# Output: .style-extract/styles.json (default)
python ~/.claude/skills/bnt-style-extract/scripts/extract.py --url "https://example.com" --selector "button.primary"
```

### 3. Convert to Tailwind
```bash
# Output: .style-extract/tailwind.json (default)
python ~/.claude/skills/bnt-style-extract/scripts/convert.py --input .style-extract/styles.json
```

## Workflow

### Step 1: Style Extraction

When user provides a URL, run `scripts/extract.py`.

**Required Parameters:**
- `--url`: Target website URL

**Optional Parameters:**
- `--selector`: CSS selector for specific elements (auto-detects main components if omitted)
- `--screenshot`: Screenshot save path
- `--wait`: Additional wait after page load in ms (default: 2000)
- `--timeout`: Page navigation timeout in ms (default: 60000)
- `--wait-until`: Page load strategy (default: domcontentloaded)
  - `domcontentloaded`: Fast, recommended for most sites
  - `load`: Wait for all resources
  - `networkidle`: Wait for network idle (slow, may timeout on dynamic sites)
  - `commit`: Fastest, just wait for navigation commit
- `--no-states`: Skip hover/focus state capture

**Output Example:**
```json
{
  "url": "https://example.com",
  "elements": [
    {
      "selector": "button.primary",
      "tag": "button",
      "role": "button",
      "styles": {
        "backgroundColor": "rgb(24, 61, 121)",
        "color": "rgb(174, 203, 250)",
        "padding": "12px 16px",
        "borderRadius": "24px",
        "fontSize": "14px"
      },
      "states": {
        "hover": {
          "backgroundColor": "rgb(30, 75, 150)"
        }
      }
    }
  ]
}
```

### Step 2: Style Analysis (Optional)

For complex pages, analyze patterns with `scripts/analyze.py`.

```bash
python ~/.claude/skills/bnt-style-extract/scripts/analyze.py --input styles.json --output analysis.json
```

**Output Example:**
```json
{
  "colorPalette": {
    "primary": ["#183d79", "#1a73e8"],
    "background": ["#000000", "#0d1421", "#202124"],
    "text": ["#ffffff", "#bdc1c6", "#aecbfa"]
  },
  "spacingScale": [4, 8, 12, 16, 24, 32],
  "borderRadii": [4, 8, 16, 24],
  "componentTypes": ["button", "input", "card", "chip"]
}
```

### Step 3: Tailwind Conversion

Generate Tailwind classes with `scripts/convert.py`.

```bash
# Uses default output: .style-extract/tailwind.json
python ~/.claude/skills/bnt-style-extract/scripts/convert.py --input .style-extract/styles.json
```

**Output Example:**
```json
{
  "elements": [
    {
      "selector": "button.primary",
      "tailwindClasses": "bg-[#183d79] hover:bg-[#1e4b96] text-[#aecbfa] hover:text-white py-3 px-4 rounded-3xl text-sm font-medium transition-all",
      "customCSS": null
    }
  ],
  "configExtensions": {
    "colors": {
      "primary": "#183d79",
      "primary-hover": "#1e4b96"
    }
  }
}
```

### Step 4: Visual Comparison

Compare original and implementation with `scripts/compare.py`.

```bash
# Screenshots saved to .style-extract/ (target.png, current.png, diff.png)
python ~/.claude/skills/bnt-style-extract/scripts/compare.py --target "https://example.com" --current "http://localhost:3000" --selector "button.primary"
```

**Output:**
- Similarity score (0-100%)
- Difference list
- Screenshots: `.style-extract/target.png`, `.style-extract/current.png`, `.style-extract/diff.png`

### Step 5: Auto-Fix Loop (Core Feature!)

**IMPORTANT: If similarity is below 95%, automatically iterate fixes.**

```bash
# Screenshots saved to .style-extract/ by default
python ~/.claude/skills/bnt-style-extract/scripts/auto_fix.py \
  --target-url "https://example.com" \
  --current-url "http://localhost:3000" \
  --selector "button" \
  --component-file "components/Button.tsx" \
  --max-iterations 3
```

#### Auto-Fix Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    Auto-Fix Iteration Loop                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Run compare.py → Check similarity                       │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────┐                                       │
│  │ Similarity ≥ 95%?│──── Yes ──→ Done! Report results      │
│  └──────────────────┘                                       │
│         │ No                                                │
│         ▼                                                   │
│  2. Analyze differences (color? spacing? border?)           │
│         │                                                   │
│         ▼                                                   │
│  3. Re-extract target properties                            │
│         │                                                   │
│         ▼                                                   │
│  4. Auto-fix component code                                 │
│         │                                                   │
│         ▼                                                   │
│  5. Iterate (max 3 times)                                   │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────┐                                       │
│  │ Exceeded 3?      │──── Yes ──→ Manual review needed      │
│  └──────────────────┘                                       │
│         │ No                                                │
│         └──────────────→ Back to Step 1                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Fix Priority

| Priority | Difference Type | Fix Method |
|----------|----------------|------------|
| 1 | Background/Text color | Re-extract color → Replace Tailwind class |
| 2 | Spacing (padding/margin) | Re-measure px → Adjust py-X, px-X |
| 3 | Border (border-radius) | Re-extract value → Adjust rounded-X |
| 4 | Font size/weight | Re-extract value → Adjust text-X, font-X |
| 5 | Shadow/effects | Handle with custom CSS if complex |

#### Output Example

```json
{
  "iteration": 2,
  "previousSimilarity": 87.5,
  "currentSimilarity": 96.2,
  "status": "PASSED",
  "fixes": [
    {
      "property": "backgroundColor",
      "before": "bg-[#1c1c1e]",
      "after": "bg-[#0d1421]",
      "file": "components/ChatOverlay.tsx",
      "line": 66
    }
  ],
  "message": "Achieved ≥95% after 2 iterations. Complete."
}
```

## Component Generation

When creating React components from extracted styles, refer to templates in `templates/` directory.

For detailed component patterns, see [PATTERNS.md](PATTERNS.md).

## Tailwind Mapping Rules

For color, spacing, typography Tailwind mapping rules, see [REFERENCE.md](REFERENCE.md).

## Auto-Fix Trigger Keywords

When requests include terms like:
- Korean: "자동으로", "알아서", "복제", "똑같이", "그대로"
- English: "automatically", "clone", "replicate", "exactly like", "same as"

Proceed with full automated workflow:
Extract → Convert → Apply → Compare → Auto-fix

## Cautions

1. **Network Access**: This Skill accesses external websites. Use only trusted URLs.
2. **Dynamic Content**: For SPAs, use `--wait-until domcontentloaded` (default) and increase `--wait` if needed.
3. **Timeout Issues**: If extraction times out, try `--wait-until commit` or increase `--timeout`.
4. **Authenticated Pages**: Pages requiring login are not supported.
