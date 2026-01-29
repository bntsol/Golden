#!/usr/bin/env python3
"""
Visual comparison between original design image and current implementation.
Calculates similarity percentage using RMS image difference.

Supports two modes:
  - --current-url: Screenshots the URL via Playwright
  - --current-image: Uses an existing screenshot file
"""

import argparse
import io
import json
import math
import os
import sys

try:
    from PIL import Image, ImageChops
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

# Viewport dimensions for Playwright screenshot
# Matches bnt-style-extract for consistency
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080

# Wait time for page rendering before screenshot
# Allows dynamic content and animations to complete
PAGE_LOAD_WAIT_MS = 2000

# Similarity threshold for passing comparison
# 95% accounts for minor rendering differences (anti-aliasing, subpixel)
DEFAULT_SIMILARITY_THRESHOLD = 95.0

# Difference enhancement multiplier for diff image visualization
# 3x makes subtle differences visible in the diff output
DIFF_ENHANCE_FACTOR = 3


def load_original_image(path):
    """Load original design image from file."""
    img = Image.open(path).convert('RGB')
    return img


def capture_current_screenshot(url, selector=None, wait_ms=PAGE_LOAD_WAIT_MS,
                               viewport_width=VIEWPORT_WIDTH,
                               viewport_height=VIEWPORT_HEIGHT):
    """Capture screenshot of current implementation via Playwright."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(json.dumps({
            'success': False,
            'error': 'Playwright not installed. Run: pip install playwright && playwright install chromium'
        }), file=sys.stderr)
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={'width': viewport_width, 'height': viewport_height}
        )

        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(wait_ms)

            if selector:
                element = page.query_selector(selector)
                if element:
                    screenshot_bytes = element.screenshot()
                else:
                    print(json.dumps({
                        'success': False,
                        'error': f'Selector not found: {selector}'
                    }), file=sys.stderr)
                    sys.exit(1)
            else:
                screenshot_bytes = page.screenshot()

            return Image.open(io.BytesIO(screenshot_bytes)).convert('RGB')

        finally:
            browser.close()


def calculate_similarity(img1, img2):
    """
    Calculate visual similarity between two PIL Images (0-100%).
    Uses Root Mean Square (RMS) difference of pixel values.
    """
    # Resize to match if needed
    if img1.size != img2.size:
        target_size = (
            max(img1.size[0], img2.size[0]),
            max(img1.size[1], img2.size[1])
        )
        img1 = img1.resize(target_size, Image.Resampling.LANCZOS)
        img2 = img2.resize(target_size, Image.Resampling.LANCZOS)

    diff = ImageChops.difference(img1, img2)
    histogram = diff.histogram()

    sum_squares = sum(
        value * ((idx % 256) ** 2)
        for idx, value in enumerate(histogram)
    )

    # 3 channels (RGB)
    num_pixels = img1.size[0] * img1.size[1] * 3
    rms = math.sqrt(sum_squares / num_pixels)

    # RMS 0 = 100% similar, RMS 255 = 0% similar
    similarity = max(0, 100 - (rms / 255 * 100))
    return round(similarity, 2)


def calculate_ssim(img1, img2, window_size=11, k1=0.01, k2=0.03):
    """
    Calculate Structural Similarity Index (SSIM) between two PIL Images.
    PIL-only implementation - no external dependencies beyond Pillow.

    Uses grayscale conversion and sliding window approach with step size
    of window_size//2 for performance (~4x faster than pixel-by-pixel).

    Args:
        img1, img2: PIL Image objects (RGB)
        window_size: Size of comparison window (default 11x11)
        k1, k2: SSIM stabilization constants

    Returns:
        SSIM score 0-100 (percentage)
    """
    # Resize to match if needed
    if img1.size != img2.size:
        target_size = (
            max(img1.size[0], img2.size[0]),
            max(img1.size[1], img2.size[1])
        )
        img1 = img1.resize(target_size, Image.Resampling.LANCZOS)
        img2 = img2.resize(target_size, Image.Resampling.LANCZOS)

    # Convert to grayscale
    g1 = img1.convert('L')
    g2 = img2.convert('L')

    width, height = g1.size
    p1 = list(g1.getdata())
    p2 = list(g2.getdata())

    # Dynamic range
    L = 255
    c1 = (k1 * L) ** 2
    c2 = (k2 * L) ** 2

    step = max(1, window_size // 2)
    ssim_values = []

    for y in range(0, height - window_size + 1, step):
        for x in range(0, width - window_size + 1, step):
            # Extract window pixels
            win1 = []
            win2 = []
            for wy in range(window_size):
                row_offset = (y + wy) * width + x
                win1.extend(p1[row_offset:row_offset + window_size])
                win2.extend(p2[row_offset:row_offset + window_size])

            n = len(win1)
            if n == 0:
                continue

            # Mean
            mu1 = sum(win1) / n
            mu2 = sum(win2) / n

            # Variance and covariance
            sigma1_sq = sum((v - mu1) ** 2 for v in win1) / n
            sigma2_sq = sum((v - mu2) ** 2 for v in win2) / n
            sigma12 = sum((a - mu1) * (b - mu2) for a, b in zip(win1, win2)) / n

            # SSIM formula
            numerator = (2 * mu1 * mu2 + c1) * (2 * sigma12 + c2)
            denominator = (mu1 ** 2 + mu2 ** 2 + c1) * (sigma1_sq + sigma2_sq + c2)

            ssim_values.append(numerator / denominator if denominator > 0 else 0)

    if not ssim_values:
        return 0.0

    mean_ssim = sum(ssim_values) / len(ssim_values)
    # Convert from [-1,1] range to 0-100 percentage
    return round(max(0, mean_ssim * 100), 2)


def create_diff_image(img1, img2, output_path):
    """Create a visual diff image highlighting differences."""
    if img1.size != img2.size:
        target_size = (
            max(img1.size[0], img2.size[0]),
            max(img1.size[1], img2.size[1])
        )
        img1 = img1.resize(target_size, Image.Resampling.LANCZOS)
        img2 = img2.resize(target_size, Image.Resampling.LANCZOS)

    diff = ImageChops.difference(img1, img2)
    # Enhance visibility of subtle differences
    diff = diff.point(lambda x: min(255, x * DIFF_ENHANCE_FACTOR))
    diff.save(output_path)
    return output_path


def analyze_differences(img1, img2):
    """Analyze what types of differences exist by region."""
    if img1.size != img2.size:
        return {
            'sizesDifferent': True,
            'original': {'width': img1.size[0], 'height': img1.size[1]},
            'current': {'width': img2.size[0], 'height': img2.size[1]},
            'recommendation': (
                f'Size mismatch detected. Use --auto-viewport to match '
                f'original dimensions ({img1.size[0]}x{img1.size[1]}).'
            )
        }

    diff = ImageChops.difference(img1, img2)
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
        non_zero = sum(histogram[1:])
        region_diffs[name] = round(non_zero / total * 100, 2) if total > 0 else 0

    return region_diffs


def suggest_font_sizes(img1, img2, num_bands=20, diff_threshold=15):
    """
    Suggest font size adjustments by analyzing horizontal bands of difference.

    Splits images into horizontal bands and identifies bands with high
    average difference, which typically indicate font size mismatches.

    Args:
        img1, img2: PIL Image objects (RGB)
        num_bands: Number of horizontal bands to analyze (default 20)
        diff_threshold: Mean difference threshold to flag a band (default 15)

    Returns:
        List of suggestion dicts with band position and estimated font size
    """
    if img1.size != img2.size:
        target_size = (
            max(img1.size[0], img2.size[0]),
            max(img1.size[1], img2.size[1])
        )
        img1 = img1.resize(target_size, Image.Resampling.LANCZOS)
        img2 = img2.resize(target_size, Image.Resampling.LANCZOS)

    diff = ImageChops.difference(img1, img2).convert('L')
    width, height = diff.size
    band_height = height // num_bands
    suggestions = []

    # Standard font sizes for suggestion
    std_sizes = [12, 14, 16, 18, 20, 24, 30, 36, 48]

    for i in range(num_bands):
        y_start = i * band_height
        y_end = y_start + band_height if i < num_bands - 1 else height
        band = diff.crop((0, y_start, width, y_end))

        pixels = list(band.getdata())
        if not pixels:
            continue

        mean_diff = sum(pixels) / len(pixels)

        if mean_diff > diff_threshold:
            # Estimate font size from band height context
            band_h = y_end - y_start
            # Assume the band roughly corresponds to a text line area
            estimated_size = max(10, round(band_h * 0.6))

            # Snap to nearest standard size
            closest = min(std_sizes, key=lambda s: abs(s - estimated_size))

            suggestions.append({
                'bandIndex': i,
                'yRange': [y_start, y_end],
                'meanDifference': round(mean_diff, 2),
                'suggestedFontSize': f'{closest}px',
                'confidence': 'high' if mean_diff > 30 else 'medium'
            })

    return suggestions


# =============================================================================
# P7: Region-level SSIM comparison
# =============================================================================

def calculate_region_ssim(img1, img2, regions):
    """
    Calculate per-region SSIM to identify which components differ most.

    Args:
        img1, img2: PIL Image objects (same size)
        regions: List of region dicts with 'name' and 'bounds' keys

    Returns:
        List of dicts with region name, SSIM score, and pass/fail
    """
    results = []
    for region in regions:
        b = region.get('bounds', {})
        x = b.get('x', 0)
        y = b.get('y', 0)
        w = b.get('w', 0)
        h = b.get('h', 0)

        # SSIM needs at least window_size (11) pixels in each dimension
        if w < 11 or h < 11:
            continue

        # Clamp to image bounds
        x2 = min(x + w, img1.size[0], img2.size[0])
        y2 = min(y + h, img1.size[1], img2.size[1])
        if x2 - x < 11 or y2 - y < 11:
            continue

        crop1 = img1.crop((x, y, x2, y2))
        crop2 = img2.crop((x, y, x2, y2))

        ssim = calculate_ssim(crop1, crop2)
        results.append({
            'name': region.get('name', ''),
            'ssim': ssim,
            'passed': ssim >= 90.0
        })

    results.sort(key=lambda r: r['ssim'])
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Compare original design image with current implementation'
    )
    parser.add_argument(
        '--original', required=True,
        help='Path to original design image (PNG/JPG)'
    )

    # Two modes for current implementation
    current_group = parser.add_mutually_exclusive_group(required=True)
    current_group.add_argument(
        '--current-url',
        help='URL to screenshot via Playwright (e.g., http://localhost:3001)'
    )
    current_group.add_argument(
        '--current-image',
        help='Path to existing screenshot of current implementation'
    )

    parser.add_argument(
        '--selector',
        help='CSS selector for specific element (used with --current-url)'
    )
    parser.add_argument(
        '--output-dir', default=DEFAULT_OUTPUT_DIR,
        help='Directory for output files'
    )
    parser.add_argument(
        '--threshold', type=float, default=DEFAULT_SIMILARITY_THRESHOLD,
        help=f'Similarity threshold for passing (default: {DEFAULT_SIMILARITY_THRESHOLD}%)'
    )
    parser.add_argument(
        '--wait', type=int, default=PAGE_LOAD_WAIT_MS,
        help='Page load wait time in ms (used with --current-url)'
    )
    parser.add_argument(
        '--metric', choices=['ssim', 'rms', 'both'], default='ssim',
        help='Similarity metric: ssim (default, structural), rms (legacy), both'
    )
    parser.add_argument(
        '--font-search', action='store_true',
        help='Analyze difference bands to suggest font size adjustments'
    )
    parser.add_argument(
        '--auto-viewport', action='store_true',
        help='Auto-match viewport to original image dimensions (--current-url only)'
    )
    parser.add_argument(
        '--regions',
        help='Region JSON file for per-region SSIM analysis'
    )

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    try:
        # Load original design image
        original_img = load_original_image(args.original)

        # Get current implementation image
        if args.current_url:
            # P6: Auto-match viewport to original image dimensions
            vp_width = VIEWPORT_WIDTH
            vp_height = VIEWPORT_HEIGHT
            if args.auto_viewport:
                vp_width = original_img.size[0]
                vp_height = original_img.size[1]

            current_img = capture_current_screenshot(
                args.current_url,
                selector=args.selector,
                wait_ms=args.wait,
                viewport_width=vp_width,
                viewport_height=vp_height
            )
        else:
            current_img = Image.open(args.current_image).convert('RGB')

        # Calculate similarity based on selected metric
        metrics = {}
        if args.metric in ('rms', 'both'):
            metrics['rms'] = calculate_similarity(original_img, current_img)
        if args.metric in ('ssim', 'both'):
            metrics['ssim'] = calculate_ssim(original_img, current_img)

        # Primary similarity score
        if args.metric == 'both':
            similarity = metrics['ssim']
        elif args.metric == 'ssim':
            similarity = metrics['ssim']
        else:
            similarity = metrics['rms']

        # Save images
        original_path = f'{args.output_dir}/original.png'
        current_path = f'{args.output_dir}/current.png'
        diff_path = f'{args.output_dir}/diff.png'

        original_img.save(original_path)
        current_img.save(current_path)
        create_diff_image(original_img, current_img, diff_path)

        # Analyze differences
        region_analysis = analyze_differences(original_img, current_img)
        passed = similarity >= args.threshold

        result = {
            'success': True,
            'similarity': similarity,
            'metric': args.metric,
            'metrics': metrics,
            'threshold': args.threshold,
            'passed': passed,
            'regionAnalysis': region_analysis,
            'images': {
                'original': original_path,
                'current': current_path,
                'diff': diff_path
            }
        }

        if not passed:
            result['recommendations'] = []

            if similarity < 80:
                result['recommendations'].append(
                    'Large difference detected. Check overall layout and structure.'
                )

            if isinstance(region_analysis, dict) and 'sizesDifferent' not in region_analysis:
                if region_analysis.get('top', 0) > 30:
                    result['recommendations'].append(
                        'Header/top area has significant differences.'
                    )
                if region_analysis.get('middle', 0) > 30:
                    result['recommendations'].append(
                        'Main content area has differences. Check colors and spacing.'
                    )
                if region_analysis.get('bottom', 0) > 30:
                    result['recommendations'].append(
                        'Footer/bottom area has differences.'
                    )

            result['recommendations'].extend([
                'Re-read original image and diff image to identify problem areas.',
                'Re-run extract_from_image.py with refined regions for problematic areas.',
                'Verify background colors match exactly.',
                'Check padding and margin values.',
            ])

        # Font size search analysis
        if args.font_search:
            font_suggestions = suggest_font_sizes(original_img, current_img)
            result['fontSearchSuggestions'] = font_suggestions

        # P7: Per-region SSIM analysis
        if args.regions:
            try:
                with open(args.regions, 'r', encoding='utf-8') as f:
                    region_list = json.load(f)
                region_ssim = calculate_region_ssim(
                    original_img, current_img, region_list
                )
                result['regionSSIM'] = region_ssim

                failed = [r for r in region_ssim if not r['passed']]
                if failed and 'recommendations' in result:
                    result['recommendations'].insert(0,
                        f'{len(failed)} region(s) below 90%: '
                        + ', '.join(
                            f"{r['name']}({r['ssim']}%)" for r in failed
                        )
                    )
            except (FileNotFoundError, json.JSONDecodeError) as e:
                result['regionSSIMError'] = str(e)

        print(json.dumps(result, indent=2))

    except FileNotFoundError as e:
        print(json.dumps({
            'success': False,
            'error': str(e)
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
