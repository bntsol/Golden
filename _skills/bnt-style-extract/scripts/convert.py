#!/usr/bin/env python3
"""
Converts extracted CSS styles to Tailwind CSS classes.
"""

import argparse
import json
import os
import re
import sys

# =============================================================================
# Output Directory Configuration
# =============================================================================

# Default output directory for all generated files
# This keeps project root clean and files are easily gitignored
DEFAULT_OUTPUT_DIR = '.style-extract'

# =============================================================================
# Tailwind Mapping Tables
# =============================================================================

# Spacing: px value -> Tailwind scale value
SPACING_MAP = {
    0: '0', 1: 'px', 2: '0.5', 4: '1', 6: '1.5', 8: '2',
    10: '2.5', 12: '3', 14: '3.5', 16: '4', 20: '5',
    24: '6', 28: '7', 32: '8', 36: '9', 40: '10',
    44: '11', 48: '12', 56: '14', 64: '16', 80: '20',
    96: '24', 112: '28', 128: '32'
}

# Font sizes: px -> Tailwind class
FONT_SIZE_MAP = {
    12: 'text-xs', 14: 'text-sm', 16: 'text-base',
    18: 'text-lg', 20: 'text-xl', 24: 'text-2xl',
    30: 'text-3xl', 36: 'text-4xl', 48: 'text-5xl',
    60: 'text-6xl', 72: 'text-7xl', 96: 'text-8xl'
}

# Border radius: px -> Tailwind class
RADIUS_MAP = {
    0: 'rounded-none', 2: 'rounded-sm', 4: 'rounded',
    6: 'rounded-md', 8: 'rounded-lg', 12: 'rounded-xl',
    16: 'rounded-2xl', 24: 'rounded-3xl', 9999: 'rounded-full'
}

# Font weight: CSS value -> Tailwind class
WEIGHT_MAP = {
    '100': 'font-thin', '200': 'font-extralight', '300': 'font-light',
    '400': 'font-normal', '500': 'font-medium', '600': 'font-semibold',
    '700': 'font-bold', '800': 'font-extrabold', '900': 'font-black'
}

# Common color names
COMMON_COLORS = {
    '#000000': 'black',
    '#ffffff': 'white',
    '#f8fafc': 'slate-50',
    '#f1f5f9': 'slate-100',
    '#e2e8f0': 'slate-200',
    '#cbd5e1': 'slate-300',
    '#94a3b8': 'slate-400',
    '#64748b': 'slate-500',
    '#475569': 'slate-600',
    '#334155': 'slate-700',
    '#1e293b': 'slate-800',
    '#0f172a': 'slate-900',
}


def parse_px(value):
    """Extract pixel value from CSS string."""
    if not value:
        return None
    match = re.search(r'([\d.]+)px', str(value))
    return float(match.group(1)) if match else None


def rgb_to_hex(rgb):
    """Convert RGB/RGBA string to hex."""
    if not rgb or rgb == 'transparent' or rgb == 'rgba(0, 0, 0, 0)':
        return None

    match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgb)
    if match:
        r, g, b = map(int, match.groups())
        return f'#{r:02x}{g:02x}{b:02x}'

    if rgb.startswith('#'):
        return rgb.lower()

    return None


def spacing_to_tailwind(px, prefix='p'):
    """Convert pixel spacing to Tailwind class."""
    if px is None or px < 0:
        return None

    px = int(round(px))

    # Exact match
    if px in SPACING_MAP:
        return f'{prefix}-{SPACING_MAP[px]}'

    # Find closest match within 2px tolerance
    closest = min(SPACING_MAP.keys(), key=lambda x: abs(x - px))
    if abs(closest - px) <= 2:
        return f'{prefix}-{SPACING_MAP[closest]}'

    # Arbitrary value
    return f'{prefix}-[{px}px]'


def color_to_tailwind(rgb, prefix='bg'):
    """Convert color to Tailwind class."""
    hex_color = rgb_to_hex(rgb)
    if not hex_color:
        return None

    # Check common colors
    if hex_color.lower() in COMMON_COLORS:
        return f'{prefix}-{COMMON_COLORS[hex_color.lower()]}'

    # Use arbitrary value
    return f'{prefix}-[{hex_color}]'


def font_size_to_tailwind(px):
    """Convert font size to Tailwind class."""
    if px is None:
        return None

    px = int(round(px))

    # Exact match
    if px in FONT_SIZE_MAP:
        return FONT_SIZE_MAP[px]

    # Find closest match within 1px tolerance
    closest = min(FONT_SIZE_MAP.keys(), key=lambda x: abs(x - px))
    if abs(closest - px) <= 1:
        return FONT_SIZE_MAP[closest]

    # Arbitrary value
    return f'text-[{px}px]'


def radius_to_tailwind(value):
    """Convert border-radius to Tailwind class."""
    px = parse_px(value)
    if px is None:
        return None

    px = int(round(px))

    # Full circle check
    if px >= 9999 or px >= 999:
        return 'rounded-full'

    # Exact match
    if px in RADIUS_MAP:
        return RADIUS_MAP[px]

    # Find closest match within 2px tolerance
    closest = min(RADIUS_MAP.keys(), key=lambda x: abs(x - px))
    if abs(closest - px) <= 2:
        return RADIUS_MAP[closest]

    # Arbitrary value
    return f'rounded-[{px}px]'


def convert_element_styles(styles, hover_styles=None):
    """Convert element styles to Tailwind classes string."""
    classes = []

    # Background color
    bg = color_to_tailwind(styles.get('backgroundColor'), 'bg')
    if bg and 'rgba(0, 0, 0, 0)' not in styles.get('backgroundColor', ''):
        classes.append(bg)

    # Text color
    text_color = color_to_tailwind(styles.get('color'), 'text')
    if text_color:
        classes.append(text_color)

    # Font size
    font_size = font_size_to_tailwind(parse_px(styles.get('fontSize')))
    if font_size:
        classes.append(font_size)

    # Font weight
    font_weight = styles.get('fontWeight')
    if font_weight and font_weight in WEIGHT_MAP:
        classes.append(WEIGHT_MAP[font_weight])

    # Padding
    pt = parse_px(styles.get('paddingTop'))
    pr = parse_px(styles.get('paddingRight'))
    pb = parse_px(styles.get('paddingBottom'))
    pl = parse_px(styles.get('paddingLeft'))

    # Check for uniform padding
    if pt == pr == pb == pl and pt is not None:
        p_class = spacing_to_tailwind(pt, 'p')
        if p_class:
            classes.append(p_class)
    else:
        # Vertical padding (py)
        if pt == pb and pt is not None:
            py_class = spacing_to_tailwind(pt, 'py')
            if py_class:
                classes.append(py_class)
        else:
            if pt:
                classes.append(spacing_to_tailwind(pt, 'pt') or '')
            if pb:
                classes.append(spacing_to_tailwind(pb, 'pb') or '')

        # Horizontal padding (px)
        if pr == pl and pr is not None:
            px_class = spacing_to_tailwind(pr, 'px')
            if px_class:
                classes.append(px_class)
        else:
            if pr:
                classes.append(spacing_to_tailwind(pr, 'pr') or '')
            if pl:
                classes.append(spacing_to_tailwind(pl, 'pl') or '')

    # Border radius
    radius = radius_to_tailwind(styles.get('borderRadius'))
    if radius:
        classes.append(radius)

    # Border
    border_width = parse_px(styles.get('borderWidth'))
    if border_width and border_width > 0:
        if border_width == 1:
            classes.append('border')
        else:
            classes.append(f'border-{int(border_width)}')

        border_color = color_to_tailwind(styles.get('borderColor'), 'border')
        if border_color:
            classes.append(border_color)

    # Display & Flex
    display = styles.get('display', '')
    if 'flex' in display:
        classes.append('flex')

        flex_dir = styles.get('flexDirection')
        if flex_dir == 'column':
            classes.append('flex-col')

        align = styles.get('alignItems')
        align_map = {
            'center': 'items-center',
            'flex-start': 'items-start',
            'flex-end': 'items-end',
            'stretch': 'items-stretch'
        }
        if align in align_map:
            classes.append(align_map[align])

        justify = styles.get('justifyContent')
        justify_map = {
            'center': 'justify-center',
            'flex-start': 'justify-start',
            'flex-end': 'justify-end',
            'space-between': 'justify-between',
            'space-around': 'justify-around'
        }
        if justify in justify_map:
            classes.append(justify_map[justify])

    # Gap
    gap = parse_px(styles.get('gap'))
    if gap:
        gap_class = spacing_to_tailwind(gap, 'gap')
        if gap_class:
            classes.append(gap_class)

    # Hover states
    if hover_styles:
        hover_bg = color_to_tailwind(hover_styles.get('backgroundColor'), 'hover:bg')
        if hover_bg and hover_bg != bg:
            classes.append(hover_bg)

        hover_text = color_to_tailwind(hover_styles.get('color'), 'hover:text')
        if hover_text and hover_text != text_color:
            classes.append(hover_text)

        # Add transition if hover effects present
        if hover_bg or hover_text:
            classes.append('transition-all')
            classes.append('duration-200')

    # Filter empty strings and return
    return ' '.join(filter(None, classes))


def main():
    parser = argparse.ArgumentParser(description='Convert styles to Tailwind CSS')
    parser.add_argument('--input', required=True, help='Input JSON file from extract.py')
    parser.add_argument('--output', default=f'{DEFAULT_OUTPUT_DIR}/tailwind.json', help='Output file path')

    args = parser.parse_args()

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)

        results = []
        custom_colors = {}

        for element in data.get('elements', []):
            styles = element.get('styles', {})
            hover_styles = element.get('states', {}).get('hover')

            tailwind_classes = convert_element_styles(styles, hover_styles)

            # Collect custom colors for config
            bg_hex = rgb_to_hex(styles.get('backgroundColor'))
            if bg_hex and bg_hex.lower() not in COMMON_COLORS:
                color_name = f'custom-{len(custom_colors)}'
                custom_colors[color_name] = bg_hex

            results.append({
                'selector': element.get('selector'),
                'tag': element.get('tag'),
                'role': element.get('role'),
                'text': element.get('text'),
                'tailwindClasses': tailwind_classes,
                'originalStyles': {
                    'backgroundColor': styles.get('backgroundColor'),
                    'color': styles.get('color'),
                    'padding': styles.get('padding'),
                    'borderRadius': styles.get('borderRadius'),
                    'fontSize': styles.get('fontSize')
                }
            })

        output = {
            'source': data.get('url'),
            'elementsConverted': len(results),
            'elements': results,
            'configExtensions': {
                'colors': custom_colors
            } if custom_colors else None
        }

        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(json.dumps({
            'success': True,
            'elementsConverted': len(results),
            'customColors': len(custom_colors),
            'output': args.output
        }, indent=2))

    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
