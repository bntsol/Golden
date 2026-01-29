#!/usr/bin/env python3
"""
Extracts UI styles from websites using Playwright.
Outputs structured JSON with computed styles for each element.
"""

import argparse
import json
import os
import sys
from datetime import datetime

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

# =============================================================================
# Configuration Constants
# =============================================================================

# Default viewport matches common desktop resolution
# Ensures consistent rendering across different machines
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080

# Wait time after page load for dynamic content to render
# Most SPAs complete initial render within 2 seconds
DEFAULT_WAIT_MS = 2000

# Default timeout for page navigation (ms)
# 60 seconds allows for slow connections while avoiding indefinite hangs
DEFAULT_TIMEOUT_MS = 60000

# Default wait_until strategy for page.goto()
# 'domcontentloaded' is faster and more reliable than 'networkidle' for most sites
# Options: 'domcontentloaded', 'load', 'networkidle', 'commit'
DEFAULT_WAIT_UNTIL = 'domcontentloaded'

# Maximum elements to capture hover states for
# Limits processing time while covering primary interactive elements
MAX_HOVER_ELEMENTS = 5

# Default selectors for auto-detection when no selector provided
DEFAULT_SELECTORS = 'button, input, [role="button"], .card, .chip, a.btn, [class*="button"], [class*="btn"]'


def extract_computed_styles(page, selector=None):
    """Extract computed styles from elements."""

    script = """
    (selector) => {
        const defaultSelector = 'button, input, [role="button"], .card, .chip, a.btn, [class*="button"], [class*="btn"]';
        const elements = document.querySelectorAll(selector || defaultSelector);

        function getUniqueSelector(el) {
            if (el.id) return '#' + el.id;
            if (el.className && typeof el.className === 'string') {
                const classes = el.className.split(' ').filter(c => c && !c.includes(':')).slice(0, 2).join('.');
                if (classes) return el.tagName.toLowerCase() + '.' + classes;
            }
            return el.tagName.toLowerCase();
        }

        return Array.from(elements).slice(0, 20).map(el => {
            const styles = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();

            // Skip hidden elements
            if (rect.width === 0 || rect.height === 0) return null;

            return {
                selector: getUniqueSelector(el),
                tag: el.tagName.toLowerCase(),
                role: el.getAttribute('role') || el.tagName.toLowerCase(),
                text: el.textContent?.trim().substring(0, 50) || '',
                boundingBox: {
                    x: Math.round(rect.x),
                    y: Math.round(rect.y),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height)
                },
                styles: {
                    // Background
                    backgroundColor: styles.backgroundColor,
                    backgroundImage: styles.backgroundImage,

                    // Text
                    color: styles.color,
                    fontSize: styles.fontSize,
                    fontWeight: styles.fontWeight,
                    fontFamily: styles.fontFamily,
                    lineHeight: styles.lineHeight,
                    textAlign: styles.textAlign,
                    letterSpacing: styles.letterSpacing,

                    // Spacing
                    padding: styles.padding,
                    paddingTop: styles.paddingTop,
                    paddingRight: styles.paddingRight,
                    paddingBottom: styles.paddingBottom,
                    paddingLeft: styles.paddingLeft,
                    margin: styles.margin,
                    marginTop: styles.marginTop,
                    marginRight: styles.marginRight,
                    marginBottom: styles.marginBottom,
                    marginLeft: styles.marginLeft,

                    // Border
                    border: styles.border,
                    borderColor: styles.borderColor,
                    borderWidth: styles.borderWidth,
                    borderStyle: styles.borderStyle,
                    borderRadius: styles.borderRadius,

                    // Layout
                    display: styles.display,
                    flexDirection: styles.flexDirection,
                    alignItems: styles.alignItems,
                    justifyContent: styles.justifyContent,
                    gap: styles.gap,

                    // Size
                    width: styles.width,
                    height: styles.height,
                    minWidth: styles.minWidth,
                    minHeight: styles.minHeight,
                    maxWidth: styles.maxWidth,
                    maxHeight: styles.maxHeight,

                    // Effects
                    boxShadow: styles.boxShadow,
                    opacity: styles.opacity,
                    transform: styles.transform,
                    transition: styles.transition,
                    cursor: styles.cursor
                }
            };
        }).filter(el => el !== null);
    }
    """

    return page.evaluate(script, selector)


def extract_hover_styles(page, elements):
    """Extract hover state styles for interactive elements."""

    hover_data = []

    for el_data in elements[:MAX_HOVER_ELEMENTS]:
        selector = el_data.get('selector')
        if not selector:
            continue

        try:
            element = page.query_selector(selector)
            if not element:
                continue

            # Hover over element
            element.hover()
            page.wait_for_timeout(150)

            # Extract hover styles
            hover_styles = page.evaluate("""
                (selector) => {
                    const el = document.querySelector(selector);
                    if (!el) return null;

                    const styles = window.getComputedStyle(el);
                    return {
                        backgroundColor: styles.backgroundColor,
                        color: styles.color,
                        borderColor: styles.borderColor,
                        transform: styles.transform,
                        boxShadow: styles.boxShadow,
                        opacity: styles.opacity
                    };
                }
            """, selector)

            if hover_styles:
                hover_data.append({
                    'selector': selector,
                    'hover': hover_styles
                })

            # Move mouse away
            page.mouse.move(0, 0)
            page.wait_for_timeout(50)

        except Exception:
            continue

    return hover_data


def merge_hover_states(elements, hover_data):
    """Merge hover state data into elements."""

    hover_map = {h['selector']: h['hover'] for h in hover_data}

    for el in elements:
        selector = el.get('selector')
        if selector in hover_map:
            el['states'] = {'hover': hover_map[selector]}

    return elements


def main():
    parser = argparse.ArgumentParser(description='Extract UI styles from websites')
    parser.add_argument('--url', required=True, help='Target URL')
    parser.add_argument('--selector', help='CSS selector (optional, auto-detects if omitted)')
    parser.add_argument('--output', default=f'{DEFAULT_OUTPUT_DIR}/styles.json', help='Output file path')
    parser.add_argument('--screenshot', help='Screenshot save path')
    parser.add_argument('--wait', type=int, default=DEFAULT_WAIT_MS, help='Additional wait after page load (ms)')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT_MS, help='Page navigation timeout (ms)')
    parser.add_argument('--wait-until', default=DEFAULT_WAIT_UNTIL,
                        choices=['domcontentloaded', 'load', 'networkidle', 'commit'],
                        help='Wait until strategy: domcontentloaded (fast), load, networkidle (slow), commit')
    parser.add_argument('--no-states', action='store_true', help='Skip hover/focus state capture')
    parser.add_argument('--headless', type=bool, default=True, help='Run in headless mode')

    args = parser.parse_args()

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        page = browser.new_page(viewport={'width': VIEWPORT_WIDTH, 'height': VIEWPORT_HEIGHT})

        try:
            # Navigate to page
            page.goto(args.url, wait_until=args.wait_until, timeout=args.timeout)
            page.wait_for_timeout(args.wait)

            # Take screenshot if requested
            if args.screenshot:
                page.screenshot(path=args.screenshot, full_page=False)

            # Extract styles
            elements = extract_computed_styles(page, args.selector)

            # Extract hover states
            if not args.no_states and elements:
                hover_data = extract_hover_styles(page, elements)
                elements = merge_hover_states(elements, hover_data)

            result = {
                'url': args.url,
                'timestamp': datetime.now().isoformat(),
                'viewport': {'width': VIEWPORT_WIDTH, 'height': VIEWPORT_HEIGHT},
                'selector': args.selector or 'auto-detected',
                'elementsCount': len(elements),
                'elements': elements
            }

            # Write output
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            # Print summary
            print(json.dumps({
                'success': True,
                'elementsCount': len(elements),
                'output': args.output,
                'screenshot': args.screenshot
            }, indent=2))

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
