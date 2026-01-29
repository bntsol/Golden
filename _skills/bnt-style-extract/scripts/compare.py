#!/usr/bin/env python3
"""
Visual comparison between target website and current implementation.
Calculates similarity percentage using image difference analysis.
"""

import argparse
import json
import os
import sys
import io

# =============================================================================
# Output Directory Configuration
# =============================================================================

# Default output directory for all generated files
# This keeps project root clean and files are easily gitignored
DEFAULT_OUTPUT_DIR = '.style-extract'

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(json.dumps({
        'success': False,
        'error': 'playwright not installed. Run: pip install playwright && playwright install chromium'
    }), file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image, ImageChops
except ImportError:
    print(json.dumps({
        'success': False,
        'error': 'Pillow not installed. Run: pip install Pillow'
    }), file=sys.stderr)
    sys.exit(1)

import math

# =============================================================================
# Configuration Constants
# =============================================================================

# Viewport dimensions for consistent screenshot comparison
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080

# Wait time for page rendering before screenshot
# Allows dynamic content and animations to complete
PAGE_LOAD_WAIT_MS = 2000

# Similarity threshold for passing comparison
# 95% accounts for minor rendering differences across environments
DEFAULT_SIMILARITY_THRESHOLD = 95.0


def capture_screenshot(page, selector=None):
    """Capture screenshot of specific element or viewport."""
    if selector:
        element = page.query_selector(selector)
        if element:
            return element.screenshot()
    return page.screenshot()


def calculate_similarity(img1_bytes, img2_bytes):
    """
    Calculate visual similarity between two images (0-100%).
    Uses Root Mean Square (RMS) difference of pixel values.
    """
    img1 = Image.open(io.BytesIO(img1_bytes)).convert('RGB')
    img2 = Image.open(io.BytesIO(img2_bytes)).convert('RGB')

    # Resize to match if needed
    if img1.size != img2.size:
        # Resize smaller image to larger
        target_size = (
            max(img1.size[0], img2.size[0]),
            max(img1.size[1], img2.size[1])
        )
        img1 = img1.resize(target_size, Image.Resampling.LANCZOS)
        img2 = img2.resize(target_size, Image.Resampling.LANCZOS)

    # Calculate difference
    diff = ImageChops.difference(img1, img2)

    # Calculate RMS
    histogram = diff.histogram()
    sum_squares = sum(
        (value * ((idx % 256) ** 2))
        for idx, value in enumerate(histogram)
    )

    num_pixels = img1.size[0] * img1.size[1] * 3  # 3 channels (RGB)
    rms = math.sqrt(sum_squares / num_pixels)

    # Convert to similarity percentage (0-100)
    # RMS of 0 = 100% similar, RMS of 255 = 0% similar
    similarity = max(0, 100 - (rms / 255 * 100))

    return round(similarity, 2)


def create_diff_image(img1_bytes, img2_bytes, output_path):
    """Create a visual diff image highlighting differences."""
    img1 = Image.open(io.BytesIO(img1_bytes)).convert('RGB')
    img2 = Image.open(io.BytesIO(img2_bytes)).convert('RGB')

    # Resize to match
    if img1.size != img2.size:
        target_size = (
            max(img1.size[0], img2.size[0]),
            max(img1.size[1], img2.size[1])
        )
        img1 = img1.resize(target_size, Image.Resampling.LANCZOS)
        img2 = img2.resize(target_size, Image.Resampling.LANCZOS)

    # Create diff
    diff = ImageChops.difference(img1, img2)

    # Enhance diff visibility
    diff = diff.point(lambda x: min(255, x * 3))

    diff.save(output_path)
    return output_path


def analyze_differences(img1_bytes, img2_bytes):
    """Analyze what types of differences exist."""
    img1 = Image.open(io.BytesIO(img1_bytes)).convert('RGB')
    img2 = Image.open(io.BytesIO(img2_bytes)).convert('RGB')

    if img1.size != img2.size:
        return {'sizesDifferent': True, 'target': img1.size, 'current': img2.size}

    diff = ImageChops.difference(img1, img2)

    # Sample regions for analysis
    width, height = diff.size
    regions = {
        'top': diff.crop((0, 0, width, height // 3)),
        'middle': diff.crop((0, height // 3, width, 2 * height // 3)),
        'bottom': diff.crop((0, 2 * height // 3, width, height))
    }

    region_diffs = {}
    for name, region in regions.items():
        histogram = region.histogram()
        total = sum(histogram)
        non_zero = sum(histogram[1:])  # Skip zero values
        region_diffs[name] = round(non_zero / total * 100, 2) if total > 0 else 0

    return region_diffs


def main():
    parser = argparse.ArgumentParser(description='Visual comparison of websites')
    parser.add_argument('--target', required=True, help='Target URL (original)')
    parser.add_argument('--current', required=True, help='Current implementation URL')
    parser.add_argument('--selector', help='CSS selector for specific element')
    parser.add_argument('--output-dir', default=DEFAULT_OUTPUT_DIR, help='Directory for output files')
    parser.add_argument('--threshold', type=float, default=DEFAULT_SIMILARITY_THRESHOLD,
                        help='Similarity threshold for passing (default: 95)')
    parser.add_argument('--wait', type=int, default=PAGE_LOAD_WAIT_MS,
                        help='Page load wait time in ms')

    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            # Capture target
            page1 = browser.new_page(viewport={'width': VIEWPORT_WIDTH, 'height': VIEWPORT_HEIGHT})
            page1.goto(args.target, wait_until='networkidle', timeout=30000)
            page1.wait_for_timeout(args.wait)
            target_screenshot = capture_screenshot(page1, args.selector)

            # Capture current
            page2 = browser.new_page(viewport={'width': VIEWPORT_WIDTH, 'height': VIEWPORT_HEIGHT})
            page2.goto(args.current, wait_until='networkidle', timeout=30000)
            page2.wait_for_timeout(args.wait)
            current_screenshot = capture_screenshot(page2, args.selector)

            # Calculate similarity
            similarity = calculate_similarity(target_screenshot, current_screenshot)

            # Save screenshots
            target_path = f'{args.output_dir}/target.png'
            current_path = f'{args.output_dir}/current.png'
            diff_path = f'{args.output_dir}/diff.png'

            with open(target_path, 'wb') as f:
                f.write(target_screenshot)
            with open(current_path, 'wb') as f:
                f.write(current_screenshot)

            # Create diff image
            create_diff_image(target_screenshot, current_screenshot, diff_path)

            # Analyze differences
            region_analysis = analyze_differences(target_screenshot, current_screenshot)

            passed = similarity >= args.threshold

            result = {
                'success': True,
                'similarity': similarity,
                'threshold': args.threshold,
                'passed': passed,
                'regionAnalysis': region_analysis,
                'screenshots': {
                    'target': target_path,
                    'current': current_path,
                    'diff': diff_path
                }
            }

            if not passed:
                result['recommendations'] = []

                if similarity < 80:
                    result['recommendations'].append('Large difference detected. Check overall layout and structure.')

                if isinstance(region_analysis, dict) and 'sizesDifferent' not in region_analysis:
                    if region_analysis.get('top', 0) > 30:
                        result['recommendations'].append('Header/top area has significant differences.')
                    if region_analysis.get('middle', 0) > 30:
                        result['recommendations'].append('Main content area has differences. Check colors and spacing.')
                    if region_analysis.get('bottom', 0) > 30:
                        result['recommendations'].append('Footer/bottom area has differences.')

                result['recommendations'].extend([
                    'Verify background colors match exactly.',
                    'Check padding and margin values.',
                    'Confirm border-radius values.',
                    'Ensure font sizes and weights match.'
                ])

            print(json.dumps(result, indent=2))

        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }, indent=2), file=sys.stderr)
            sys.exit(1)

        finally:
            browser.close()


if __name__ == '__main__':
    main()
