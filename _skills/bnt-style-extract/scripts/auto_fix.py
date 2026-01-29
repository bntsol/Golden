#!/usr/bin/env python3
"""
Automated difference analysis and iterative correction script.
Analyzes style differences and suggests/applies fixes until similarity threshold is met.
"""

import argparse
import json
import os
import re
import sys
import subprocess
import time
from pathlib import Path

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

# Target similarity threshold (percentage)
# 95% allows for minor rendering differences while ensuring visual match
DEFAULT_SIMILARITY_THRESHOLD = 95.0

# Maximum correction iterations before giving up
# 3 iterations typically resolve most fixable differences
MAX_ITERATIONS = 3

# Wait time between iterations for server rebuild (seconds)
# Next.js/Vite hot reload typically completes within 3 seconds
SERVER_REBUILD_WAIT = 3

# Maximum style properties to fix per iteration
# Fixing too many at once can cause cascading issues
MAX_FIXES_PER_ITERATION = 3

# Priority order for fixing style differences
# Lower number = higher priority (colors most visible, then spacing, then borders)
FIX_PRIORITY = {
    'backgroundColor': 1,
    'color': 1,
    'paddingTop': 2,
    'paddingRight': 2,
    'paddingBottom': 2,
    'paddingLeft': 2,
    'borderRadius': 3,
    'fontSize': 4,
    'fontWeight': 4,
    'borderColor': 5,
    'boxShadow': 6,
}

# Viewport for consistent comparison
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080


def get_script_dir():
    """Get the directory containing this script."""
    return Path(__file__).parent


def run_compare(target_url, current_url, selector, output_dir):
    """Run compare.py and return results."""
    script_path = get_script_dir() / 'compare.py'

    cmd = [
        'python', str(script_path),
        '--target', target_url,
        '--current', current_url,
        '--output-dir', output_dir
    ]

    if selector:
        cmd.extend(['--selector', selector])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return None
    except Exception as e:
        print(f"Compare error: {e}", file=sys.stderr)
        return None


def extract_element_styles(url, selector):
    """Extract specific element's computed styles from URL."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': VIEWPORT_WIDTH, 'height': VIEWPORT_HEIGHT})

        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(2000)

            styles = page.evaluate("""
                (selector) => {
                    const el = document.querySelector(selector);
                    if (!el) return null;

                    const computed = window.getComputedStyle(el);
                    return {
                        backgroundColor: computed.backgroundColor,
                        color: computed.color,
                        padding: computed.padding,
                        paddingTop: computed.paddingTop,
                        paddingRight: computed.paddingRight,
                        paddingBottom: computed.paddingBottom,
                        paddingLeft: computed.paddingLeft,
                        borderRadius: computed.borderRadius,
                        fontSize: computed.fontSize,
                        fontWeight: computed.fontWeight,
                        border: computed.border,
                        borderColor: computed.borderColor,
                        borderWidth: computed.borderWidth,
                        boxShadow: computed.boxShadow,
                        fontFamily: computed.fontFamily,
                        lineHeight: computed.lineHeight
                    };
                }
            """, selector)

            return styles

        finally:
            browser.close()


def analyze_differences(target_styles, current_styles):
    """Analyze and prioritize differences between styles."""
    if not target_styles or not current_styles:
        return []

    differences = []

    for prop, priority in sorted(FIX_PRIORITY.items(), key=lambda x: x[1]):
        target_val = target_styles.get(prop)
        current_val = current_styles.get(prop)

        if target_val and current_val and target_val != current_val:
            # Skip transparent/none values
            if 'rgba(0, 0, 0, 0)' in str(target_val) or 'none' in str(target_val).lower():
                continue

            differences.append({
                'property': prop,
                'priority': priority,
                'target': target_val,
                'current': current_val
            })

    return differences


def rgb_to_hex(rgb):
    """Convert RGB string to hex."""
    if not rgb:
        return None
    match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgb)
    if match:
        r, g, b = map(int, match.groups())
        return f'#{r:02x}{g:02x}{b:02x}'
    return rgb if rgb.startswith('#') else None


def generate_tailwind_fix(difference):
    """Generate Tailwind class replacement for a difference."""
    prop = difference['property']
    target_value = difference['target']

    if prop == 'backgroundColor':
        hex_color = rgb_to_hex(target_value)
        if hex_color:
            return {
                'type': 'tailwind_class',
                'search_pattern': r'bg-\[#[a-fA-F0-9]+\]',
                'replacement': f'bg-[{hex_color}]',
                'description': f'Change background color to {hex_color}'
            }

    elif prop == 'color':
        hex_color = rgb_to_hex(target_value)
        if hex_color:
            return {
                'type': 'tailwind_class',
                'search_pattern': r'text-\[#[a-fA-F0-9]+\]',
                'replacement': f'text-[{hex_color}]',
                'description': f'Change text color to {hex_color}'
            }

    elif prop == 'borderRadius':
        px_match = re.search(r'([\d.]+)px', target_value)
        if px_match:
            px = int(float(px_match.group(1)))
            radius_map = {
                0: 'rounded-none', 4: 'rounded', 6: 'rounded-md',
                8: 'rounded-lg', 12: 'rounded-xl', 16: 'rounded-2xl',
                24: 'rounded-3xl'
            }
            tw_class = radius_map.get(px, f'rounded-[{px}px]')
            return {
                'type': 'tailwind_class',
                'search_pattern': r'rounded-\[[\d]+px\]|rounded-(?:none|sm|md|lg|xl|2xl|3xl|full)',
                'replacement': tw_class,
                'description': f'Change border-radius to {px}px ({tw_class})'
            }

    elif prop.startswith('padding'):
        px_match = re.search(r'([\d.]+)px', target_value)
        if px_match:
            px = int(float(px_match.group(1)))
            spacing_map = {
                0: '0', 4: '1', 8: '2', 12: '3', 16: '4',
                20: '5', 24: '6', 32: '8', 40: '10', 48: '12'
            }

            if prop in ['paddingTop', 'paddingBottom']:
                prefix = 'py'
            else:
                prefix = 'px'

            tw_value = spacing_map.get(px, f'[{px}px]')
            return {
                'type': 'tailwind_class',
                'search_pattern': rf'{prefix}-\[[\d]+px\]|{prefix}-[\d]+',
                'replacement': f'{prefix}-{tw_value}',
                'description': f'Change {prefix} padding to {px}px'
            }

    elif prop == 'fontSize':
        px_match = re.search(r'([\d.]+)px', target_value)
        if px_match:
            px = int(float(px_match.group(1)))
            size_map = {
                12: 'text-xs', 14: 'text-sm', 16: 'text-base',
                18: 'text-lg', 20: 'text-xl', 24: 'text-2xl'
            }
            tw_class = size_map.get(px, f'text-[{px}px]')
            return {
                'type': 'tailwind_class',
                'search_pattern': r'text-\[[\d]+px\]|text-(?:xs|sm|base|lg|xl|2xl|3xl)',
                'replacement': tw_class,
                'description': f'Change font size to {px}px ({tw_class})'
            }

    return None


def apply_fix_to_file(file_path, fix):
    """Apply a fix to a component file. Returns True if successful."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = fix['search_pattern']
        replacement = fix['replacement']

        # Find matches
        matches = re.findall(pattern, content)
        if not matches:
            return False, 'Pattern not found in file'

        # Apply replacement
        new_content = re.sub(pattern, replacement, content, count=1)

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, f'Replaced "{matches[0]}" with "{replacement}"'

        return False, 'No changes made'

    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description='Automated iterative style correction')
    parser.add_argument('--target-url', required=True, help='Target URL (original design)')
    parser.add_argument('--current-url', required=True, help='Current implementation URL')
    parser.add_argument('--selector', required=True, help='CSS selector for element to compare')
    parser.add_argument('--component-file', required=True, help='Path to component file to fix')
    parser.add_argument('--max-iterations', type=int, default=MAX_ITERATIONS, help='Maximum fix iterations')
    parser.add_argument('--threshold', type=float, default=DEFAULT_SIMILARITY_THRESHOLD, help='Target similarity %')
    parser.add_argument('--output-dir', default=DEFAULT_OUTPUT_DIR, help='Output directory for screenshots')
    parser.add_argument('--dry-run', action='store_true', help='Show fixes without applying')

    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Validate component file exists
    if not Path(args.component_file).exists():
        print(json.dumps({
            'success': False,
            'error': f'Component file not found: {args.component_file}'
        }, indent=2), file=sys.stderr)
        sys.exit(1)

    all_fixes = []
    initial_similarity = None

    print(f"\n{'='*60}")
    print("BNT Style Auto-Fix")
    print(f"{'='*60}")
    print(f"Target: {args.target_url}")
    print(f"Current: {args.current_url}")
    print(f"Selector: {args.selector}")
    print(f"Component: {args.component_file}")
    print(f"Threshold: {args.threshold}%")
    print(f"{'='*60}\n")

    for iteration in range(1, args.max_iterations + 1):
        print(f"\n--- Iteration {iteration}/{args.max_iterations} ---\n")

        # Step 1: Run comparison
        print("Running visual comparison...")
        compare_result = run_compare(
            args.target_url, args.current_url,
            args.selector, args.output_dir
        )

        if not compare_result or not compare_result.get('success'):
            print("Comparison failed", file=sys.stderr)
            continue

        similarity = compare_result.get('similarity', 0)
        print(f"Current similarity: {similarity}%")

        if initial_similarity is None:
            initial_similarity = similarity

        # Step 2: Check if threshold met
        if similarity >= args.threshold:
            result = {
                'success': True,
                'status': 'PASSED',
                'iterations': iteration,
                'initialSimilarity': initial_similarity,
                'finalSimilarity': similarity,
                'fixes': all_fixes,
                'message': f'Achieved {similarity}% similarity (>= {args.threshold}%) after {iteration} iteration(s).'
            }
            print(f"\n{'='*60}")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return

        # Step 3: Extract and compare styles
        print("Extracting target styles...")
        target_styles = extract_element_styles(args.target_url, args.selector)

        if not target_styles:
            print(f"Could not extract styles from target with selector: {args.selector}")
            continue

        print("Extracting current styles...")
        current_styles = extract_element_styles(args.current_url, args.selector)

        if not current_styles:
            print(f"Could not extract styles from current with selector: {args.selector}")
            continue

        # Step 4: Analyze differences
        differences = analyze_differences(target_styles, current_styles)
        print(f"Found {len(differences)} style difference(s)")

        if not differences:
            print("No fixable differences found. Manual review may be needed.")
            break

        # Step 5: Generate and apply fixes
        fixes_applied = 0

        for diff in differences[:MAX_FIXES_PER_ITERATION]:
            fix = generate_tailwind_fix(diff)

            if not fix:
                continue

            print(f"\nDifference: {diff['property']}")
            print(f"  Current: {diff['current']}")
            print(f"  Target:  {diff['target']}")
            print(f"  Fix: {fix['description']}")

            if args.dry_run:
                print("  [DRY RUN] Would apply fix")
                all_fixes.append({
                    'iteration': iteration,
                    'property': diff['property'],
                    'before': diff['current'],
                    'after': diff['target'],
                    'dryRun': True
                })
            else:
                success, message = apply_fix_to_file(args.component_file, fix)

                if success:
                    print(f"  Applied: {message}")
                    fixes_applied += 1
                    all_fixes.append({
                        'iteration': iteration,
                        'property': diff['property'],
                        'before': diff['current'],
                        'after': diff['target'],
                        'file': args.component_file
                    })
                else:
                    print(f"  Failed: {message}")

        if fixes_applied == 0 and not args.dry_run:
            print("\nNo fixes could be applied. Manual intervention needed.")
            break

        # Wait for server rebuild
        if not args.dry_run and fixes_applied > 0:
            print(f"\nWaiting {SERVER_REBUILD_WAIT}s for server rebuild...")
            time.sleep(SERVER_REBUILD_WAIT)

    # Final comparison
    print("\n--- Final Check ---\n")
    final_compare = run_compare(
        args.target_url, args.current_url,
        args.selector, args.output_dir
    )

    final_similarity = final_compare.get('similarity', 0) if final_compare else 0

    if final_similarity >= args.threshold:
        status = 'PASSED'
        success = True
    else:
        status = 'MAX_ITERATIONS_REACHED'
        success = False

    result = {
        'success': success,
        'status': status,
        'iterations': args.max_iterations,
        'initialSimilarity': initial_similarity,
        'finalSimilarity': final_similarity,
        'threshold': args.threshold,
        'fixes': all_fixes,
        'message': f'Final similarity: {final_similarity}%'
    }

    if not success:
        result['recommendations'] = [
            'Complex gradients or shadows may need manual adjustment.',
            'Check for layout structure differences.',
            'Font rendering may vary between environments.',
            'Consider comparing individual style properties manually.'
        ]

    print(f"\n{'='*60}")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
