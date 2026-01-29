---
name: bnt-image-extract
description: Extracts UI/UX styles from design images (PNG/JPG/screenshot) and converts them to Tailwind CSS classes. Triggers on requests mentioning image style extraction, screenshot-to-code, design-to-tailwind, UI image cloning, or creating components from design images.
---

# BNT Image Style Extractor

Extracts UI styles from design images using Claude Vision + PIL, converts to Tailwind CSS.

## Setup: Add to .gitignore

```
# Image extraction temp files
.image-extract/
```

## Workflow Checklist

Copy this checklist to track progress:

```
Image Style Extraction Progress:
- [ ] Step 1: Visual analysis (Claude reads image)
- [ ] Step 2: Precise extraction (extract_from_image.py)
- [ ] Step 2.5: Hybrid extraction (if source URL known)
- [ ] Step 3: Tailwind conversion
- [ ] Step 4: Component generation
- [ ] Step 5: Compare & auto-fix (compare.py)
```

## Step 1: Visual Analysis (Claude Vision)

Read the design image directly. Identify and document:

1. **Component hierarchy** (tree structure with nesting)
2. **Component types** (sidebar, button, card, input, nav-item, etc.)
3. **Layout direction** (vertical/horizontal, flex-col/flex-row)
4. **Font size estimation** - estimate text height in px for each text element (Step 2 auto-corrects via pixel measurement)
5. **Text color analysis** - distinguish white / off-white / light gray / dark gray / black (Step 2 auto-corrects via interior pixel sampling)
6. **Font weight estimation** - thin / light / normal / medium / bold (Step 2 auto-corrects via stroke width analysis)
7. **Icon dimensions** - estimate icon width x height in px
8. **Stroke width** - line thickness for icons and borders (1 / 1.5 / 2px)
9. **Font family hints** - serif / sans-serif / monospace, geometric / humanist
10. **Spacing patterns** - gaps between elements, section padding in px (Step 2 auto-measures gaps for repeated elements)
11. **Bounding regions** as JSON for Step 2:

```json
[
  {"name": "sidebar-header", "bounds": {"x": 0, "y": 0, "w": 213, "h": 48}},
  {"name": "nav-item-home", "bounds": {"x": 0, "y": 48, "w": 213, "h": 44}}
]
```

Save regions to `.image-extract/regions.json`.

### Vision Analysis Output Template

Document findings in this format before proceeding to Step 2:

```
Vision Analysis Results:
- Font sizes: header=18px, nav-item=14px, label=12px (auto-corrected in Step 2)
- Font weights: header=normal, nav-item=medium (auto-corrected in Step 2)
- Text colors: primary=#ffffff, secondary=#e5e7eb, muted=#9ca3af (auto-corrected in Step 2)
- Icon sizes: nav-icons=24x24px
- Stroke widths: nav-icons=1.5
- Font family: sans-serif, geometric
- Spacing: nav-item-gap=4px, section-padding=16px (auto-measured in Step 2)
```

## Step 2: Precise Extraction

Run `extract_from_image.py` with the image and regions from Step 1.

```bash
# Basic: palette only
python ~/.claude/skills/bnt-image-extract/scripts/extract_from_image.py \
  --image "path/to/design.png"

# With regions from Step 1
python ~/.claude/skills/bnt-image-extract/scripts/extract_from_image.py \
  --image "path/to/design.png" \
  --regions ".image-extract/regions.json"
```

**Parameters:**
- `--image` (required): Path to design image
- `--regions`: JSON file with region coordinates from Step 1
- `--output`: Output path (default: `.image-extract/styles.json`)
- `--palette-size`: Number of dominant colors (default: 10)

**Output:** `.image-extract/styles.json` with color palette, region styles, and elements array compatible with bnt-style-extract pipeline.

**Auto-extraction features (P1-P5):**
- **Font size** (P1): Pixel-level text height measurement via background contrast analysis, then cap-height ratio (0.72) conversion. Falls back to heuristic if measurement fails.
- **Font weight** (P4): Horizontal stroke run-length analysis. Median stroke width / font size ratio maps to CSS weight (200-800).
- **Text color** (P5): Interior pixel sampling only (4-neighbor non-background check). Excludes anti-aliasing edge artifacts.
- **Background gradient** (P3): Vertical/horizontal strip sampling (10 points, center 60%). Detects monotonic brightness change and generates `bg-gradient-{direction} from-[#hex] to-[#hex]`.
- **Element gaps** (P2): Auto-detects repeated element groups by name prefix (e.g., "bar-attack", "bar-magic" -> "bar" group). Measures gaps and outputs Tailwind gap class.

## Step 2.5: Hybrid Extraction (Optional)

When the source URL of the design is known, combine both extraction methods for higher accuracy.

### Decision Flow

```
Source URL available?
  |- Yes -> Run bnt-style-extract first (exact CSS values)
  |         Then run bnt-image-extract (visual verification)
  |         Merge: use CSS values as primary, image data as fallback
  |- No  -> Continue with image-only extraction (Step 3)
```

### Procedure

1. **CSS extraction first**: Use bnt-style-extract with the source URL to get exact computed styles (font-size, color, padding, etc.)
2. **Image verification**: Use bnt-image-extract to visually verify the extracted styles match the design image
3. **Merge strategy**: Prefer CSS-extracted values for typography (font-size, font-weight, line-height, color) and use image-extracted values for layout and visual elements not captured by CSS

### When to Use

- The design image is a screenshot of a live website
- The source URL is accessible and renders the same content as the image
- Font sizes or text colors from image extraction have low confidence

## Step 3: Tailwind Conversion

Apply conversion using the extracted styles and mapping rules.

For color, spacing, typography mapping rules, see [REFERENCE.md](REFERENCE.md).

**Conversion priority:**
1. Background colors -> `bg-[#hex]` or named Tailwind color
2. Text colors -> `text-[#hex]`
3. Dimensions -> `w-[Npx]`, `h-[Npx]` or Tailwind scale
4. Spacing -> `p-N`, `gap-N` etc.
5. Border radius -> `rounded-*`
6. Layout -> `flex`, `flex-col`, `items-center`, etc.

**Note:** Font sizes and weights are estimated from visual analysis. Use common UI conventions:
- Section headers: `text-xs` (12px), `font-normal`, `text-gray-400`
- Nav items: `text-sm` (14px), `font-medium`
- Logo text: `text-base` (16px), `font-semibold`

## Step 4: Component Generation

Create React/TSX components with extracted Tailwind classes.

For component patterns and templates, see [PATTERNS.md](PATTERNS.md).

Match detected component types to patterns:
- Sidebar -> Sidebar pattern in PATTERNS.md
- Button -> Button pattern
- Card -> Card pattern
- Input -> Input pattern
- Navigation items -> custom based on extracted styles

## Step 5: Compare & Auto-Fix

After generating components, compare with the original design.

```bash
# Compare original image vs running implementation
python ~/.claude/skills/bnt-image-extract/scripts/compare.py \
  --original "path/to/design.png" \
  --current-url "http://localhost:3001" \
  --selector ".sidebar"

# Or compare with a screenshot file
python ~/.claude/skills/bnt-image-extract/scripts/compare.py \
  --original "path/to/design.png" \
  --current-image ".image-extract/current.png"
```

**Parameters:**
- `--original` (required): Path to original design image
- `--current-url`: URL to screenshot (uses Playwright)
- `--current-image`: Path to implementation screenshot (alternative to URL)
- `--selector`: CSS selector for specific element
- `--output-dir`: Directory for output files (default: `.image-extract`)
- `--threshold`: Similarity threshold (default: 95%)
- `--metric`: Similarity metric - `ssim` (default, structural), `rms` (legacy), `both`
- `--font-search`: Analyze difference bands to suggest font size adjustments
- `--auto-viewport` (P6): Auto-match Playwright viewport to original image dimensions. Eliminates resize artifacts when comparing.
- `--regions` (P7): Region JSON file path for per-region SSIM analysis. Identifies which component has the most difference.

### Auto-Fix Loop

If similarity < 95%, iterate:

```
1. Read diff image (.image-extract/diff.png)
2. Read original image alongside diff to identify problem areas
3. Run --font-search to identify font size mismatches:
   python ~/.claude/skills/bnt-image-extract/scripts/compare.py \
     --original "design.png" --current-image ".image-extract/current.png" \
     --font-search
3.5. Run --regions for per-region SSIM analysis (P7):
   python ~/.claude/skills/bnt-image-extract/scripts/compare.py \
     --original "design.png" --current-image ".image-extract/current.png" \
     --regions ".image-extract/regions.json"
   -> Identifies which region has the lowest SSIM score
4. Re-extract colors from problematic regions (re-run Step 2 with refined regions)
5. Adjust Tailwind classes based on new data and font-search suggestions
6. Rebuild and re-compare (use --auto-viewport for URL comparison)
7. Repeat (max 3 iterations)
```

**Fix priority:**

| Priority | Type | Action |
|----------|------|--------|
| 1 | Background/text color | Re-sample region, update `bg-*`/`text-*` |
| 2 | Font size/weight | Run `--font-search`, adjust `text-*`/`font-*` |
| 3 | Spacing/padding | Re-measure gaps, update `p-*`/`gap-*` |
| 4 | Border radius | Re-estimate corners, update `rounded-*` |
| 5 | Layout direction | Fix `flex-col`/`flex-row`, alignment |

## Trigger Keywords

Activate on requests containing:
- Korean: "이미지에서 추출", "스크린샷에서", "디자인 이미지", "이미지 기반", "그림에서"
- English: "from image", "from screenshot", "image to code", "design to tailwind"
- Auto-fix: "자동으로", "알아서", "똑같이" / "automatically", "clone", "exactly like"

## Differences from bnt-style-extract

| Aspect | bnt-style-extract | bnt-image-extract |
|--------|-------------------|-------------------|
| Input | Live website URL | Image file (PNG/JPG) |
| Extraction | Playwright DOM access | PIL pixel analysis + Claude Vision |
| Hover states | Captured | Not available (suggest common patterns) |
| Comparison target | Website screenshot | Local image file |

## Cautions

1. **Font estimation**: Font sizes are auto-measured via pixel-level text height analysis (P1). Font weights are estimated via stroke width ratio (P4). Both snap to standard values. Use `--font-search` during comparison to verify.
2. **Anti-aliasing**: Image edges may produce intermediate colors. Text color extraction (P5) uses interior-pixel-only sampling to exclude edge artifacts. The palette extraction filters colors below 0.5% pixel coverage.
3. **Scale dependency**: Extracted pixel dimensions depend on the image resolution. If the design image is scaled, dimensions need proportional adjustment. Use `--auto-viewport` (P6) to match viewport to original image size.
4. **Gradient detection**: Background gradients (P3) require monotonic brightness change of at least 15 RGB units across the region. Subtle or non-linear gradients may not be detected.
5. **Gap measurement**: Element gaps (P2) require at least 2 elements with matching name prefix (e.g., "bar-attack", "bar-magic"). Single elements or differently-named elements won't trigger gap detection.
6. **CSS mechanism limitation**: Image-only extraction cannot detect CSS filters (hue-rotate, sepia, contrast), nested element structures, or hover states. For these, use Step 2.5 hybrid extraction with the source URL.
7. **Hybrid workflow recommended**: When the design source URL is known, always use Step 2.5 hybrid extraction for accurate font sizes and text colors. Image-only extraction has inherent limitations for typography.
