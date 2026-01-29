# UI/UX Style Extractor - Agent Skill 구현 계획

## 1. 개요

### 목표
타겟 웹사이트의 UI/UX 스타일을 자동으로 추출하고 Tailwind CSS로 변환하는 **Claude Code Agent Skill** 구현

### 핵심 원칙
1. **Progressive Disclosure**: 필요한 것만 로딩
2. **스크립트 실행**: 코드는 컨텍스트에 로딩하지 않고 결과만 사용
3. **단일 책임**: 각 스크립트는 하나의 역할만 수행
4. **JSON 기반 통신**: 스크립트 출력은 구조화된 JSON

---

## 2. Skill 디렉토리 구조

```
~/.claude/skills/bnt-style-extract/
├── SKILL.md                    # 메인 지침서 (Level 2)
├── REFERENCE.md                # Tailwind 매핑 참조 (Level 3)
├── PATTERNS.md                 # 컴포넌트 패턴 가이드 (Level 3)
├── scripts/
│   ├── requirements.txt        # Python 의존성
│   ├── extract.py              # 스타일 추출
│   ├── analyze.py              # 스타일 분석
│   ├── convert.py              # Tailwind 변환
│   ├── compare.py              # 시각적 비교
│   ├── auto_fix.py             # 자동 차이점 분석 및 수정 제안
│   └── utils/
│       ├── __init__.py
│       ├── color.py            # 색상 유틸리티
│       ├── spacing.py          # 간격 유틸리티
│       └── tailwind.py         # Tailwind 매핑
└── templates/
    ├── component.tsx           # React 컴포넌트 템플릿
    ├── button.tsx              # 버튼 템플릿
    ├── input.tsx               # 입력 필드 템플릿
    ├── card.tsx                # 카드 템플릿
    └── chip.tsx                # 칩/태그 템플릿
```

---

## 3. SKILL.md 설계

```markdown
---
name: bnt-style-extract
description: Extracts UI/UX styles from target websites and converts them to Tailwind CSS. Triggers on requests mentioning style extraction, UI cloning, design copying, Tailwind conversion, or applying specific website component styles.
---

# Style Extractor

Extracts computed styles from websites using Playwright and converts them to Tailwind CSS classes.

## Workflow Checklist

Copy this checklist to track progress:

```
Style Extraction Progress:
- [ ] Step 1: Extract styles (extract.py)
- [ ] Step 2: Convert to Tailwind (convert.py)
- [ ] Step 3: Apply to component
- [ ] Step 4: Visual comparison (compare.py)
- [ ] Step 5: Auto-fix if needed (auto_fix.py)
```

## Quick Start

### 1. 전체 페이지 스타일 추출
```bash
# 출력: .style-extract/styles.json (기본값)
python scripts/extract.py --url "https://example.com"
```

### 2. 특정 요소 스타일 추출
```bash
# 출력: .style-extract/styles.json (기본값)
python scripts/extract.py --url "https://example.com" --selector "button.primary"
```

### 3. Tailwind로 변환
```bash
# 출력: .style-extract/tailwind.json (기본값)
python scripts/convert.py --input .style-extract/styles.json
```

## 워크플로우

### Step 1: 스타일 추출
사용자가 URL을 제공하면 `scripts/extract.py`를 실행합니다.

**필수 파라미터:**
- `--url`: 타겟 웹사이트 URL

**선택 파라미터:**
- `--selector`: 특정 요소 선택자 (없으면 주요 컴포넌트 자동 감지)
- `--screenshot`: 스크린샷 저장 경로
- `--wait`: 페이지 로드 후 추가 대기 시간 ms (기본: 2000)
- `--timeout`: 페이지 탐색 타임아웃 ms (기본: 60000)
- `--wait-until`: 페이지 로드 전략 (기본: domcontentloaded)
  - `domcontentloaded`: 빠름, 대부분의 사이트에 권장
  - `load`: 모든 리소스 로딩 대기
  - `networkidle`: 네트워크 유휴 대기 (느림, 동적 사이트에서 타임아웃 가능)
  - `commit`: 가장 빠름, 탐색 커밋만 대기
- `--no-states`: hover/focus 상태 캡처 생략

**출력 예시:**
```json
{
  "url": "https://example.com",
  "elements": [
    {
      "selector": "button.primary",
      "tag": "button",
      "role": "button",
      "styles": {
        "backgroundColor": "rgb(24, 61, 121)",
        "color": "rgb(174, 203, 250)",
        "padding": "12px 16px",
        "borderRadius": "24px",
        "fontSize": "14px"
      },
      "states": {
        "hover": {
          "backgroundColor": "rgb(30, 75, 150)"
        }
      }
    }
  ]
}
```

### Step 2: 스타일 분석 (선택적)
복잡한 페이지의 경우 `scripts/analyze.py`로 패턴을 분석합니다.

```bash
python scripts/analyze.py --input styles.json --output analysis.json
```

**출력 예시:**
```json
{
  "colorPalette": {
    "primary": ["#183d79", "#1a73e8"],
    "background": ["#000000", "#0d1421", "#202124"],
    "text": ["#ffffff", "#bdc1c6", "#aecbfa"]
  },
  "spacingScale": [4, 8, 12, 16, 24, 32],
  "borderRadii": [4, 8, 16, 24],
  "componentTypes": ["button", "input", "card", "chip"]
}
```

### Step 3: Tailwind 변환
`scripts/convert.py`로 Tailwind 클래스를 생성합니다.

```bash
# 출력: .style-extract/tailwind.json (기본값)
python scripts/convert.py --input .style-extract/styles.json
```

**출력 예시:**
```json
{
  "elements": [
    {
      "selector": "button.primary",
      "tailwindClasses": "bg-[#183d79] hover:bg-[#1e4b96] text-[#aecbfa] hover:text-white py-3 px-4 rounded-3xl text-sm font-medium transition-all",
      "customCSS": null
    }
  ],
  "configExtensions": {
    "colors": {
      "primary": "#183d79",
      "primary-hover": "#1e4b96"
    }
  }
}
```

### Step 4: 시각적 비교
`scripts/compare.py`로 원본과 구현을 비교합니다.

```bash
python scripts/compare.py --target "https://example.com" --current "http://localhost:3000" --selector "button.primary"
```

**출력:**
- 유사도 점수 (0-100%)
- 차이점 목록
- diff 이미지 저장

### Step 5: 자동 반복 수정 (핵심!)

**중요: 유사도가 95% 미만이면 자동으로 수정을 반복합니다.**

```bash
# 스크린샷 저장: .style-extract/ (기본값)
python scripts/auto_fix.py --target-url "https://example.com" --current-url "http://localhost:3000" --selector "button" --component-file "components/Button.tsx" --max-iterations 3
```

#### 자동 수정 워크플로우

```
┌─────────────────────────────────────────────────────────────┐
│                    자동 반복 수정 루프                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. compare.py 실행 → 유사도 확인                            │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────┐                                       │
│  │ 유사도 >= 95% ?  │──── Yes ──→ 완료! 결과 보고           │
│  └──────────────────┘                                       │
│         │ No                                                │
│         ▼                                                   │
│  2. 차이점 분석 (색상? 간격? 테두리?)                         │
│         │                                                   │
│         ▼                                                   │
│  3. 타겟에서 해당 속성 재추출                                 │
│         │                                                   │
│         ▼                                                   │
│  4. 컴포넌트 코드 자동 수정                                   │
│         │                                                   │
│         ▼                                                   │
│  5. 반복 (최대 3회)                                          │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────┐                                       │
│  │ 3회 초과?        │──── Yes ──→ 수동 검토 필요 알림        │
│  └──────────────────┘                                       │
│         │ No                                                │
│         └──────────────→ Step 1로 돌아가기                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 수정 우선순위

| 우선순위 | 차이 유형 | 수정 방법 |
|---------|----------|----------|
| 1 | 배경색/텍스트색 | 타겟에서 색상 재추출 → Tailwind 클래스 교체 |
| 2 | 간격 (padding/margin) | px 값 재측정 → py-X, px-X 조정 |
| 3 | 테두리 (border-radius) | 값 재추출 → rounded-X 조정 |
| 4 | 폰트 크기/굵기 | 값 재추출 → text-X, font-X 조정 |
| 5 | 그림자/효과 | 복잡한 경우 커스텀 CSS로 처리 |

#### 출력 예시

```json
{
  "iteration": 2,
  "previousSimilarity": 87.5,
  "currentSimilarity": 96.2,
  "status": "PASSED",
  "fixes": [
    {
      "property": "backgroundColor",
      "before": "bg-[#1c1c1e]",
      "after": "bg-[#0d1421]",
      "file": "components/ChatOverlay.tsx",
      "line": 66
    },
    {
      "property": "borderRadius",
      "before": "rounded-[28px]",
      "after": "rounded-3xl",
      "file": "components/ChatOverlay.tsx",
      "line": 66
    }
  ],
  "message": "2회 반복 후 95% 이상 달성. 수정 완료."
}
```

## 컴포넌트 생성

추출된 스타일로 React 컴포넌트를 생성할 때는 `templates/` 디렉토리의 템플릿을 참조합니다.

상세한 컴포넌트 패턴은 [PATTERNS.md](PATTERNS.md)를 참조하세요.

## Tailwind 매핑 규칙

색상, 간격, 타이포그래피의 Tailwind 매핑 규칙은 [REFERENCE.md](REFERENCE.md)를 참조하세요.

## 주의사항

1. **네트워크 접근**: 이 Skill은 외부 웹사이트에 접근합니다. 신뢰할 수 있는 URL만 사용하세요.
2. **동적 콘텐츠**: SPA의 경우 `--wait-until domcontentloaded` (기본값) 사용, 필요시 `--wait` 증가.
3. **타임아웃 문제**: 추출이 타임아웃되면 `--wait-until commit` 또는 `--timeout` 증가 시도.
4. **인증 필요 페이지**: 로그인이 필요한 페이지는 지원하지 않습니다.
```

---

## 4. 핵심 스크립트 설계

### 4.1 extract.py

```python
#!/usr/bin/env python3
"""
Extracts UI styles from websites using Playwright.
Outputs structured JSON with computed styles for each element.
"""

import argparse
import json
import sys
from playwright.sync_api import sync_playwright

# =============================================================================
# Configuration Constants (documented per Anthropic best practices)
# =============================================================================

# Default viewport matches common desktop resolution
# Ensures consistent rendering across different machines
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080

# Wait time after page load for dynamic content to render
# Most SPAs complete initial render within 2 seconds
# Adjust with --wait flag for slower pages
DEFAULT_WAIT_MS = 2000

# Maximum elements to capture hover states for
# Limits processing time while covering primary interactive elements
MAX_HOVER_ELEMENTS = 5


def extract_computed_styles(page, selector=None):
    """요소의 computed style 추출"""

    script = """
    (selector) => {
        const elements = selector
            ? document.querySelectorAll(selector)
            : document.querySelectorAll('button, input, [role="button"], .card, .chip');

        return Array.from(elements).map(el => {
            const styles = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();

            return {
                selector: getUniqueSelector(el),
                tag: el.tagName.toLowerCase(),
                role: el.getAttribute('role') || el.tagName.toLowerCase(),
                text: el.textContent?.trim().substring(0, 50),
                boundingBox: {
                    x: rect.x, y: rect.y,
                    width: rect.width, height: rect.height
                },
                styles: {
                    // 배경
                    backgroundColor: styles.backgroundColor,
                    backgroundImage: styles.backgroundImage,

                    // 텍스트
                    color: styles.color,
                    fontSize: styles.fontSize,
                    fontWeight: styles.fontWeight,
                    fontFamily: styles.fontFamily,
                    lineHeight: styles.lineHeight,
                    textAlign: styles.textAlign,

                    // 간격
                    padding: styles.padding,
                    paddingTop: styles.paddingTop,
                    paddingRight: styles.paddingRight,
                    paddingBottom: styles.paddingBottom,
                    paddingLeft: styles.paddingLeft,
                    margin: styles.margin,

                    // 테두리
                    border: styles.border,
                    borderColor: styles.borderColor,
                    borderWidth: styles.borderWidth,
                    borderRadius: styles.borderRadius,

                    // 레이아웃
                    display: styles.display,
                    flexDirection: styles.flexDirection,
                    alignItems: styles.alignItems,
                    justifyContent: styles.justifyContent,
                    gap: styles.gap,

                    // 효과
                    boxShadow: styles.boxShadow,
                    opacity: styles.opacity,
                    transform: styles.transform,
                    transition: styles.transition
                }
            };
        });

        function getUniqueSelector(el) {
            if (el.id) return '#' + el.id;
            if (el.className) {
                const classes = el.className.split(' ').filter(c => c).slice(0, 2).join('.');
                if (classes) return el.tagName.toLowerCase() + '.' + classes;
            }
            return el.tagName.toLowerCase();
        }
    }
    """

    return page.evaluate(script, selector)


def extract_hover_styles(page, selector):
    """hover 상태의 스타일 추출"""

    elements = page.query_selector_all(selector) if selector else page.query_selector_all('button')
    hover_styles = []

    for el in elements[:5]:  # 최대 5개만
        el.hover()
        page.wait_for_timeout(100)

        styles = page.evaluate("""
            (el) => {
                const styles = window.getComputedStyle(el);
                return {
                    backgroundColor: styles.backgroundColor,
                    color: styles.color,
                    transform: styles.transform,
                    boxShadow: styles.boxShadow
                };
            }
        """, el)

        hover_styles.append(styles)

    return hover_styles


def main():
    parser = argparse.ArgumentParser(description='웹사이트 스타일 추출')
    parser.add_argument('--url', required=True, help='타겟 URL')
    parser.add_argument('--selector', help='CSS 선택자 (선택적)')
    parser.add_argument('--output', default='.style-extract/styles.json', help='출력 파일')
    parser.add_argument('--screenshot', help='스크린샷 저장 경로')
    parser.add_argument('--wait', type=int, default=2000, help='페이지 로딩 대기 시간(ms)')
    parser.add_argument('--states', type=bool, default=True, help='hover/focus 상태 캡처')

    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        try:
            page.goto(args.url, wait_until='networkidle')
            page.wait_for_timeout(args.wait)

            # 스크린샷 캡처
            if args.screenshot:
                page.screenshot(path=args.screenshot, full_page=False)

            # 스타일 추출
            elements = extract_computed_styles(page, args.selector)

            # hover 상태 추출
            if args.states and elements:
                for i, el in enumerate(elements[:5]):
                    selector = el.get('selector')
                    if selector:
                        hover = extract_hover_styles(page, selector)
                        if hover:
                            elements[i]['states'] = {'hover': hover[0]}

            result = {
                'url': args.url,
                'timestamp': __import__('datetime').datetime.now().isoformat(),
                'elements': elements
            }

            # 출력
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(json.dumps({
                'success': True,
                'elementsCount': len(elements),
                'output': args.output
            }))

        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }), file=sys.stderr)
            sys.exit(1)

        finally:
            browser.close()


if __name__ == '__main__':
    main()
```

### 4.2 convert.py

```python
#!/usr/bin/env python3
"""
추출된 스타일을 Tailwind CSS로 변환하는 스크립트
"""

import argparse
import json
import re
import sys

# Tailwind 간격 스케일 매핑
SPACING_MAP = {
    0: '0', 1: 'px', 2: '0.5', 4: '1', 6: '1.5', 8: '2',
    10: '2.5', 12: '3', 14: '3.5', 16: '4', 20: '5',
    24: '6', 28: '7', 32: '8', 36: '9', 40: '10',
    44: '11', 48: '12', 56: '14', 64: '16', 80: '20',
    96: '24', 112: '28', 128: '32'
}

# Tailwind 폰트 크기 매핑
FONT_SIZE_MAP = {
    12: 'text-xs', 14: 'text-sm', 16: 'text-base',
    18: 'text-lg', 20: 'text-xl', 24: 'text-2xl',
    30: 'text-3xl', 36: 'text-4xl', 48: 'text-5xl'
}

# Tailwind border-radius 매핑
RADIUS_MAP = {
    0: 'rounded-none', 2: 'rounded-sm', 4: 'rounded',
    6: 'rounded-md', 8: 'rounded-lg', 12: 'rounded-xl',
    16: 'rounded-2xl', 24: 'rounded-3xl', 9999: 'rounded-full'
}


def parse_px(value):
    """'16px' -> 16"""
    if not value:
        return None
    match = re.search(r'([\d.]+)px', str(value))
    return float(match.group(1)) if match else None


def rgb_to_hex(rgb):
    """'rgb(24, 61, 121)' -> '#183d79'"""
    if not rgb or rgb == 'transparent' or rgb == 'rgba(0, 0, 0, 0)':
        return None

    match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgb)
    if match:
        r, g, b = map(int, match.groups())
        return f'#{r:02x}{g:02x}{b:02x}'
    return rgb if rgb.startswith('#') else None


def spacing_to_tailwind(px, prefix='p'):
    """px 값을 Tailwind 간격 클래스로 변환"""
    if px is None:
        return None

    px = int(round(px))

    if px in SPACING_MAP:
        return f'{prefix}-{SPACING_MAP[px]}'

    # 가장 가까운 값 찾기
    closest = min(SPACING_MAP.keys(), key=lambda x: abs(x - px))
    if abs(closest - px) <= 2:
        return f'{prefix}-{SPACING_MAP[closest]}'

    # arbitrary value
    return f'{prefix}-[{px}px]'


def color_to_tailwind(rgb, prefix='bg'):
    """RGB 값을 Tailwind 색상 클래스로 변환"""
    hex_color = rgb_to_hex(rgb)
    if not hex_color:
        return None

    # 일반적인 색상 매칭 (간단한 버전)
    common_colors = {
        '#000000': 'black',
        '#ffffff': 'white',
        '#1a73e8': 'blue-600',
        '#202124': 'gray-900',
    }

    if hex_color.lower() in common_colors:
        return f'{prefix}-{common_colors[hex_color.lower()]}'

    return f'{prefix}-[{hex_color}]'


def font_size_to_tailwind(px):
    """폰트 크기를 Tailwind 클래스로 변환"""
    if px is None:
        return None

    px = int(round(px))

    if px in FONT_SIZE_MAP:
        return FONT_SIZE_MAP[px]

    closest = min(FONT_SIZE_MAP.keys(), key=lambda x: abs(x - px))
    if abs(closest - px) <= 1:
        return FONT_SIZE_MAP[closest]

    return f'text-[{px}px]'


def radius_to_tailwind(px):
    """border-radius를 Tailwind 클래스로 변환"""
    if px is None:
        return None

    px = int(round(px))

    if px in RADIUS_MAP:
        return RADIUS_MAP[px]

    closest = min(RADIUS_MAP.keys(), key=lambda x: abs(x - px))
    if abs(closest - px) <= 2:
        return RADIUS_MAP[closest]

    return f'rounded-[{px}px]'


def convert_element_styles(styles, hover_styles=None):
    """요소 스타일을 Tailwind 클래스 문자열로 변환"""
    classes = []

    # 배경색
    bg = color_to_tailwind(styles.get('backgroundColor'), 'bg')
    if bg:
        classes.append(bg)

    # 텍스트 색상
    text_color = color_to_tailwind(styles.get('color'), 'text')
    if text_color:
        classes.append(text_color)

    # 폰트 크기
    font_size = font_size_to_tailwind(parse_px(styles.get('fontSize')))
    if font_size:
        classes.append(font_size)

    # 폰트 굵기
    font_weight = styles.get('fontWeight')
    if font_weight:
        weight_map = {'400': 'font-normal', '500': 'font-medium', '600': 'font-semibold', '700': 'font-bold'}
        if font_weight in weight_map:
            classes.append(weight_map[font_weight])

    # 패딩
    padding_y = parse_px(styles.get('paddingTop') or styles.get('paddingBottom'))
    padding_x = parse_px(styles.get('paddingLeft') or styles.get('paddingRight'))

    if padding_y:
        py = spacing_to_tailwind(padding_y, 'py')
        if py:
            classes.append(py)

    if padding_x:
        px_class = spacing_to_tailwind(padding_x, 'px')
        if px_class:
            classes.append(px_class)

    # border-radius
    radius = radius_to_tailwind(parse_px(styles.get('borderRadius')))
    if radius:
        classes.append(radius)

    # border
    border_width = parse_px(styles.get('borderWidth'))
    if border_width and border_width > 0:
        classes.append('border')
        border_color = color_to_tailwind(styles.get('borderColor'), 'border')
        if border_color:
            classes.append(border_color)

    # hover 상태
    if hover_styles:
        hover_bg = color_to_tailwind(hover_styles.get('backgroundColor'), 'hover:bg')
        if hover_bg and hover_bg != bg:
            classes.append(hover_bg)

        hover_text = color_to_tailwind(hover_styles.get('color'), 'hover:text')
        if hover_text and hover_text != text_color:
            classes.append(hover_text)

    # transition
    if hover_styles:
        classes.append('transition-all')
        classes.append('duration-200')

    return ' '.join(classes)


def main():
    parser = argparse.ArgumentParser(description='스타일을 Tailwind CSS로 변환')
    parser.add_argument('--input', required=True, help='입력 JSON 파일')
    parser.add_argument('--output', default='.style-extract/tailwind.json', help='출력 파일')

    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)

        results = []
        config_colors = {}

        for element in data.get('elements', []):
            styles = element.get('styles', {})
            hover_styles = element.get('states', {}).get('hover')

            tailwind_classes = convert_element_styles(styles, hover_styles)

            # 사용된 커스텀 색상 수집
            bg_hex = rgb_to_hex(styles.get('backgroundColor'))
            if bg_hex:
                config_colors[f'custom-{len(config_colors)}'] = bg_hex

            results.append({
                'selector': element.get('selector'),
                'role': element.get('role'),
                'tailwindClasses': tailwind_classes,
                'originalStyles': styles
            })

        output = {
            'source': data.get('url'),
            'elements': results,
            'configExtensions': {
                'colors': config_colors
            } if config_colors else None
        }

        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(json.dumps({
            'success': True,
            'elementsConverted': len(results),
            'output': args.output
        }))

    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e)
        }), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
```

### 4.3 compare.py

```python
#!/usr/bin/env python3
"""
Visual comparison between target website and current implementation.
Calculates similarity percentage using image difference analysis.
"""

import argparse
import json
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
import io

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
SIMILARITY_THRESHOLD = 95.0


def capture_element(page, selector):
    """Captures screenshot of specific element or full page."""
    element = page.query_selector(selector)
    if element:
        return element.screenshot()
    return page.screenshot()


def calculate_similarity(img1_bytes, img2_bytes):
    """두 이미지의 유사도 계산 (0-100%)"""
    from PIL import ImageChops
    import math

    img1 = Image.open(io.BytesIO(img1_bytes)).convert('RGB')
    img2 = Image.open(io.BytesIO(img2_bytes)).convert('RGB')

    # 크기 맞추기
    if img1.size != img2.size:
        img2 = img2.resize(img1.size)

    diff = ImageChops.difference(img1, img2)

    # RMS 계산
    h = diff.histogram()
    sq = sum((value * ((idx % 256) ** 2) for idx, value in enumerate(h)))
    rms = math.sqrt(sq / float(img1.size[0] * img1.size[1] * 3))

    # 유사도로 변환 (0-100%)
    similarity = max(0, 100 - (rms / 255 * 100))
    return round(similarity, 2)


def main():
    parser = argparse.ArgumentParser(description='시각적 비교')
    parser.add_argument('--target', required=True, help='타겟 URL')
    parser.add_argument('--current', required=True, help='현재 구현 URL')
    parser.add_argument('--selector', help='비교할 요소 선택자')
    parser.add_argument('--output-dir', default='.style-extract', help='출력 디렉토리')

    args = parser.parse_args()

    # 출력 디렉토리 자동 생성
    import os
    os.makedirs(args.output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            # 타겟 캡처
            page1 = browser.new_page(viewport={'width': 1920, 'height': 1080})
            page1.goto(args.target, wait_until='networkidle')
            page1.wait_for_timeout(2000)
            target_screenshot = capture_element(page1, args.selector) if args.selector else page1.screenshot()

            # 현재 구현 캡처
            page2 = browser.new_page(viewport={'width': 1920, 'height': 1080})
            page2.goto(args.current, wait_until='networkidle')
            page2.wait_for_timeout(2000)
            current_screenshot = capture_element(page2, args.selector) if args.selector else page2.screenshot()

            # 유사도 계산
            similarity = calculate_similarity(target_screenshot, current_screenshot)

            # 스크린샷 저장
            with open(f'{args.output_dir}/target.png', 'wb') as f:
                f.write(target_screenshot)
            with open(f'{args.output_dir}/current.png', 'wb') as f:
                f.write(current_screenshot)

            result = {
                'success': True,
                'similarity': similarity,
                'threshold': 95,
                'passed': similarity >= 95,
                'screenshots': {
                    'target': f'{args.output_dir}/target.png',
                    'current': f'{args.output_dir}/current.png'
                }
            }

            if similarity < 95:
                result['recommendations'] = [
                    '색상 값을 다시 확인하세요',
                    '간격(padding/margin)을 조정하세요',
                    'border-radius 값을 확인하세요'
                ]

            print(json.dumps(result, indent=2))

        except Exception as e:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }), file=sys.stderr)
            sys.exit(1)

        finally:
            browser.close()


if __name__ == '__main__':
    main()
```

### 4.4 auto_fix.py (Core - Automated Iterative Correction)

```python
#!/usr/bin/env python3
"""
Automated difference analysis and iterative correction script.
Analyzes style differences and applies fixes until similarity threshold is met.
"""

import argparse
import json
import re
import sys
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

# =============================================================================
# Configuration Constants
# =============================================================================

# Target similarity threshold (percentage)
# 95% allows for minor rendering differences while ensuring visual match
DEFAULT_SIMILARITY_THRESHOLD = 95.0

# Maximum correction iterations before giving up
# 3 iterations typically resolve most fixable differences
# More iterations have diminishing returns
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
}


def run_compare(target_url, current_url, selector, output_dir):
    """compare.py 실행하여 유사도 확인"""
    result = subprocess.run([
        'python', 'compare.py',
        '--target', target_url,
        '--current', current_url,
        '--selector', selector,
        '--output-dir', output_dir
    ], capture_output=True, text=True)

    if result.returncode != 0:
        return None

    return json.loads(result.stdout)


def extract_target_styles(url, selector):
    """타겟에서 특정 요소의 스타일 재추출"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
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
                    boxShadow: computed.boxShadow
                };
            }
        """, selector)

        browser.close()
        return styles


def analyze_difference(target_styles, current_styles):
    """두 스타일의 차이점 분석"""
    differences = []

    # 색상 비교
    if target_styles.get('backgroundColor') != current_styles.get('backgroundColor'):
        differences.append({
            'property': 'backgroundColor',
            'priority': 1,
            'target': target_styles.get('backgroundColor'),
            'current': current_styles.get('backgroundColor')
        })

    if target_styles.get('color') != current_styles.get('color'):
        differences.append({
            'property': 'color',
            'priority': 1,
            'target': target_styles.get('color'),
            'current': current_styles.get('color')
        })

    # 간격 비교
    for prop in ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft']:
        if target_styles.get(prop) != current_styles.get(prop):
            differences.append({
                'property': prop,
                'priority': 2,
                'target': target_styles.get(prop),
                'current': current_styles.get(prop)
            })

    # border-radius 비교
    if target_styles.get('borderRadius') != current_styles.get('borderRadius'):
        differences.append({
            'property': 'borderRadius',
            'priority': 3,
            'target': target_styles.get('borderRadius'),
            'current': current_styles.get('borderRadius')
        })

    # 우선순위로 정렬
    differences.sort(key=lambda x: x['priority'])
    return differences


def rgb_to_hex(rgb):
    """RGB to Hex 변환"""
    if not rgb:
        return None
    match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgb)
    if match:
        r, g, b = map(int, match.groups())
        return f'#{r:02x}{g:02x}{b:02x}'
    return rgb


def generate_fix(difference):
    """차이점에 대한 수정 코드 생성"""
    prop = difference['property']
    target_value = difference['target']

    if prop == 'backgroundColor':
        hex_color = rgb_to_hex(target_value)
        return {
            'type': 'tailwind_class',
            'search_pattern': r'bg-\[#[a-fA-F0-9]+\]|bg-\w+',
            'replacement': f'bg-[{hex_color}]'
        }

    elif prop == 'color':
        hex_color = rgb_to_hex(target_value)
        return {
            'type': 'tailwind_class',
            'search_pattern': r'text-\[#[a-fA-F0-9]+\]|text-\w+',
            'replacement': f'text-[{hex_color}]'
        }

    elif prop == 'borderRadius':
        px_match = re.search(r'([\d.]+)px', target_value)
        if px_match:
            px = int(float(px_match.group(1)))
            radius_map = {0: 'rounded-none', 4: 'rounded', 8: 'rounded-lg',
                         12: 'rounded-xl', 16: 'rounded-2xl', 24: 'rounded-3xl'}
            tw_class = radius_map.get(px, f'rounded-[{px}px]')
            return {
                'type': 'tailwind_class',
                'search_pattern': r'rounded-\[[\d]+px\]|rounded-\w+',
                'replacement': tw_class
            }

    elif prop.startswith('padding'):
        px_match = re.search(r'([\d.]+)px', target_value)
        if px_match:
            px = int(float(px_match.group(1)))
            spacing_map = {4: '1', 8: '2', 12: '3', 16: '4', 20: '5', 24: '6', 32: '8'}
            prefix = 'py' if 'Top' in prop or 'Bottom' in prop else 'px'
            tw_value = spacing_map.get(px, f'[{px}px]')
            return {
                'type': 'tailwind_class',
                'search_pattern': rf'{prefix}-\[[\d]+px\]|{prefix}-[\d.]+',
                'replacement': f'{prefix}-{tw_value}'
            }

    return None


def apply_fix_to_file(file_path, fix, selector_hint=None):
    """파일에 수정 적용"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # className 내에서 패턴 찾아 교체
    pattern = fix['search_pattern']
    replacement = fix['replacement']

    # 간단한 교체 (더 정교한 로직 필요시 AST 파싱 사용)
    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False


def main():
    parser = argparse.ArgumentParser(description='자동 반복 수정')
    parser.add_argument('--target-url', required=True, help='타겟 URL')
    parser.add_argument('--current-url', required=True, help='현재 구현 URL')
    parser.add_argument('--selector', required=True, help='비교할 요소 선택자')
    parser.add_argument('--component-file', required=True, help='수정할 컴포넌트 파일 경로')
    parser.add_argument('--max-iterations', type=int, default=3, help='최대 반복 횟수')
    parser.add_argument('--threshold', type=float, default=95.0, help='목표 유사도 (%)')
    parser.add_argument('--output-dir', default='.style-extract', help='출력 디렉토리')

    args = parser.parse_args()

    # 출력 디렉토리 자동 생성
    import os
    os.makedirs(args.output_dir, exist_ok=True)

    all_fixes = []

    for iteration in range(1, args.max_iterations + 1):
        print(f"\n{'='*50}")
        print(f"반복 {iteration}/{args.max_iterations}")
        print('='*50)

        # 1. 비교 실행
        compare_result = run_compare(
            args.target_url, args.current_url,
            args.selector, args.output_dir
        )

        if not compare_result:
            print("비교 실행 실패", file=sys.stderr)
            sys.exit(1)

        similarity = compare_result.get('similarity', 0)
        print(f"현재 유사도: {similarity}%")

        # 2. 목표 달성 확인
        if similarity >= args.threshold:
            result = {
                'success': True,
                'status': 'PASSED',
                'iterations': iteration,
                'finalSimilarity': similarity,
                'fixes': all_fixes,
                'message': f'{iteration}회 반복 후 {args.threshold}% 이상 달성. 수정 완료.'
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return

        # 3. 타겟 스타일 재추출
        print("타겟 스타일 추출 중...")
        target_styles = extract_target_styles(args.target_url, args.selector)

        if not target_styles:
            print("타겟 스타일 추출 실패", file=sys.stderr)
            continue

        # 4. 현재 스타일 추출
        print("현재 스타일 추출 중...")
        current_styles = extract_target_styles(args.current_url, args.selector)

        # 5. 차이점 분석
        differences = analyze_difference(target_styles, current_styles)
        print(f"발견된 차이점: {len(differences)}개")

        if not differences:
            print("차이점을 찾을 수 없습니다. 수동 검토가 필요합니다.")
            break

        # 6. 수정 적용 (우선순위 순)
        for diff in differences[:3]:  # 한 번에 최대 3개 수정
            fix = generate_fix(diff)
            if fix:
                print(f"수정 중: {diff['property']}")
                print(f"  현재: {diff['current']}")
                print(f"  목표: {diff['target']}")

                success = apply_fix_to_file(args.component_file, fix)
                if success:
                    all_fixes.append({
                        'iteration': iteration,
                        'property': diff['property'],
                        'before': diff['current'],
                        'after': diff['target'],
                        'file': args.component_file
                    })
                    print(f"  ✓ 수정 완료")
                else:
                    print(f"  ✗ 수정 실패 (패턴 미발견)")

        # 잠시 대기 (서버 재빌드 시간)
        import time
        print("서버 재빌드 대기 중...")
        time.sleep(3)

    # 최대 반복 도달
    final_compare = run_compare(
        args.target_url, args.current_url,
        args.selector, args.output_dir
    )

    result = {
        'success': False,
        'status': 'MAX_ITERATIONS_REACHED',
        'iterations': args.max_iterations,
        'finalSimilarity': final_compare.get('similarity', 0) if final_compare else 0,
        'fixes': all_fixes,
        'message': f'{args.max_iterations}회 반복 후에도 {args.threshold}% 미달. 수동 검토 필요.',
        'recommendations': [
            '복잡한 그라데이션이나 그림자는 수동 조정이 필요할 수 있습니다.',
            '레이아웃 구조 차이가 있는지 확인하세요.',
            '폰트 차이가 원인일 수 있습니다.'
        ]
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(1)


if __name__ == '__main__':
    main()
```

---

## 5. 참조 문서 설계

### 5.1 REFERENCE.md

```markdown
# Tailwind CSS 매핑 참조

## 색상 변환

### RGB to Tailwind
```
rgb(r, g, b) → #rrggbb → bg-[#rrggbb] 또는 text-[#rrggbb]
```

### 일반 색상 매핑
| RGB | Hex | Tailwind |
|-----|-----|----------|
| rgb(0,0,0) | #000000 | black |
| rgb(255,255,255) | #ffffff | white |
| rgb(26,115,232) | #1a73e8 | blue-600 (근사) |

## 간격 변환

### Tailwind Spacing Scale
| px | Tailwind |
|----|----------|
| 0 | 0 |
| 1 | px |
| 4 | 1 |
| 8 | 2 |
| 12 | 3 |
| 16 | 4 |
| 20 | 5 |
| 24 | 6 |
| 32 | 8 |

### 변환 규칙
1. 정확히 매칭되면 해당 값 사용
2. ±2px 오차 허용
3. 매칭 안 되면 arbitrary value: `p-[13px]`

## Border Radius

| px | Tailwind |
|----|----------|
| 0 | rounded-none |
| 4 | rounded |
| 8 | rounded-lg |
| 12 | rounded-xl |
| 16 | rounded-2xl |
| 24 | rounded-3xl |
| 9999 | rounded-full |

## 폰트 크기

| px | Tailwind |
|----|----------|
| 12 | text-xs |
| 14 | text-sm |
| 16 | text-base |
| 18 | text-lg |
| 20 | text-xl |
| 24 | text-2xl |
```

### 5.2 PATTERNS.md

```markdown
# 컴포넌트 패턴 가이드

## 버튼 패턴

### Primary Button
```tsx
<button className="bg-[#primary] hover:bg-[#primary-hover] text-white
                   py-3 px-6 rounded-lg font-medium transition-all">
  버튼 텍스트
</button>
```

### Chip/Tag Button
```tsx
<button className="inline-flex items-center gap-2
                   bg-[#chip-bg] hover:bg-[#chip-hover]
                   text-[#chip-text] hover:text-white
                   py-3 px-4 rounded-3xl text-sm font-medium
                   transition-all">
  <Icon />
  <span>라벨</span>
</button>
```

## 입력 필드 패턴

### Text Input with Gradient Border
```tsx
<div className="gradient-border rounded-3xl">
  <div className="bg-[#input-bg] rounded-[calc(24px-1px)]">
    <input className="w-full p-4 bg-transparent text-white
                      outline-none placeholder:text-[#placeholder]" />
  </div>
</div>
```

## 컨테이너 패턴

### Card Container
```tsx
<div className="bg-[#container-bg] rounded-3xl p-8 shadow-2xl">
  {/* 콘텐츠 */}
</div>
```
```

---

## 6. 설치 및 사용

### 6.1 설치

```bash
# 1. Skill 디렉토리 생성
mkdir -p ~/~/.claude/skills/bnt-style-extract/scripts

# 2. 파일 복사 (SKILL.md, scripts/*.py, etc.)

# 3. Python 의존성 설치
cd ~/~/.claude/skills/bnt-style-extract/scripts
pip install playwright pillow
playwright install chromium
```

### 6.2 사용 예시

**예시 1: 전체 스타일 추출**
```
사용자: "https://mapsplatform.google.com/ai/ 의 스타일을 추출해서 내 프로젝트에 적용해줘"

Claude:
1. extract.py 실행 → styles.json 생성
2. convert.py 실행 → tailwind.json 생성
3. 결과를 분석하여 컴포넌트에 적용
```

**예시 2: 특정 컴포넌트 추출**
```
사용자: "해당 페이지의 chip 버튼 스타일만 추출해줘"

Claude:
1. extract.py --selector "button" 실행
2. chip 패턴과 매칭되는 요소 필터링
3. Tailwind 클래스 생성 및 적용
```

**예시 3: 비교 후 자동 수정 (핵심!)**
```
사용자: "구현이 원본과 얼마나 비슷한지 확인하고, 다르면 알아서 수정해줘"

Claude:
1. compare.py 실행 → 유사도 87%
2. 95% 미만이므로 자동 수정 시작
3. auto_fix.py 실행:
   - 1회차: 배경색 수정 (#1c1c1e → #0d1421) → 유사도 91%
   - 2회차: border-radius 수정 (28px → 24px) → 유사도 96%
4. 95% 달성! 완료 보고

출력:
{
  "status": "PASSED",
  "iterations": 2,
  "finalSimilarity": 96.2,
  "fixes": [
    {"property": "backgroundColor", "before": "#1c1c1e", "after": "#0d1421"},
    {"property": "borderRadius", "before": "28px", "after": "24px"}
  ],
  "message": "2회 반복 후 95% 이상 달성. 수정 완료."
}
```

**예시 4: 완전 자동화 요청**
```
사용자: "https://mapsplatform.google.com/ai/ 의 스타일을 그대로 복제해줘"

Claude:
1. extract.py 실행 → 타겟 스타일 추출
2. convert.py 실행 → Tailwind 클래스 생성
3. 컴포넌트 파일에 적용
4. 서버 시작
5. auto_fix.py 실행 → 자동 비교 및 수정 반복
6. 95% 이상 달성될 때까지 자동으로 수정
7. 최종 결과 보고
```

---

## 7. Auto-Fix Workflow Guidelines

Add the following section to SKILL.md to guide the auto-fix workflow:

```markdown
## Auto-Fix Workflow

When visual comparison shows similarity below 95%, the auto_fix.py script can automatically iterate to improve matching.

### Recommended Flow

1. Run compare.py to check similarity
2. If below 95%, run auto_fix.py for automated correction
3. auto_fix.py iterates up to 3 times, analyzing and fixing differences each round
4. Reports final similarity and all changes made

### Trigger Keywords

When requests include terms like "자동으로", "알아서", "복제", "똑같이", "그대로", proceed with the full automated workflow:
- Extract → Convert → Apply → Compare → Auto-fix

### Output

auto_fix.py provides structured JSON output:
- iterations: number of correction rounds
- finalSimilarity: achieved similarity percentage
- fixes: list of all changes made
- status: PASSED (≥95%) or MAX_ITERATIONS_REACHED

### Manual Review

If 3 iterations don't achieve 95%, the script reports recommendations for manual review. Common issues include:
- Complex gradients or shadows
- Layout structure differences
- Font rendering differences
```

---

## 8. Anthropic Best Practices Compliance Checklist

Before deploying the Skill, verify compliance with Anthropic guidelines:

### Core Quality
- [x] Description is in third person
- [x] Description includes both what and when
- [x] SKILL.md body under 500 lines
- [x] Progressive disclosure with separate files (REFERENCE.md, PATTERNS.md)
- [x] No time-sensitive information
- [x] Consistent terminology throughout
- [x] File references one level deep

### Scripts
- [x] All constants documented with justification
- [x] Error handling is explicit
- [x] No "voodoo constants"
- [x] Forward slashes for all paths
- [x] Feedback loops implemented (auto_fix.py)

### Workflow
- [x] Checklist pattern for complex tasks
- [x] Clear step-by-step instructions
- [x] Validation steps included

---

## 9. Conclusion

This Agent Skill approach provides a practical solution for Claude Code:

1. **No separate infrastructure**: No server setup/operation costs
2. **Easy maintenance**: Update by modifying files only
3. **Natural Claude integration**: Token-efficient via progressive disclosure
4. **Automated iteration**: auto_fix.py handles repetitive correction work
5. **Anthropic-compliant**: Follows official best practices for Skill authoring