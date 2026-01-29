#!/usr/bin/env python3
"""
Extracts UI styles from design images using PIL/Pillow.
Outputs structured JSON compatible with the bnt-style-extract pipeline.
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime

try:
    from PIL import Image
except ImportError:
    print(json.dumps({
        'success': False,
        'error': 'Pillow not installed. Run: pip install Pillow'
    }), file=sys.stderr)
    sys.exit(1)

# =============================================================================
# Configuration Constants
# =============================================================================

# Default output directory for all generated files
DEFAULT_OUTPUT_DIR = '.image-extract'

# Number of colors after quantization
# 16 covers most UI color palettes without excessive detail
QUANTIZE_COLORS = 16

# Minimum pixel percentage for a color to be considered significant
# Filters noise and anti-aliasing artifacts at component edges
MIN_COLOR_PERCENTAGE = 0.5

# Number of dominant colors to extract by default
# 10 captures primary, secondary, background, text, and accent colors
DEFAULT_PALETTE_SIZE = 10


def extract_color_palette(image, max_colors=DEFAULT_PALETTE_SIZE):
    """
    Extract dominant colors from image using quantization.

    Returns list of color dicts sorted by pixel coverage (descending).
    """
    quantized = image.quantize(
        colors=QUANTIZE_COLORS,
        method=Image.Quantize.MEDIANCUT
    )
    palette_data = quantized.getpalette()
    if not palette_data:
        return []

    color_counts = Counter(quantized.getdata())
    total_pixels = image.size[0] * image.size[1]
    colors = []

    for color_idx, count in color_counts.most_common(max_colors):
        percentage = count / total_pixels * 100
        if percentage < MIN_COLOR_PERCENTAGE:
            continue

        r = palette_data[color_idx * 3]
        g = palette_data[color_idx * 3 + 1]
        b = palette_data[color_idx * 3 + 2]

        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        category = classify_color(luminance, r, g, b)

        colors.append({
            'hex': hex_color,
            'rgb': f'rgb({r}, {g}, {b})',
            'percentage': round(percentage, 2),
            'luminance': round(luminance, 3),
            'category': category
        })

    return colors


def classify_color(luminance, r, g, b):
    """
    Classify color by luminance and saturation.

    Categories: background-dark, background, neutral, text, text-light, text-white, accent
    """
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    saturation = (max_c - min_c) / max_c if max_c > 0 else 0

    # High saturation = accent color regardless of luminance
    if saturation > 0.5:
        return 'accent'

    if luminance < 0.15:
        return 'background-dark'
    elif luminance < 0.4:
        return 'background'
    elif luminance > 0.95:
        return 'text-white'
    elif luminance > 0.85:
        return 'text-light'
    elif luminance > 0.6:
        return 'text'
    else:
        return 'neutral'


# Standard font sizes used in UI design (px)
STANDARD_FONT_SIZES = [12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72]

# Maximum deviation ratio for snapping to a standard size
FONT_SNAP_THRESHOLD = 0.25


# =============================================================================
# P1: Pixel-level text height measurement
# =============================================================================

def measure_text_height(cropped_image, bg_threshold=30):
    """
    Measure actual pixel height occupied by text in a cropped region.

    Analyzes background vs foreground pixels row by row to find
    the topmost and bottommost text rows.

    Args:
        cropped_image: PIL Image (RGB) containing text
        bg_threshold: Max brightness difference to consider as background

    Returns:
        int: Actual text pixel height, or None if measurement fails
    """
    gray = cropped_image.convert('L')
    width, height = gray.size
    if width < 4 or height < 4:
        return None

    pixels = list(gray.getdata())

    # Estimate background level from top/bottom 5% rows (median)
    margin = max(1, height // 20)
    bg_samples = []
    for y in list(range(margin)) + list(range(height - margin, height)):
        row_start = y * width
        bg_samples.extend(pixels[row_start:row_start + width])
    bg_samples.sort()
    bg_level = bg_samples[len(bg_samples) // 2]

    # Calculate text pixel ratio per row
    text_rows = []
    for y in range(height):
        row_start = y * width
        row = pixels[row_start:row_start + width]
        text_pixels = sum(1 for p in row if abs(p - bg_level) > bg_threshold)
        if text_pixels / width > 0.05:
            text_rows.append(y)

    if len(text_rows) < 3:
        return None

    return text_rows[-1] - text_rows[0] + 1


def estimate_font_size(region_height, line_height_ratio=1.5, cropped_image=None):
    """
    Estimate font size from bounding box height.

    When cropped_image is provided, uses pixel-level text height measurement
    for higher accuracy. Falls back to heuristic calculation otherwise.

    Args:
        region_height: Height of the bounding region in pixels
        line_height_ratio: CSS line-height multiplier (default 1.5)
        cropped_image: Optional PIL Image for pixel-level measurement

    Returns:
        Estimated font size in pixels (int)
    """
    # Pixel-level measurement (preferred when available)
    if cropped_image is not None:
        measured_height = measure_text_height(cropped_image)
        if measured_height is not None:
            # text height ~= font-size * 0.72 (cap height ratio)
            raw_size = measured_height / 0.72
            for std_size in STANDARD_FONT_SIZES:
                if abs(raw_size - std_size) / std_size <= FONT_SNAP_THRESHOLD:
                    return std_size
            return max(10, round(raw_size))

    # Fallback: heuristic based on region height
    if region_height < 40:
        padding = 8
    elif region_height < 50:
        padding = 12
    else:
        padding = 16

    raw_size = (region_height - padding) / line_height_ratio

    # Snap to nearest standard size if within threshold
    for std_size in STANDARD_FONT_SIZES:
        if abs(raw_size - std_size) / std_size <= FONT_SNAP_THRESHOLD:
            return std_size

    return max(10, round(raw_size))


# =============================================================================
# P4: Font weight estimation via stroke width analysis
# =============================================================================

def estimate_font_weight(cropped_image, estimated_font_size=16, bg_threshold=30):
    """
    Estimate font weight by analyzing text stroke width.

    Measures horizontal run lengths of text pixels and compares
    the median stroke width to font size ratio.

    Args:
        cropped_image: PIL Image (RGB) containing text
        estimated_font_size: Font size in px (from estimate_font_size)
        bg_threshold: Background detection threshold

    Returns:
        str: CSS font-weight value ('200'-'800') or None
    """
    gray = cropped_image.convert('L')
    width, height = gray.size
    if width < 4 or height < 4:
        return None

    pixels = list(gray.getdata())

    # Estimate background level from corner pixels
    corners = []
    for y in [0, height - 1]:
        for x in [0, width - 1]:
            corners.append(pixels[y * width + x])
    corners.sort()
    bg_level = corners[len(corners) // 2]

    # Collect horizontal run lengths of text pixels
    stroke_widths = []
    for y in range(height):
        in_stroke = False
        run_length = 0
        for x in range(width):
            pixel = pixels[y * width + x]
            is_text = abs(pixel - bg_level) > bg_threshold

            if is_text:
                if not in_stroke:
                    in_stroke = True
                    run_length = 1
                else:
                    run_length += 1
            else:
                if in_stroke:
                    if run_length >= 2:  # noise filter
                        stroke_widths.append(run_length)
                    in_stroke = False
                    run_length = 0

        if in_stroke and run_length >= 2:
            stroke_widths.append(run_length)

    if not stroke_widths:
        return None

    # Median stroke width
    stroke_widths.sort()
    median_stroke = stroke_widths[len(stroke_widths) // 2]

    # Stroke width / font size ratio -> weight mapping
    ratio = median_stroke / max(estimated_font_size, 1)

    if ratio < 0.04:
        return '200'   # extralight
    elif ratio < 0.06:
        return '300'   # light
    elif ratio < 0.09:
        return '400'   # normal
    elif ratio < 0.11:
        return '500'   # medium
    elif ratio < 0.14:
        return '600'   # semibold
    elif ratio < 0.18:
        return '700'   # bold
    else:
        return '800'   # extrabold


# =============================================================================
# P5: Precise text color extraction (interior pixels only)
# =============================================================================

def extract_text_color(cropped_image, bg_threshold=30):
    """
    Extract text foreground color by sampling interior pixels only.

    Excludes edge/anti-aliasing pixels by checking that all 4 neighbors
    are also non-background, then takes median RGB of interior pixels.

    Args:
        cropped_image: PIL Image (RGB) containing text
        bg_threshold: Background detection threshold

    Returns:
        dict with hex/rgb/luminance, or None if too few interior pixels
    """
    gray = cropped_image.convert('L')
    rgb_image = cropped_image.convert('RGB')
    width, height = gray.size
    if width < 6 or height < 6:
        return None

    gray_pixels = list(gray.getdata())
    rgb_pixels = list(rgb_image.getdata())

    # Estimate background level from top/bottom 5% rows
    margin = max(1, height // 20)
    bg_samples = []
    for y in list(range(margin)) + list(range(height - margin, height)):
        for x in range(width):
            bg_samples.append(gray_pixels[y * width + x])
    bg_samples.sort()
    bg_level = bg_samples[len(bg_samples) // 2]

    # Collect interior text pixels (all 4 neighbors are non-background)
    interior_colors = []
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            idx = y * width + x
            if abs(gray_pixels[idx] - bg_level) <= bg_threshold:
                continue  # background pixel

            neighbors = [
                gray_pixels[(y - 1) * width + x],
                gray_pixels[(y + 1) * width + x],
                gray_pixels[y * width + (x - 1)],
                gray_pixels[y * width + (x + 1)],
            ]

            if all(abs(n - bg_level) > bg_threshold for n in neighbors):
                interior_colors.append(rgb_pixels[idx])

    if len(interior_colors) < 5:
        return None

    # Median color by brightness
    interior_colors.sort(key=lambda c: c[0] + c[1] + c[2])
    mid = len(interior_colors) // 2
    r, g, b = interior_colors[mid]

    hex_color = f'#{r:02x}{g:02x}{b:02x}'
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    return {
        'hex': hex_color,
        'rgb': f'rgb({r}, {g}, {b})',
        'luminance': round(luminance, 3)
    }


# =============================================================================
# P3: Background gradient detection
# =============================================================================

def detect_gradient(cropped_image, direction='vertical', num_samples=10,
                    min_change=15):
    """
    Detect directional color gradient in a region.

    Samples color strips along the specified direction and checks
    for monotonic brightness change exceeding min_change threshold.

    Args:
        cropped_image: PIL Image (RGB)
        direction: 'vertical' or 'horizontal'
        num_samples: Number of strips to sample (default 10)
        min_change: Minimum total RGB change to qualify as gradient

    Returns:
        dict with gradient info and Tailwind class, or None
    """
    width, height = cropped_image.size
    if width < 4 or height < 4:
        return None

    samples = []

    if direction == 'vertical':
        for i in range(num_samples):
            y = int(i * (height - 1) / (num_samples - 1))
            # Sample center 60% to avoid edge artifacts
            x_start = width // 5
            x_end = width * 4 // 5
            if x_end <= x_start:
                x_end = x_start + 1
            strip = cropped_image.crop((x_start, y, x_end, min(y + 1, height)))
            pixels = list(strip.getdata())
            if not pixels:
                continue
            avg_r = sum(p[0] for p in pixels) // len(pixels)
            avg_g = sum(p[1] for p in pixels) // len(pixels)
            avg_b = sum(p[2] for p in pixels) // len(pixels)
            samples.append((avg_r, avg_g, avg_b))
    else:
        for i in range(num_samples):
            x = int(i * (width - 1) / (num_samples - 1))
            y_start = height // 5
            y_end = height * 4 // 5
            if y_end <= y_start:
                y_end = y_start + 1
            strip = cropped_image.crop((x, y_start, min(x + 1, width), y_end))
            pixels = list(strip.getdata())
            if not pixels:
                continue
            avg_r = sum(p[0] for p in pixels) // len(pixels)
            avg_g = sum(p[1] for p in pixels) // len(pixels)
            avg_b = sum(p[2] for p in pixels) // len(pixels)
            samples.append((avg_r, avg_g, avg_b))

    if len(samples) < 2:
        return None

    # Total RGB change between first and last sample
    first = samples[0]
    last = samples[-1]
    total_change = sum(abs(a - b) for a, b in zip(first, last))

    if total_change < min_change:
        return None

    # Check monotonic brightness change (with 3-unit tolerance)
    luminances = [0.299 * s[0] + 0.587 * s[1] + 0.114 * s[2] for s in samples]
    increasing = all(
        luminances[i] <= luminances[i + 1] + 3
        for i in range(len(luminances) - 1)
    )
    decreasing = all(
        luminances[i] >= luminances[i + 1] - 3
        for i in range(len(luminances) - 1)
    )

    if not (increasing or decreasing):
        return None

    start_hex = f'#{first[0]:02x}{first[1]:02x}{first[2]:02x}'
    end_hex = f'#{last[0]:02x}{last[1]:02x}{last[2]:02x}'

    if direction == 'vertical':
        tw_direction = 'to-b' if increasing else 'to-t'
    else:
        tw_direction = 'to-r' if increasing else 'to-l'

    # from = gradient start (darker or lighter side)
    if tw_direction in ('to-b', 'to-r'):
        from_color, to_color = start_hex, end_hex
    else:
        from_color, to_color = end_hex, start_hex

    return {
        'hasGradient': True,
        'direction': tw_direction,
        'startColor': start_hex,
        'endColor': end_hex,
        'tailwindClass': f'bg-gradient-{tw_direction} from-[{from_color}] to-[{to_color}]'
    }


# =============================================================================
# P2: Element gap measurement
# =============================================================================

def measure_element_gaps(elements, axis='horizontal'):
    """
    Measure gaps between repeated elements along an axis.

    Args:
        elements: List of bounds dicts [{"x", "y", "w", "h"}, ...]
        axis: 'horizontal' (left-right) or 'vertical' (top-bottom)

    Returns:
        dict with gaps list, mean, median, and Tailwind class, or None
    """
    if len(elements) < 2:
        return None

    if axis == 'horizontal':
        sorted_els = sorted(elements, key=lambda e: e.get('x', 0))
        gaps = []
        for i in range(len(sorted_els) - 1):
            curr_end = sorted_els[i].get('x', 0) + sorted_els[i].get('w', 0)
            next_start = sorted_els[i + 1].get('x', 0)
            gap = next_start - curr_end
            if gap > 0:
                gaps.append(gap)
    else:
        sorted_els = sorted(elements, key=lambda e: e.get('y', 0))
        gaps = []
        for i in range(len(sorted_els) - 1):
            curr_end = sorted_els[i].get('y', 0) + sorted_els[i].get('h', 0)
            next_start = sorted_els[i + 1].get('y', 0)
            gap = next_start - curr_end
            if gap > 0:
                gaps.append(gap)

    if not gaps:
        return None

    gaps.sort()
    mean_gap = sum(gaps) / len(gaps)
    median_gap = gaps[len(gaps) // 2]

    # Tailwind gap class mapping
    tw_gap = _spacing_to_gap_class(round(median_gap))

    return {
        'gaps': gaps,
        'meanGap': round(mean_gap, 1),
        'medianGap': median_gap,
        'tailwindGap': tw_gap
    }


def _spacing_to_gap_class(px):
    """Map pixel value to Tailwind gap class."""
    SPACING_MAP = {
        0: '0', 1: 'px', 2: '0.5', 4: '1', 6: '1.5', 8: '2',
        10: '2.5', 12: '3', 14: '3.5', 16: '4', 20: '5', 24: '6',
        28: '7', 32: '8', 36: '9', 40: '10', 44: '11', 48: '12',
    }
    # Exact match
    if px in SPACING_MAP:
        return f'gap-{SPACING_MAP[px]}'
    # Closest within 2px tolerance
    closest = min(SPACING_MAP.keys(), key=lambda x: abs(x - px))
    if abs(closest - px) <= 2:
        return f'gap-{SPACING_MAP[closest]}'
    return f'gap-[{px}px]'


# =============================================================================
# Core extraction functions
# =============================================================================

def extract_region_styles(image, regions):
    """
    Extract styles from specific image regions.

    Integrates font size/weight estimation, text color precision,
    gradient detection, and gap measurement.

    Args:
        image: PIL Image object
        regions: List of region dicts with 'name' and 'bounds' keys

    Returns:
        List of region style dicts
    """
    results = []
    img_width, img_height = image.size

    for region in regions:
        bounds = region.get('bounds', {})
        x = max(0, bounds.get('x', 0))
        y = max(0, bounds.get('y', 0))
        w = bounds.get('w', 0)
        h = bounds.get('h', 0)

        # Clamp to image boundaries
        x2 = min(x + w, img_width)
        y2 = min(y + h, img_height)

        if x2 <= x or y2 <= y:
            continue

        cropped = image.crop((x, y, x2, y2))
        colors = extract_color_palette(cropped, max_colors=5)

        bg_color = colors[0] if colors else None

        # P3: Detect background gradient
        gradient = detect_gradient(cropped, direction='vertical')
        if not gradient:
            gradient = detect_gradient(cropped, direction='horizontal')

        # Find text color: highest luminance contrast to background (fallback)
        text_color = None
        if bg_color and len(colors) > 1:
            bg_lum = bg_color['luminance']
            best_contrast = 0
            for c in colors[1:]:
                contrast = abs(c['luminance'] - bg_lum)
                if contrast > best_contrast:
                    best_contrast = contrast
                    text_color = c

        # P5: Precise text color from interior pixels (preferred)
        precise_text = extract_text_color(cropped)
        if precise_text:
            text_color = precise_text

        # P1: Font size with pixel-level measurement
        region_h = y2 - y
        estimated_fs = estimate_font_size(region_h, cropped_image=cropped)

        # P4: Font weight via stroke width analysis
        estimated_fw = estimate_font_weight(cropped, estimated_font_size=estimated_fs)

        # Build styles dict
        styles = {
            'backgroundColor': bg_color['rgb'] if bg_color else None,
            'color': text_color['rgb'] if text_color else (
                text_color.get('rgb') if isinstance(text_color, dict) else None
            ),
            'width': f'{x2 - x}px',
            'height': f'{region_h}px',
            'estimatedFontSize': f'{estimated_fs}px',
        }

        if estimated_fw:
            styles['estimatedFontWeight'] = estimated_fw

        if gradient:
            styles['backgroundGradient'] = gradient['tailwindClass']

        region_result = {
            'name': region.get('name', f'region_{len(results)}'),
            'role': region.get('role', 'region'),
            'text': region.get('text', ''),
            'bounds': {'x': x, 'y': y, 'w': x2 - x, 'h': region_h},
            'styles': styles,
            'extractedColors': colors
        }

        if gradient:
            region_result['gradient'] = gradient

        results.append(region_result)

    # P2: Detect repeated element groups and measure gaps
    groups = defaultdict(list)
    for r in results:
        # Group by common name prefix: "bar-attack" -> "bar"
        parts = r['name'].rsplit('-', 1)
        if len(parts) == 2 and parts[0]:
            groups[parts[0]].append(r['bounds'])

    for group_name, bounds_list in groups.items():
        if len(bounds_list) >= 2:
            gap_info = measure_element_gaps(bounds_list, axis='horizontal')
            if not gap_info:
                gap_info = measure_element_gaps(bounds_list, axis='vertical')
            if gap_info:
                results.append({
                    'name': f'{group_name}-gap-info',
                    'role': 'gap-measurement',
                    'text': '',
                    'bounds': {},
                    'styles': {
                        'gap': f'{gap_info["medianGap"]}px'
                    },
                    'gapAnalysis': gap_info
                })

    return results


def build_elements(image, palette, regions_data):
    """
    Build elements array compatible with bnt-style-extract output format.

    This enables reuse of the convert.py pipeline from bnt-style-extract.
    """
    elements = []
    width, height = image.size

    # Classify palette colors
    bg_colors = [c for c in palette if 'background' in c['category']]
    text_colors = [c for c in palette if 'text' in c['category']]

    root_bg = bg_colors[0] if bg_colors else (palette[0] if palette else None)
    root_text = text_colors[0] if text_colors else None

    # Root container element
    root = {
        'selector': 'root-container',
        'tag': 'div',
        'role': 'container',
        'text': '',
        'boundingBox': {
            'x': 0, 'y': 0,
            'width': width, 'height': height
        },
        'styles': {
            'backgroundColor': root_bg['rgb'] if root_bg else None,
            'color': root_text['rgb'] if root_text else None,
            'width': f'{width}px',
            'height': f'{height}px',
            'display': 'flex',
            'flexDirection': 'column'
        }
    }
    elements.append(root)

    # Region elements
    for region in regions_data:
        # Skip gap-measurement pseudo-elements
        if region.get('role') == 'gap-measurement':
            # P2: Propagate gap to root container
            gap_value = region['styles'].get('gap')
            if gap_value:
                root['styles']['gap'] = gap_value
            continue

        styles = dict(region['styles'])

        # Promote estimated values for pipeline compatibility
        if 'estimatedFontSize' in styles:
            styles['fontSize'] = styles.pop('estimatedFontSize')
        if 'estimatedFontWeight' in styles:
            styles['fontWeight'] = styles.pop('estimatedFontWeight')

        el = {
            'selector': region['name'],
            'tag': 'div',
            'role': region.get('role', 'region'),
            'text': region.get('text', ''),
            'boundingBox': {
                'x': region['bounds']['x'],
                'y': region['bounds']['y'],
                'width': region['bounds']['w'],
                'height': region['bounds']['h']
            },
            'styles': styles
        }
        elements.append(el)

    return elements


def main():
    parser = argparse.ArgumentParser(
        description='Extract UI styles from design images'
    )
    parser.add_argument(
        '--image', required=True,
        help='Path to design image (PNG/JPG)'
    )
    parser.add_argument(
        '--regions',
        help='JSON file with region coordinates (from Claude Vision analysis)'
    )
    parser.add_argument(
        '--output', default=f'{DEFAULT_OUTPUT_DIR}/styles.json',
        help='Output file path'
    )
    parser.add_argument(
        '--palette-size', type=int, default=DEFAULT_PALETTE_SIZE,
        help=f'Number of dominant colors to extract (default: {DEFAULT_PALETTE_SIZE})'
    )

    args = parser.parse_args()

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        image = Image.open(args.image).convert('RGB')
        width, height = image.size

        # Extract color palette
        palette = extract_color_palette(image, max_colors=args.palette_size)

        # Categorize palette
        categorized = {}
        for color in palette:
            cat = color['category']
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(color['hex'])

        # Extract region styles if provided
        regions_data = []
        if args.regions:
            with open(args.regions, 'r', encoding='utf-8') as f:
                regions = json.load(f)
            regions_data = extract_region_styles(image, regions)

        # Build pipeline-compatible elements
        elements = build_elements(image, palette, regions_data)

        result = {
            'source': os.path.abspath(args.image),
            'type': 'image',
            'timestamp': datetime.now().isoformat(),
            'dimensions': {'width': width, 'height': height},
            'colorPalette': categorized,
            'dominantColors': palette,
            'elementsCount': len(elements),
            'elements': elements
        }

        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(json.dumps({
            'success': True,
            'dimensions': f'{width}x{height}',
            'colorsExtracted': len(palette),
            'regionsAnalyzed': len(regions_data),
            'elementsCount': len(elements),
            'output': args.output
        }, indent=2))

    except FileNotFoundError:
        print(json.dumps({
            'success': False,
            'error': f'Image file not found: {args.image}'
        }, indent=2), file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
