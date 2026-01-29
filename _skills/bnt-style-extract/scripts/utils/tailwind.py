"""
Tailwind CSS conversion utilities.
"""

import re
from .color import rgb_to_hex
from .spacing import parse_px, spacing_to_tailwind

# Font size mapping: px -> Tailwind class
FONT_SIZE_MAP = {
    12: 'text-xs',
    14: 'text-sm',
    16: 'text-base',
    18: 'text-lg',
    20: 'text-xl',
    24: 'text-2xl',
    30: 'text-3xl',
    36: 'text-4xl',
    48: 'text-5xl',
    60: 'text-6xl',
    72: 'text-7xl',
    96: 'text-8xl',
    128: 'text-9xl',
}

# Border radius mapping: px -> Tailwind class
RADIUS_MAP = {
    0: 'rounded-none',
    2: 'rounded-sm',
    4: 'rounded',
    6: 'rounded-md',
    8: 'rounded-lg',
    12: 'rounded-xl',
    16: 'rounded-2xl',
    24: 'rounded-3xl',
    9999: 'rounded-full',
}

# Font weight mapping: CSS value -> Tailwind class
WEIGHT_MAP = {
    '100': 'font-thin',
    '200': 'font-extralight',
    '300': 'font-light',
    '400': 'font-normal',
    '500': 'font-medium',
    '600': 'font-semibold',
    '700': 'font-bold',
    '800': 'font-extrabold',
    '900': 'font-black',
}

# Common colors for direct mapping
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
    '#020617': 'slate-950',
}


def font_size_to_tailwind(value, tolerance=1):
    """
    Convert font size to Tailwind class.

    Args:
        value: CSS font-size value (px string or number)
        tolerance: Allowed px deviation for rounding

    Returns:
        Tailwind class string
    """
    px = parse_px(value)
    if px is None:
        return None

    px = round(px)

    # Exact match
    if px in FONT_SIZE_MAP:
        return FONT_SIZE_MAP[px]

    # Find closest within tolerance
    closest = min(FONT_SIZE_MAP.keys(), key=lambda x: abs(x - px))
    if abs(closest - px) <= tolerance:
        return FONT_SIZE_MAP[closest]

    # Arbitrary value
    return f'text-[{px}px]'


def radius_to_tailwind(value, tolerance=2):
    """
    Convert border-radius to Tailwind class.

    Args:
        value: CSS border-radius value
        tolerance: Allowed px deviation for rounding

    Returns:
        Tailwind class string
    """
    px = parse_px(value)
    if px is None:
        return None

    px = round(px)

    # Full circle check
    if px >= 999:
        return 'rounded-full'

    # Exact match
    if px in RADIUS_MAP:
        return RADIUS_MAP[px]

    # Find closest within tolerance
    closest = min(RADIUS_MAP.keys(), key=lambda x: abs(x - px))
    if abs(closest - px) <= tolerance:
        return RADIUS_MAP[closest]

    # Arbitrary value
    return f'rounded-[{px}px]'


def weight_to_tailwind(value):
    """
    Convert font-weight to Tailwind class.

    Args:
        value: CSS font-weight value (number or string)

    Returns:
        Tailwind class string or None
    """
    value = str(value).strip()
    return WEIGHT_MAP.get(value)


def color_to_tailwind(value, prefix='bg'):
    """
    Convert color value to Tailwind class.

    Args:
        value: CSS color value (rgb, rgba, hex)
        prefix: Tailwind prefix ('bg', 'text', 'border', etc.)

    Returns:
        Tailwind class string or None
    """
    hex_color = rgb_to_hex(value)
    if not hex_color:
        return None

    # Check common colors
    hex_lower = hex_color.lower()
    if hex_lower in COMMON_COLORS:
        return f'{prefix}-{COMMON_COLORS[hex_lower]}'

    # Use arbitrary value
    return f'{prefix}-[{hex_color}]'


def shadow_to_tailwind(value):
    """
    Convert box-shadow to Tailwind class.

    Args:
        value: CSS box-shadow value

    Returns:
        Tailwind class string or None
    """
    if not value or value == 'none':
        return None

    value = value.lower()

    # Common shadow patterns
    if 'inset' in value:
        return 'shadow-inner'

    # Try to match blur amount
    blur_match = re.search(r'(\d+)px\s+(\d+)px\s+(\d+)px', value)
    if blur_match:
        blur = int(blur_match.group(3))

        if blur <= 2:
            return 'shadow-sm'
        elif blur <= 4:
            return 'shadow'
        elif blur <= 8:
            return 'shadow-md'
        elif blur <= 15:
            return 'shadow-lg'
        elif blur <= 25:
            return 'shadow-xl'
        else:
            return 'shadow-2xl'

    return 'shadow'


def convert_to_tailwind(styles, include_hover=True):
    """
    Convert a styles dictionary to Tailwind classes string.

    Args:
        styles: Dictionary of CSS properties and values
        include_hover: Whether to include hover state classes

    Returns:
        Space-separated string of Tailwind classes
    """
    classes = []

    # Background
    bg = color_to_tailwind(styles.get('backgroundColor'), 'bg')
    if bg:
        classes.append(bg)

    # Text color
    text_color = color_to_tailwind(styles.get('color'), 'text')
    if text_color:
        classes.append(text_color)

    # Font size
    font_size = font_size_to_tailwind(styles.get('fontSize'))
    if font_size:
        classes.append(font_size)

    # Font weight
    font_weight = weight_to_tailwind(styles.get('fontWeight'))
    if font_weight:
        classes.append(font_weight)

    # Padding
    pt = parse_px(styles.get('paddingTop'))
    pr = parse_px(styles.get('paddingRight'))
    pb = parse_px(styles.get('paddingBottom'))
    pl = parse_px(styles.get('paddingLeft'))

    if pt == pr == pb == pl and pt:
        p = spacing_to_tailwind(pt, 'p')
        if p:
            classes.append(p)
    else:
        if pt == pb and pt:
            py = spacing_to_tailwind(pt, 'py')
            if py:
                classes.append(py)
        if pr == pl and pr:
            px = spacing_to_tailwind(pr, 'px')
            if px:
                classes.append(px)

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

    # Box shadow
    shadow = shadow_to_tailwind(styles.get('boxShadow'))
    if shadow:
        classes.append(shadow)

    # Display flex
    display = styles.get('display', '')
    if 'flex' in display:
        classes.append('flex')

        if styles.get('flexDirection') == 'column':
            classes.append('flex-col')

        align_map = {
            'center': 'items-center',
            'flex-start': 'items-start',
            'flex-end': 'items-end',
        }
        align = align_map.get(styles.get('alignItems'))
        if align:
            classes.append(align)

        justify_map = {
            'center': 'justify-center',
            'flex-start': 'justify-start',
            'flex-end': 'justify-end',
            'space-between': 'justify-between',
        }
        justify = justify_map.get(styles.get('justifyContent'))
        if justify:
            classes.append(justify)

    # Gap
    gap = parse_px(styles.get('gap'))
    if gap:
        gap_class = spacing_to_tailwind(gap, 'gap')
        if gap_class:
            classes.append(gap_class)

    return ' '.join(classes)
