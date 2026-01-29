"""
BNT Style Extract Utilities

Common utility functions for style extraction and conversion.
"""

from .color import rgb_to_hex, hex_to_rgb, parse_rgb, color_distance
from .spacing import parse_px, spacing_to_tailwind, SPACING_MAP
from .tailwind import (
    convert_to_tailwind,
    FONT_SIZE_MAP,
    RADIUS_MAP,
    WEIGHT_MAP
)

__all__ = [
    'rgb_to_hex',
    'hex_to_rgb',
    'parse_rgb',
    'color_distance',
    'parse_px',
    'spacing_to_tailwind',
    'SPACING_MAP',
    'convert_to_tailwind',
    'FONT_SIZE_MAP',
    'RADIUS_MAP',
    'WEIGHT_MAP',
]
