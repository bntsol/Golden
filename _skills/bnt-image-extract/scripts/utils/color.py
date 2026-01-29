"""
Color utility functions for style extraction.
"""

import re
import math


def parse_rgb(rgb_str):
    """
    Parse RGB/RGBA string to tuple.

    Args:
        rgb_str: CSS color string like 'rgb(255, 128, 0)' or 'rgba(255, 128, 0, 0.5)'

    Returns:
        Tuple of (r, g, b) or (r, g, b, a) or None if invalid
    """
    if not rgb_str:
        return None

    # Try RGBA
    rgba_match = re.search(r'rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)', rgb_str)
    if rgba_match:
        r, g, b = map(int, rgba_match.groups()[:3])
        a = float(rgba_match.group(4))
        return (r, g, b, a)

    # Try RGB
    rgb_match = re.search(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', rgb_str)
    if rgb_match:
        return tuple(map(int, rgb_match.groups()))

    return None


def rgb_to_hex(rgb):
    """
    Convert RGB string or tuple to hex string.

    Args:
        rgb: Either a CSS string like 'rgb(255, 128, 0)' or tuple (255, 128, 0)

    Returns:
        Hex string like '#ff8000' or None if invalid
    """
    if not rgb:
        return None

    # Handle string input
    if isinstance(rgb, str):
        if rgb.startswith('#'):
            return rgb.lower()
        if rgb == 'transparent' or 'rgba(0, 0, 0, 0)' in rgb:
            return None
        parsed = parse_rgb(rgb)
        if not parsed:
            return None
        rgb = parsed

    # Handle tuple input
    if isinstance(rgb, (tuple, list)) and len(rgb) >= 3:
        r, g, b = rgb[:3]
        return f'#{int(r):02x}{int(g):02x}{int(b):02x}'

    return None


def hex_to_rgb(hex_str):
    """
    Convert hex string to RGB tuple.

    Args:
        hex_str: Hex color string like '#ff8000' or 'ff8000'

    Returns:
        Tuple of (r, g, b) or None if invalid
    """
    if not hex_str:
        return None

    # Remove # prefix if present
    hex_str = hex_str.lstrip('#')

    # Handle 3-char shorthand
    if len(hex_str) == 3:
        hex_str = ''.join(c * 2 for c in hex_str)

    if len(hex_str) != 6:
        return None

    try:
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return (r, g, b)
    except ValueError:
        return None


def color_distance(color1, color2):
    """
    Calculate perceptual distance between two colors.
    Uses weighted Euclidean distance in RGB space.

    Args:
        color1: RGB tuple or hex string
        color2: RGB tuple or hex string

    Returns:
        Distance value (0-100 scale, lower is more similar)
    """
    # Convert to RGB tuples if needed
    if isinstance(color1, str):
        color1 = hex_to_rgb(color1) or parse_rgb(color1)
    if isinstance(color2, str):
        color2 = hex_to_rgb(color2) or parse_rgb(color2)

    if not color1 or not color2:
        return 100  # Max distance for invalid colors

    r1, g1, b1 = color1[:3]
    r2, g2, b2 = color2[:3]

    # Weighted RGB distance (human eye is more sensitive to green)
    # Using CIE76 approximation weights
    r_weight = 0.30
    g_weight = 0.59
    b_weight = 0.11

    distance = math.sqrt(
        r_weight * (r1 - r2) ** 2 +
        g_weight * (g1 - g2) ** 2 +
        b_weight * (b1 - b2) ** 2
    )

    # Normalize to 0-100 scale
    max_distance = math.sqrt(r_weight * 255**2 + g_weight * 255**2 + b_weight * 255**2)
    return round(distance / max_distance * 100, 2)


def lighten(hex_color, percent):
    """
    Lighten a color by a percentage.

    Args:
        hex_color: Hex color string
        percent: Percentage to lighten (0-100)

    Returns:
        Lightened hex color string
    """
    rgb = hex_to_rgb(hex_color)
    if not rgb:
        return hex_color

    factor = percent / 100
    r = int(rgb[0] + (255 - rgb[0]) * factor)
    g = int(rgb[1] + (255 - rgb[1]) * factor)
    b = int(rgb[2] + (255 - rgb[2]) * factor)

    return rgb_to_hex((r, g, b))


def darken(hex_color, percent):
    """
    Darken a color by a percentage.

    Args:
        hex_color: Hex color string
        percent: Percentage to darken (0-100)

    Returns:
        Darkened hex color string
    """
    rgb = hex_to_rgb(hex_color)
    if not rgb:
        return hex_color

    factor = 1 - (percent / 100)
    r = int(rgb[0] * factor)
    g = int(rgb[1] * factor)
    b = int(rgb[2] * factor)

    return rgb_to_hex((r, g, b))
