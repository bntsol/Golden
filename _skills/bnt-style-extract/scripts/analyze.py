#!/usr/bin/env python3
"""
Analyzes extracted styles to identify patterns, color palettes,
spacing scales, and component types.
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict


def parse_rgb(rgb_str):
    """Parse RGB/RGBA string to tuple."""
    if not rgb_str:
        return None
    match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgb_str)
    if match:
        return tuple(map(int, match.groups()))
    return None


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string."""
    if not rgb:
        return None
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


def parse_px(value):
    """Parse pixel value to number."""
    if not value:
        return None
    match = re.search(r'([\d.]+)px', str(value))
    return float(match.group(1)) if match else None


def categorize_color(hex_color):
    """Categorize color as primary, background, text, or accent."""
    if not hex_color:
        return None

    # Convert to RGB for analysis
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    # Calculate luminance
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    # Categorize based on luminance and saturation
    if luminance < 0.2:
        return 'background'
    elif luminance > 0.8:
        return 'text'
    else:
        # Check if it's a saturated color (potential primary/accent)
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        saturation = (max_c - min_c) / max_c if max_c > 0 else 0

        if saturation > 0.5:
            return 'primary'
        else:
            return 'neutral'


def analyze_colors(elements):
    """Extract and categorize color palette."""
    colors = defaultdict(set)

    for el in elements:
        styles = el.get('styles', {})

        # Background colors
        bg = rgb_to_hex(parse_rgb(styles.get('backgroundColor')))
        if bg:
            category = categorize_color(bg)
            if category:
                colors[category].add(bg)

        # Text colors
        text = rgb_to_hex(parse_rgb(styles.get('color')))
        if text:
            colors['text'].add(text)

        # Border colors
        border = rgb_to_hex(parse_rgb(styles.get('borderColor')))
        if border and border != bg:
            colors['border'].add(border)

        # Hover states
        hover = el.get('states', {}).get('hover', {})
        if hover:
            hover_bg = rgb_to_hex(parse_rgb(hover.get('backgroundColor')))
            if hover_bg:
                colors['hover'].add(hover_bg)

    return {k: sorted(list(v)) for k, v in colors.items() if v}


def analyze_spacing(elements):
    """Extract spacing scale from elements."""
    spacings = []

    for el in elements:
        styles = el.get('styles', {})

        for prop in ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
                     'marginTop', 'marginRight', 'marginBottom', 'marginLeft', 'gap']:
            px = parse_px(styles.get(prop))
            if px and px > 0:
                spacings.append(int(round(px)))

    # Find most common spacing values
    counter = Counter(spacings)
    common = [s for s, _ in counter.most_common(10)]

    # Round to common scale values
    scale = sorted(set(round(s / 4) * 4 for s in common if s <= 96))

    return scale


def analyze_border_radii(elements):
    """Extract border radius values."""
    radii = []

    for el in elements:
        styles = el.get('styles', {})
        radius = styles.get('borderRadius', '')

        # Parse potentially multiple values
        matches = re.findall(r'([\d.]+)px', radius)
        for m in matches:
            radii.append(int(round(float(m))))

    counter = Counter(radii)
    return sorted([r for r, _ in counter.most_common(8) if r > 0])


def analyze_typography(elements):
    """Extract typography patterns."""
    font_sizes = []
    font_weights = []
    font_families = set()

    for el in elements:
        styles = el.get('styles', {})

        size = parse_px(styles.get('fontSize'))
        if size:
            font_sizes.append(int(round(size)))

        weight = styles.get('fontWeight')
        if weight:
            font_weights.append(weight)

        family = styles.get('fontFamily', '')
        if family:
            # Extract first font family
            first_font = family.split(',')[0].strip().strip('"\'')
            if first_font:
                font_families.add(first_font)

    return {
        'sizes': sorted(set(font_sizes)),
        'weights': sorted(set(font_weights)),
        'families': list(font_families)
    }


def analyze_component_types(elements):
    """Identify component types present."""
    types = set()

    for el in elements:
        tag = el.get('tag', '').lower()
        role = el.get('role', '').lower()
        selector = el.get('selector', '').lower()

        if tag == 'button' or role == 'button' or 'btn' in selector or 'button' in selector:
            types.add('button')
        if tag == 'input' or tag == 'textarea':
            types.add('input')
        if 'card' in selector:
            types.add('card')
        if 'chip' in selector or 'tag' in selector or 'badge' in selector:
            types.add('chip')
        if tag == 'a' or role == 'link':
            types.add('link')
        if 'nav' in selector or role == 'navigation':
            types.add('navigation')

    return sorted(list(types))


def analyze_layout_patterns(elements):
    """Identify common layout patterns."""
    patterns = {
        'flex': 0,
        'grid': 0,
        'block': 0,
        'inline': 0
    }

    flex_directions = []

    for el in elements:
        styles = el.get('styles', {})
        display = styles.get('display', '')

        if 'flex' in display:
            patterns['flex'] += 1
            direction = styles.get('flexDirection')
            if direction:
                flex_directions.append(direction)
        elif 'grid' in display:
            patterns['grid'] += 1
        elif 'inline' in display:
            patterns['inline'] += 1
        else:
            patterns['block'] += 1

    return {
        'displayTypes': {k: v for k, v in patterns.items() if v > 0},
        'flexDirections': list(set(flex_directions))
    }


def main():
    parser = argparse.ArgumentParser(description='Analyze extracted styles')
    parser.add_argument('--input', required=True, help='Input JSON file from extract.py')
    parser.add_argument('--output', default='analysis.json', help='Output file path')

    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)

        elements = data.get('elements', [])

        analysis = {
            'source': data.get('url'),
            'elementsAnalyzed': len(elements),
            'colorPalette': analyze_colors(elements),
            'spacingScale': analyze_spacing(elements),
            'borderRadii': analyze_border_radii(elements),
            'typography': analyze_typography(elements),
            'componentTypes': analyze_component_types(elements),
            'layoutPatterns': analyze_layout_patterns(elements)
        }

        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        print(json.dumps({
            'success': True,
            'output': args.output,
            'summary': {
                'colors': len([c for cats in analysis['colorPalette'].values() for c in cats]),
                'spacingValues': len(analysis['spacingScale']),
                'componentTypes': len(analysis['componentTypes'])
            }
        }, indent=2))

    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
