"""
Spacing utility functions for style extraction.
"""

import re

# Tailwind spacing scale: px value -> Tailwind scale value
SPACING_MAP = {
    0: '0',
    1: 'px',
    2: '0.5',
    4: '1',
    6: '1.5',
    8: '2',
    10: '2.5',
    12: '3',
    14: '3.5',
    16: '4',
    20: '5',
    24: '6',
    28: '7',
    32: '8',
    36: '9',
    40: '10',
    44: '11',
    48: '12',
    56: '14',
    64: '16',
    80: '20',
    96: '24',
    112: '28',
    128: '32',
    144: '36',
    160: '40',
    176: '44',
    192: '48',
    208: '52',
    224: '56',
    240: '60',
    256: '64',
    288: '72',
    320: '80',
    384: '96',
}


def parse_px(value):
    """
    Parse pixel value from CSS string.

    Args:
        value: CSS value string like '16px', '1.5rem', or numeric value

    Returns:
        Float pixel value or None if unparseable
    """
    if value is None:
        return None

    # Handle numeric input
    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip()

    # Try px value
    px_match = re.search(r'([\d.]+)\s*px', value, re.IGNORECASE)
    if px_match:
        return float(px_match.group(1))

    # Try rem value (assume 16px base)
    rem_match = re.search(r'([\d.]+)\s*rem', value, re.IGNORECASE)
    if rem_match:
        return float(rem_match.group(1)) * 16

    # Try em value
    em_match = re.search(r'([\d.]+)\s*em', value, re.IGNORECASE)
    if em_match:
        return float(em_match.group(1)) * 16

    # Try bare number
    num_match = re.match(r'^([\d.]+)$', value)
    if num_match:
        return float(num_match.group(1))

    return None


def spacing_to_tailwind(px, prefix='p', tolerance=2):
    """
    Convert pixel spacing to Tailwind class.

    Args:
        px: Pixel value (number or string)
        prefix: Tailwind prefix ('p', 'px', 'py', 'pt', 'm', 'gap', etc.)
        tolerance: Allowed deviation for rounding to scale (default: 2px)

    Returns:
        Tailwind class string like 'p-4' or 'px-[13px]' for arbitrary values
    """
    # Parse if string
    if isinstance(px, str):
        px = parse_px(px)

    if px is None or px < 0:
        return None

    px = round(px)

    # Exact match
    if px in SPACING_MAP:
        return f'{prefix}-{SPACING_MAP[px]}'

    # Find closest match within tolerance
    closest = min(SPACING_MAP.keys(), key=lambda x: abs(x - px))
    if abs(closest - px) <= tolerance:
        return f'{prefix}-{SPACING_MAP[closest]}'

    # Use arbitrary value
    return f'{prefix}-[{px}px]'


def parse_spacing_shorthand(value):
    """
    Parse CSS spacing shorthand into individual values.

    Args:
        value: CSS shorthand like '10px 20px' or '10px 20px 30px 40px'

    Returns:
        Dict with top, right, bottom, left values or None
    """
    if not value:
        return None

    # Find all px values
    matches = re.findall(r'([\d.]+)px', value)
    if not matches:
        return None

    values = [float(m) for m in matches]

    if len(values) == 1:
        return {
            'top': values[0],
            'right': values[0],
            'bottom': values[0],
            'left': values[0]
        }
    elif len(values) == 2:
        return {
            'top': values[0],
            'right': values[1],
            'bottom': values[0],
            'left': values[1]
        }
    elif len(values) == 3:
        return {
            'top': values[0],
            'right': values[1],
            'bottom': values[2],
            'left': values[1]
        }
    elif len(values) >= 4:
        return {
            'top': values[0],
            'right': values[1],
            'bottom': values[2],
            'left': values[3]
        }

    return None


def optimize_spacing_classes(top, right, bottom, left, prefix='p'):
    """
    Generate optimized Tailwind spacing classes.

    Args:
        top, right, bottom, left: Pixel values
        prefix: 'p' for padding, 'm' for margin

    Returns:
        List of optimized Tailwind classes
    """
    classes = []

    # All same
    if top == right == bottom == left:
        cls = spacing_to_tailwind(top, prefix)
        if cls:
            classes.append(cls)
        return classes

    # Vertical same, horizontal same
    if top == bottom and right == left:
        py = spacing_to_tailwind(top, f'{prefix}y')
        px = spacing_to_tailwind(right, f'{prefix}x')
        if py:
            classes.append(py)
        if px:
            classes.append(px)
        return classes

    # Individual values
    if top:
        cls = spacing_to_tailwind(top, f'{prefix}t')
        if cls:
            classes.append(cls)
    if right:
        cls = spacing_to_tailwind(right, f'{prefix}r')
        if cls:
            classes.append(cls)
    if bottom:
        cls = spacing_to_tailwind(bottom, f'{prefix}b')
        if cls:
            classes.append(cls)
    if left:
        cls = spacing_to_tailwind(left, f'{prefix}l')
        if cls:
            classes.append(cls)

    return classes
