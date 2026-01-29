# BNT Image Style Extractor 스킬 문서

디자인 이미지(PNG/JPG/스크린샷)에서 UI 스타일을 추출하여 Tailwind CSS 클래스로 변환하는 스킬.
Claude Vision + PIL 기반으로 동작한다.

## 설정

`.gitignore`에 추가:
```
.image-extract/
```

## 워크플로우 체크리스트

```
이미지 스타일 추출 진행 현황:
- [ ] Step 1: 시각 분석 (Claude가 이미지 읽기)
- [ ] Step 2: 정밀 추출 (extract_from_image.py)
- [ ] Step 2.5: 하이브리드 추출 (소스 URL이 있는 경우)
- [ ] Step 3: Tailwind 변환
- [ ] Step 4: 컴포넌트 생성
- [ ] Step 5: 비교 및 자동 수정 (compare.py)
```

---

## Step 1: 시각 분석 (Claude Vision)

디자인 이미지를 직접 읽고 다음 11가지 항목을 분석 및 문서화한다:

1. **컴포넌트 계층 구조** - 트리 형태의 중첩 구조
2. **컴포넌트 유형** - sidebar, button, card, input, nav-item 등
3. **레이아웃 방향** - 수직/수평, flex-col/flex-row
4. **폰트 크기 추정** - 각 텍스트 요소의 높이를 px 단위로 추정 (Step 2에서 자동 보정)
5. **텍스트 색상 분석** - white / off-white / light gray / dark gray / black 구분 (Step 2에서 자동 보정)
6. **폰트 굵기 추정** - thin / light / normal / medium / bold (Step 2에서 자동 보정)
7. **아이콘 크기** - 아이콘의 가로 x 세로 px 추정
8. **선 두께** - 아이콘 및 테두리의 선 두께 (1 / 1.5 / 2px)
9. **폰트 패밀리 힌트** - serif / sans-serif / monospace, 기하학적 / 휴머니스트
10. **간격 패턴** - 요소 간 간격, 섹션 패딩을 px 단위로 (Step 2에서 자동 측정)
11. **바운딩 영역** - Step 2에서 사용할 JSON 좌표

바운딩 영역 JSON 형식:
```json
[
  {"name": "sidebar-header", "bounds": {"x": 0, "y": 0, "w": 213, "h": 48}},
  {"name": "nav-item-home", "bounds": {"x": 0, "y": 48, "w": 213, "h": 44}}
]
```

`.image-extract/regions.json`에 저장한다.

### 시각 분석 출력 템플릿

Step 2 진행 전에 다음 형식으로 분석 결과를 정리한다:

```
시각 분석 결과:
- 폰트 크기: header=18px, nav-item=14px, label=12px (Step 2에서 자동 보정)
- 폰트 굵기: header=normal, nav-item=medium (Step 2에서 자동 보정)
- 텍스트 색상: primary=#ffffff, secondary=#e5e7eb, muted=#9ca3af (Step 2에서 자동 보정)
- 아이콘 크기: nav-icons=24x24px
- 선 두께: nav-icons=1.5
- 폰트 패밀리: sans-serif, geometric
- 간격: nav-item-gap=4px, section-padding=16px (Step 2에서 자동 측정)
```

---

## Step 2: 정밀 추출

Step 1의 이미지와 영역 정보를 사용하여 `extract_from_image.py`를 실행한다.

```bash
# 팔레트만 추출
python ~/.claude/skills/bnt-image-extract/scripts/extract_from_image.py \
  --image "path/to/design.png"

# Step 1의 영역 정보 포함
python ~/.claude/skills/bnt-image-extract/scripts/extract_from_image.py \
  --image "path/to/design.png" \
  --regions ".image-extract/regions.json"
```

**매개변수:**
- `--image` (필수): 디자인 이미지 경로
- `--regions`: Step 1에서 생성한 영역 좌표 JSON 파일
- `--output`: 출력 경로 (기본값: `.image-extract/styles.json`)
- `--palette-size`: 추출할 주요 색상 수 (기본값: 10)

**출력:** `.image-extract/styles.json` - 색상 팔레트, 영역 스타일, bnt-style-extract 파이프라인 호환 elements 배열 포함.

### 자동 추출 기능 (P1-P5)

- **폰트 크기 (P1)**: 배경 대비 분석을 통한 픽셀 레벨 텍스트 높이 측정 후, cap-height 비율(0.72)로 폰트 크기 변환. 측정 실패 시 휴리스틱 계산으로 폴백.
- **요소 간격 (P2)**: 이름 접두사로 반복 요소 그룹을 자동 탐지 (예: "bar-attack", "bar-magic" -> "bar" 그룹). 간격을 측정하여 Tailwind gap 클래스 출력.
- **배경 그라디언트 (P3)**: 수직/수평 스트립 샘플링 (10개 포인트, 중앙 60%). 단조 밝기 변화를 감지하여 `bg-gradient-{direction} from-[#hex] to-[#hex]` 생성.
- **폰트 굵기 (P4)**: 수평 획 런렝스 분석. 중앙값 획 두께 / 폰트 크기 비율로 CSS weight (200-800) 매핑.
- **텍스트 색상 (P5)**: 내부 픽셀만 샘플링 (4방향 이웃이 모두 비배경인 픽셀). 안티앨리어싱 가장자리 아티팩트 제외.

---

## Step 2.5: 하이브리드 추출 (선택)

디자인의 소스 URL을 알고 있는 경우, 두 가지 추출 방법을 결합하여 정확도를 높인다.

### 의사결정 흐름

```
소스 URL 확인 가능?
  |- 예 -> bnt-style-extract 먼저 실행 (정확한 CSS 값 추출)
  |        그 다음 bnt-image-extract 실행 (시각적 검증)
  |        병합: CSS 값을 기본으로, 이미지 데이터를 폴백으로 사용
  |- 아니오 -> 이미지 전용 추출로 진행 (Step 3)
```

### 절차

1. **CSS 추출 우선**: bnt-style-extract로 소스 URL에서 정확한 computed 스타일 추출 (font-size, color, padding 등)
2. **이미지 검증**: bnt-image-extract로 추출된 스타일이 디자인 이미지와 일치하는지 시각적으로 확인
3. **병합 전략**: 타이포그래피(font-size, font-weight, line-height, color)는 CSS 추출 값 우선, 레이아웃 및 시각 요소는 이미지 추출 값 사용

### 사용 시점

- 디자인 이미지가 라이브 웹사이트의 스크린샷인 경우
- 소스 URL에 접근 가능하고 이미지와 동일한 콘텐츠를 렌더링하는 경우
- 이미지 추출에서 폰트 크기나 텍스트 색상의 신뢰도가 낮은 경우

---

## Step 3: Tailwind 변환

추출된 스타일을 기반으로 Tailwind CSS 클래스로 변환한다.

색상, 간격, 타이포그래피 매핑 규칙은 [REFERENCE.md](REFERENCE.md) 참조.

**변환 우선순위:**
1. 배경 색상 -> `bg-[#hex]` 또는 Tailwind 명명 색상
2. 텍스트 색상 -> `text-[#hex]`
3. 크기 -> `w-[Npx]`, `h-[Npx]` 또는 Tailwind 스케일
4. 간격 -> `p-N`, `gap-N` 등
5. 테두리 반경 -> `rounded-*`
6. 레이아웃 -> `flex`, `flex-col`, `items-center` 등

**참고:** 폰트 크기와 굵기는 시각 분석에서 추정된 값이다. 일반적인 UI 규칙:
- 섹션 헤더: `text-xs` (12px), `font-normal`, `text-gray-400`
- 네비게이션 항목: `text-sm` (14px), `font-medium`
- 로고 텍스트: `text-base` (16px), `font-semibold`

---

## Step 4: 컴포넌트 생성

추출된 Tailwind 클래스로 React/TSX 컴포넌트를 생성한다.

컴포넌트 패턴과 템플릿은 [PATTERNS.md](PATTERNS.md) 참조.

감지된 컴포넌트 유형별 패턴 매칭:
- Sidebar -> PATTERNS.md의 Sidebar 패턴
- Button -> Button 패턴
- Card -> Card 패턴
- Input -> Input 패턴
- Navigation items -> 추출된 스타일 기반 커스텀

---

## Step 5: 비교 및 자동 수정

컴포넌트 생성 후 원본 디자인과 비교한다.

```bash
# 원본 이미지 vs 실행 중인 구현체 비교
python ~/.claude/skills/bnt-image-extract/scripts/compare.py \
  --original "path/to/design.png" \
  --current-url "http://localhost:3001" \
  --selector ".sidebar"

# 스크린샷 파일과 비교
python ~/.claude/skills/bnt-image-extract/scripts/compare.py \
  --original "path/to/design.png" \
  --current-image ".image-extract/current.png"
```

**매개변수:**
- `--original` (필수): 원본 디자인 이미지 경로
- `--current-url`: 스크린샷 캡처할 URL (Playwright 사용)
- `--current-image`: 구현체 스크린샷 파일 경로 (URL 대안)
- `--selector`: 특정 요소의 CSS 선택자
- `--output-dir`: 출력 파일 디렉토리 (기본값: `.image-extract`)
- `--threshold`: 유사도 임계값 (기본값: 95%)
- `--metric`: 유사도 측정 방식 - `ssim` (기본값, 구조적), `rms` (레거시), `both` (양쪽 모두)
- `--font-search`: 차이 밴드 분석으로 폰트 크기 조정 제안
- `--auto-viewport` (P6): Playwright 뷰포트를 원본 이미지 크기에 자동 맞춤. 리사이즈 아티팩트 제거.
- `--regions` (P7): 영역 JSON 파일 경로. 영역별 SSIM 분석으로 어떤 컴포넌트가 가장 차이가 큰지 식별.

### 비교 메트릭 설명

| 메트릭 | 설명 | 특징 |
|--------|------|------|
| `ssim` | 구조적 유사도 지수 (Structural Similarity Index) | 인간 시각 인지에 가까움. 밝기/대비/구조 비교. 기본값. |
| `rms` | 픽셀 값 차이의 제곱 평균 제곱근 | 단순하고 빠르지만 미세한 색상 차이에 민감. 레거시 호환. |
| `both` | 두 메트릭 모두 계산 | 기본 판정은 SSIM 기준, RMS는 참고용으로 함께 출력. |

### 자동 수정 루프

유사도 < 95%인 경우 반복:

```
1. diff 이미지 확인 (.image-extract/diff.png)
2. 원본 이미지와 diff를 비교하여 문제 영역 식별
3. --font-search로 폰트 크기 불일치 탐지:
   python ~/.claude/skills/bnt-image-extract/scripts/compare.py \
     --original "design.png" --current-image ".image-extract/current.png" \
     --font-search
3.5. --regions로 영역별 SSIM 분석 (P7):
   python ~/.claude/skills/bnt-image-extract/scripts/compare.py \
     --original "design.png" --current-image ".image-extract/current.png" \
     --regions ".image-extract/regions.json"
   -> 어떤 영역의 SSIM 점수가 가장 낮은지 식별
4. 문제 영역에서 색상 재추출 (Step 2를 정제된 영역으로 재실행)
5. 새 데이터와 font-search 제안을 기반으로 Tailwind 클래스 조정
6. 빌드 후 재비교 (URL 비교 시 --auto-viewport 사용)
7. 반복 (최대 3회)
```

**수정 우선순위:**

| 순위 | 유형 | 조치 |
|------|------|------|
| 1 | 배경/텍스트 색상 | 영역 재샘플링, `bg-*`/`text-*` 업데이트 |
| 2 | 폰트 크기/굵기 | `--font-search` 실행, `text-*`/`font-*` 조정 |
| 3 | 간격/패딩 | 간격 재측정, `p-*`/`gap-*` 업데이트 |
| 4 | 테두리 반경 | 모서리 재추정, `rounded-*` 업데이트 |
| 5 | 레이아웃 방향 | `flex-col`/`flex-row`, 정렬 수정 |

---

## 트리거 키워드

다음 키워드가 포함된 요청에서 활성화:
- 한국어: "이미지에서 추출", "스크린샷에서", "디자인 이미지", "이미지 기반", "그림에서"
- 영어: "from image", "from screenshot", "image to code", "design to tailwind"
- 자동 수정: "자동으로", "알아서", "똑같이" / "automatically", "clone", "exactly like"

---

## bnt-style-extract와의 차이점

| 항목 | bnt-style-extract | bnt-image-extract |
|------|-------------------|-------------------|
| 입력 | 라이브 웹사이트 URL | 이미지 파일 (PNG/JPG) |
| 추출 방식 | Playwright DOM 접근 | PIL 픽셀 분석 + Claude Vision |
| 호버 상태 | 캡처 가능 | 불가 (일반 패턴 제안) |
| 비교 대상 | 웹사이트 스크린샷 | 로컬 이미지 파일 |

---

## 주의사항

1. **폰트 추정**: 폰트 크기는 픽셀 레벨 텍스트 높이 분석(P1)으로 자동 측정된다. 폰트 굵기는 획 두께 비율(P4)로 추정된다. 모두 표준 값으로 스냅된다. 비교 시 `--font-search`로 불일치를 검증한다.
2. **안티앨리어싱**: 이미지 가장자리에서 중간 색상이 나타날 수 있다. 텍스트 색상 추출(P5)은 내부 픽셀만 샘플링하여 가장자리 아티팩트를 제외한다. 팔레트 추출은 0.5% 미만 픽셀 커버리지 색상을 필터링한다.
3. **해상도 의존성**: 추출된 픽셀 치수는 이미지 해상도에 따라 달라진다. 디자인 이미지가 축소/확대된 경우 비례 조정이 필요하다. `--auto-viewport` (P6)을 사용하여 뷰포트를 원본 이미지 크기에 맞출 수 있다.
4. **그라디언트 감지**: 배경 그라디언트(P3)는 영역 내 최소 15 RGB 단위의 단조 밝기 변화가 필요하다. 미세하거나 비선형 그라디언트는 감지되지 않을 수 있다.
5. **간격 측정**: 요소 간격(P2)은 동일한 이름 접두사를 가진 최소 2개 요소가 필요하다 (예: "bar-attack", "bar-magic"). 단일 요소나 다른 이름의 요소는 간격 감지를 트리거하지 않는다.
6. **CSS 메커니즘 한계**: 이미지 전용 추출은 CSS 필터(hue-rotate, sepia, contrast), 중첩 요소 구조, 호버 상태를 감지할 수 없다. 이런 경우 Step 2.5 하이브리드 추출을 사용한다.
7. **하이브리드 워크플로우 권장**: 디자인 소스 URL을 알고 있다면, 항상 Step 2.5 하이브리드 추출을 사용한다. 이미지 전용 추출은 타이포그래피에 본질적인 한계가 있다.

---

## 디렉토리 구조

경로: `~/.claude/skills/bnt-image-extract/`

```
bnt-image-extract/
  SKILL.md                          # 스킬 정의 (Claude가 자동으로 읽는 진입점)
  REFERENCE.md                      # Tailwind CSS 매핑 레퍼런스
  PATTERNS.md                       # 컴포넌트 패턴 템플릿 모음
  scripts/
    extract_from_image.py           # 이미지에서 스타일 추출 (메인 스크립트)
    compare.py                      # 원본 vs 구현체 시각 비교
    utils/
      __init__.py                   # 유틸리티 패키지 (공개 API 정의)
      color.py                      # 색상 변환 유틸리티
      spacing.py                    # 간격/패딩 변환 유틸리티
      tailwind.py                   # Tailwind CSS 변환 엔진
  templates/
    component.tsx                   # 기본 컴포넌트 템플릿
```

---

## 파일별 상세 설명

### SKILL.md (스킬 정의)

Claude가 스킬 활성화 시 자동으로 읽는 파일. frontmatter에 메타데이터를 포함한다.

**frontmatter:**
```yaml
name: bnt-image-extract
description: Extracts UI/UX styles from design images (PNG/JPG/screenshot) and
             converts them to Tailwind CSS classes. Triggers on requests mentioning
             image style extraction, screenshot-to-code, design-to-tailwind, UI
             image cloning, or creating components from design images.
```

**포함 내용:**
- 워크플로우 체크리스트 (Step 1~5 + Step 2.5)
- Step 1: 시각 분석 가이드 (11개 분석 항목 + 출력 템플릿)
- Step 2: 정밀 추출 CLI 사용법 + 자동 추출 기능 (P1-P5)
- Step 2.5: 하이브리드 추출 절차
- Step 3: Tailwind 변환 우선순위
- Step 4: 컴포넌트 생성 패턴 매칭
- Step 5: 비교 및 자동 수정 루프 (메트릭, font-search, auto-viewport P6, regions P7 포함)
- 트리거 키워드 (한국어/영어)
- bnt-style-extract와의 차이점
- 주의사항 7가지

---

### REFERENCE.md (Tailwind CSS 매핑 레퍼런스)

CSS 속성값을 Tailwind 클래스로 변환하기 위한 매핑 테이블 모음.

**포함 매핑 테이블:**

| 섹션 | 내용 | 예시 |
|------|------|------|
| Color Conversion | RGB/RGBA -> Tailwind 색상 | `rgb(0,0,0)` -> `black` |
| Spacing Scale | px -> Tailwind 간격 스케일 | `16px` -> `4` (= `p-4`) |
| Padding/Margin | 방향별 접두사 | `pt-`, `px-`, `my-` 등 |
| Border Radius | px -> rounded 클래스 | `8px` -> `rounded-lg` |
| Font Size | px -> text 클래스 | `14px` -> `text-sm` |
| Font Weight | CSS 수치 -> font 클래스 | `600` -> `font-semibold` |
| Box Shadow | CSS shadow -> shadow 클래스 | blur 8px -> `shadow-md` |
| Opacity | 소수점 -> opacity 클래스 | `0.5` -> `opacity-50` |
| Flexbox | display/direction/align/justify | `flex-col`, `items-center` |
| Gap | px -> gap 클래스 | `16px` -> `gap-4` |
| Transitions | duration/timing/property | `duration-200`, `ease-out` |

**변환 규칙:**
1. 정확한 값 매칭 우선
2. 허용 오차 범위 내(+-2px) 가장 가까운 값으로 스냅
3. 매칭 실패 시 임의 값 사용: `p-[13px]`

---

### PATTERNS.md (컴포넌트 패턴 템플릿)

추출된 스타일을 적용할 수 있는 TSX 컴포넌트 템플릿 모음.

**포함 패턴:**

| 카테고리 | 패턴 | 설명 |
|----------|------|------|
| Button | Primary, Secondary, Ghost, Chip/Tag, Icon | 5가지 버튼 변형. 호버 상태 포함. |
| Input | Basic, Gradient Border, Search with Icon | 3가지 입력 필드 변형 |
| Card | Basic, Image, Interactive, Glass | 4가지 카드 변형. Glassmorphism 포함. |
| Container | Page, Modal/Dialog | 페이지 컨테이너와 모달 |
| Navigation | Navbar, Sidebar | 상단 네비게이션 바, 사이드바 |
| Badge/Tag | Status Badge, Removable Tag | 상태 표시 및 태그 |
| Animation | Fade In, Slide Up | tailwind.config.js 키프레임 포함 |

각 패턴은 `[#bg-color]`, `[#text-color]` 등의 플레이스홀더를 사용하며, 추출된 실제 색상값으로 교체하여 사용한다.

---

### scripts/extract_from_image.py (이미지 스타일 추출)

디자인 이미지에서 색상 팔레트와 영역별 스타일을 추출하는 메인 스크립트.

**주요 함수:**

| 함수 | 역할 |
|------|------|
| `extract_color_palette()` | 이미지 양자화 후 주요 색상 추출 (MEDIANCUT, 기본 16색) |
| `classify_color()` | luminance/saturation 기반 색상 분류 (7개 카테고리) |
| `measure_text_height()` | (P1) 배경 대비 분석으로 픽셀 레벨 텍스트 높이 측정 |
| `estimate_font_size()` | (P1) 픽셀 측정 우선, 실패 시 휴리스틱 폴백 (표준 크기 스냅) |
| `estimate_font_weight()` | (P4) 수평 획 런렝스 분석으로 CSS font-weight 추정 (200-800) |
| `extract_text_color()` | (P5) 내부 픽셀만 샘플링하여 정확한 텍스트 색상 추출 |
| `detect_gradient()` | (P3) 수직/수평 스트립 샘플링으로 배경 그라디언트 감지 |
| `measure_element_gaps()` | (P2) 반복 요소 그룹 간격 측정 및 Tailwind gap 클래스 출력 |
| `extract_region_styles()` | 지정 영역의 배경색, 텍스트색, 폰트 크기/굵기, 그라디언트, 간격 추출 |
| `build_elements()` | bnt-style-extract 파이프라인 호환 elements 배열 생성 |

**색상 분류 카테고리:**

| 카테고리 | 조건 | 용도 |
|----------|------|------|
| `accent` | saturation > 0.5 | 강조색 (채도 높은 색) |
| `background-dark` | luminance < 0.15 | 어두운 배경 |
| `background` | luminance < 0.4 | 일반 배경 |
| `neutral` | luminance 0.4~0.6 | 중립색 |
| `text` | luminance > 0.6 | 일반 텍스트 |
| `text-light` | luminance > 0.85 | 밝은 텍스트 (off-white/light gray) |
| `text-white` | luminance > 0.95 | 순수 백색 텍스트 |

**폰트 크기 추정:**

우선 방식 (P1 - 픽셀 레벨 측정):
```
text_height = measure_text_height(cropped_image)  # 픽셀 높이
font_size = text_height / 0.72  # cap-height 비율
```

폴백 방식 (휴리스틱):
```
font_size = (region_height - vertical_padding) / line_height_ratio
```
- `line_height_ratio`: 1.5 (기본값)
- 패딩 휴리스틱: h<40 -> 8px, h<50 -> 12px, h>=50 -> 16px
- 표준 크기: 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72px
- 스냅 오차: 25% 이내

---

### scripts/compare.py (시각 비교)

원본 디자인 이미지와 구현체 스크린샷을 비교하여 유사도를 측정하는 스크립트.

**주요 함수:**

| 함수 | 역할 |
|------|------|
| `calculate_similarity()` | RMS(Root Mean Square) 기반 유사도 계산 (0~100%) |
| `calculate_ssim()` | SSIM(Structural Similarity Index) 기반 유사도 계산 (PIL-only) |
| `create_diff_image()` | 차이 시각화 이미지 생성 (3배 강조) |
| `analyze_differences()` | 상/중/하 영역별 차이 분석 |
| `suggest_font_sizes()` | 20개 수평 밴드 분석으로 폰트 크기 불일치 탐지 |
| `calculate_region_ssim()` | (P7) 영역별 SSIM 계산으로 가장 차이가 큰 컴포넌트 식별 |
| `capture_current_screenshot()` | Playwright로 URL 스크린샷 캡처 (P6: auto-viewport 지원) |

**SSIM 구현 상세:**
- PIL-only (외부 의존성 없음)
- 그레이스케일 변환 후 11x11 윈도우 슬라이딩
- step = window_size // 2 (성능 최적화, 약 4배 빠름)
- 표준 SSIM 파라미터: k1=0.01, k2=0.03

**font-search 동작 방식:**
- 이미지를 20개 수평 밴드로 분할
- 각 밴드의 평균 차이 강도 계산
- mean_diff > 15인 밴드에서 폰트 크기 후보 제안
- confidence: mean_diff > 30이면 `high`, 아니면 `medium`

---

### scripts/utils/ (유틸리티 패키지)

bnt-style-extract 파이프라인과 공유하는 변환 유틸리티.

**color.py - 색상 유틸리티:**

| 함수 | 역할 |
|------|------|
| `parse_rgb()` | `rgb()/rgba()` 문자열을 튜플로 파싱 |
| `rgb_to_hex()` | RGB 문자열/튜플을 hex 문자열로 변환 |
| `hex_to_rgb()` | hex 문자열을 RGB 튜플로 변환 |
| `color_distance()` | CIE76 근사 가중 유클리드 거리 (0~100 스케일) |
| `lighten()` / `darken()` | 색상 밝기 조절 |

**spacing.py - 간격 유틸리티:**

| 함수/상수 | 역할 |
|-----------|------|
| `SPACING_MAP` | px -> Tailwind 스케일 매핑 (0px ~ 384px) |
| `parse_px()` | CSS 값 문자열에서 px 추출 (px/rem/em 지원) |
| `spacing_to_tailwind()` | px 값을 Tailwind 클래스로 변환 (허용 오차 2px) |
| `parse_spacing_shorthand()` | CSS 축약형 파싱 (`10px 20px` -> top/right/bottom/left) |
| `optimize_spacing_classes()` | 최적화된 Tailwind 클래스 생성 (`py-4 px-6` 등) |

**tailwind.py - Tailwind 변환 엔진:**

| 함수/상수 | 역할 |
|-----------|------|
| `FONT_SIZE_MAP` | px -> `text-*` 매핑 (12px~128px) |
| `RADIUS_MAP` | px -> `rounded-*` 매핑 |
| `WEIGHT_MAP` | CSS 수치 -> `font-*` 매핑 |
| `COMMON_COLORS` | hex -> Tailwind 명명 색상 (slate 계열 등) |
| `font_size_to_tailwind()` | 폰트 크기 변환 (허용 오차 1px) |
| `radius_to_tailwind()` | 테두리 반경 변환 (허용 오차 2px) |
| `color_to_tailwind()` | 색상 변환 (명명 색상 우선, 임의 값 폴백) |
| `shadow_to_tailwind()` | 그림자 변환 (blur 크기 기반 추정) |
| `convert_to_tailwind()` | styles 딕셔너리를 Tailwind 클래스 문자열로 일괄 변환 |

`convert_to_tailwind()`가 처리하는 속성:
backgroundColor, color, fontSize, fontWeight, padding (4방향), borderRadius, borderWidth, borderColor, boxShadow, display(flex), flexDirection, alignItems, justifyContent, gap

---

### templates/component.tsx (기본 컴포넌트 템플릿)

추출된 스타일을 적용할 기본 React 컴포넌트 골격.

```tsx
/**
 * Base Component Template
 *
 * Replace placeholders with extracted values:
 * - [#bg-color]: Background color hex
 * - [#text-color]: Text color hex
 * - [padding]: Tailwind padding classes
 * - [radius]: Tailwind border-radius class
 */

import React from 'react';

interface ComponentProps {
  children: React.ReactNode;
  className?: string;
}

export function Component({ children, className = '' }: ComponentProps) {
  return (
    <div
      className={`
        bg-[#bg-color]
        text-[#text-color]
        [padding]
        [radius]
        ${className}
      `.trim().replace(/\s+/g, ' ')}
    >
      {children}
    </div>
  );
}

export default Component;
```

플레이스홀더(`[#bg-color]`, `[#text-color]`, `[padding]`, `[radius]`)를 추출된 실제 값으로 교체하여 사용한다.
