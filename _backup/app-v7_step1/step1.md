# Step 1 교육 교재: 카페 랜딩 페이지로 배우는 웹 개발 기초

---

## 우리가 만든 것

브라우저에서 보이는 "Maison de Cafe" 웹사이트는 **파일 6개**로 이루어져 있습니다.
이 교재는 그 6개 파일이 각각 무슨 역할을 하는지, 코드가 어떻게 화면이 되는지를 설명합니다.

완성된 화면 구성:

```
+--------------------------------------------+
|            SINCE 2024                      |
|         Maison de Cafe                     |  <-- 어두운 배경, 카페 이름
|    한 잔의 여유가 만드는 특별한 순간.         |
+--------------------------------------------+
|          Signature Menu                    |
|   오늘 하루, 어떤 한 잔을 선택하시겠어요?     |
|                                            |
|  [라떼]      [크루아상]     [치즈케이크]      |  <-- 흰색 카드 3개
|  ₩5,500      ₩4,800        ₩7,500         |
+--------------------------------------------+
|  LOCATION     HOURS        CONTACT         |  <-- 어두운 배경, 매장 정보
|  경기도 안양   매일 08~18   02-1234-5678    |
+--------------------------------------------+
```

이 한 페이지가 어떤 파일들로 구성되어 있는지 하나씩 살펴보겠습니다.

---

## 1. 전체 구조: 폴더와 파일

우리 프로젝트의 파일 구조입니다.

```
프로젝트 폴더/
├── app/                        ← "페이지" 관련 파일 모음
│   ├── globals.css             ← 전체 스타일 설정
│   ├── layout.tsx              ← 모든 페이지의 공통 틀
│   └── page.tsx                ← 메인 화면 (조립 설계도)
│
└── components/                 ← "부품" 모음
    ├── HeroSection.tsx         ← 상단 타이틀 영역
    ├── MenuCard.tsx            ← 메뉴 카드 1개
    └── InfoSection.tsx         ← 하단 매장 정보 영역
```

### 비유: 건물 짓기

| 폴더/파일 | 건물에 비유하면 |
|-----------|----------------|
| `app/` 폴더 | 건물 설계 사무소 |
| `layout.tsx` | 건물의 외벽과 기초 공사 (모든 층에 공통) |
| `page.tsx` | 1층 인테리어 배치도 ("여기에 소파, 여기에 테이블") |
| `globals.css` | 건물 전체에 적용되는 인테리어 기본 규칙 |
| `components/` 폴더 | 가구 공장 (소파, 테이블, 조명 등을 만드는 곳) |

**핵심 개념**: `page.tsx`는 "어디에 뭘 배치할지" 결정하고, `components/`는 "배치할 부품"을 만듭니다.

---

## 2. globals.css - 전체 스타일 설정

가장 짧은 파일부터 시작합니다.

```css
@import "tailwindcss";

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display...');
```

**딱 2줄입니다.** 이 파일이 하는 일:

| 줄 | 하는 일 | 비유 |
|----|---------|------|
| 1번 줄 | Tailwind CSS 도구를 불러옴 | 인테리어 도구 상자를 가져오는 것 |
| 2번 줄 | 예쁜 글꼴(Playfair Display)을 인터넷에서 가져옴 | 건물에 쓸 타일을 주문하는 것 |

---

## 3. layout.tsx - 모든 페이지의 공통 틀

```tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Maison de Cafe",
  description: "A cup of comfort",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="bg-stone-50 text-stone-800"
            style={{ fontFamily: "'Noto Sans KR', sans-serif" }}>
        {children}
      </body>
    </html>
  );
}
```

코드 전체를 이해할 필요는 없습니다. **3가지만** 보면 됩니다.

### (1) 브라우저 탭에 표시되는 이름

```tsx
export const metadata: Metadata = {
  title: "Maison de Cafe",        // <-- 브라우저 탭에 보이는 제목
  description: "A cup of comfort", // <-- 검색엔진에 보이는 설명
};
```

크롬 브라우저 상단 탭에 "Maison de Cafe"라고 표시되는 이유가 바로 이 부분입니다.

### (2) 페이지 전체의 기본 스타일

```tsx
<body className="bg-stone-50 text-stone-800" ...>
```

- `bg-stone-50` : 배경색을 연한 베이지로 설정
- `text-stone-800` : 글자색을 짙은 갈색으로 설정

이것이 바로 **Tailwind CSS**입니다. 영어 단어로 된 꾸미기 명령을 `className`에 나열하면 됩니다.
자세한 설명은 뒤에서 다룹니다.

### (3) {children} - "여기에 내용이 들어갑니다" 표시

```tsx
<body ...>
  {children}
</body>
```

`{children}`은 **"여기에 실제 페이지 내용이 표시됩니다"** 라는 뜻입니다.
액자에 비유하면, layout.tsx는 액자 틀이고, `{children}`은 액자 안에 들어갈 그림 자리입니다.
그 "그림"이 바로 다음에 설명할 `page.tsx`입니다.

```
layout.tsx (액자 틀)
+----------------------------------+
|  <html>                          |
|    <body>                        |
|      +------------------------+  |
|      |                        |  |
|      |    {children} 자리     |  |  <-- 여기에 page.tsx 내용이 들어감
|      |                        |  |
|      +------------------------+  |
|    </body>                       |
|  </html>                         |
+----------------------------------+
```

---

## 4. page.tsx - 메인 화면 조립 설계도

이 파일이 우리 웹사이트의 **핵심**입니다. 화면에 보이는 모든 것의 배치를 결정합니다.

```tsx
import HeroSection from "@/components/HeroSection";
import MenuCard from "@/components/MenuCard";
import InfoSection from "@/components/InfoSection";

export default function Home() {
  return (
    <div className="min-h-screen">
      <HeroSection />

      <section className="py-12 px-6">
        <h2 ...>Signature Menu</h2>
        <p ...>오늘 하루, 어떤 한 잔을 선택하시겠어요?</p>

        <div className="max-w-3xl mx-auto grid grid-cols-3 gap-6">
          <MenuCard emoji="☕" name="시그니처 라떼"     price="₩5,500" ... />
          <MenuCard emoji="🥐" name="버터 크루아상"     price="₩4,800" ... />
          <MenuCard emoji="🍰" name="바스크 치즈케이크"  price="₩7,500" ... />
        </div>
      </section>

      <InfoSection />
    </div>
  );
}
```

### 이 파일을 3단계로 나눠서 읽겠습니다.

**[1단계] 부품 가져오기 (import)**

```tsx
import HeroSection from "@/components/HeroSection";
import MenuCard from "@/components/MenuCard";
import InfoSection from "@/components/InfoSection";
```

"components 폴더에서 부품 3종을 가져오겠다"는 선언입니다.
요리에 비유하면 **재료 준비** 단계입니다. 냉장고(components 폴더)에서 재료를 꺼내는 것과 같습니다.

**[2단계] 배치하기 (return 안의 내용)**

```tsx
return (
  <div>
    <HeroSection />          ← 1번: 상단 타이틀 영역

    <section>                ← 2번: 중간 메뉴 영역
      <MenuCard ... />
      <MenuCard ... />
      <MenuCard ... />
    </section>

    <InfoSection />          ← 3번: 하단 매장 정보
  </div>
);
```

위에서 아래로 순서대로 배치합니다.
PPT에서 텍스트 상자를 위에서 아래로 놓는 것과 같습니다.

```
화면에 보이는 순서:
 1. <HeroSection />    → 카페 이름이 보이는 어두운 영역
 2. <MenuCard /> x 3   → 메뉴 카드 3개
 3. <InfoSection />    → 위치, 시간, 연락처
```

**[3단계] MenuCard가 3번 반복되는 이유**

```tsx
<MenuCard emoji="☕" name="시그니처 라떼"     price="₩5,500" ... />
<MenuCard emoji="🥐" name="버터 크루아상"     price="₩4,800" ... />
<MenuCard emoji="🍰" name="바스크 치즈케이크"  price="₩7,500" ... />
```

같은 부품(MenuCard)을 **3번 사용**하되, 매번 **다른 내용**을 전달하고 있습니다.
이것이 바로 **컴포넌트의 핵심**: 한 번 만들면 여러 번 재사용할 수 있다는 것입니다.

비유: 같은 양식의 주문서를 3장 쓰되, 메뉴명과 가격만 다르게 적는 것과 같습니다.

---

## 5. 컴포넌트(Component) - 재사용 가능한 부품

### 컴포넌트란?

**한 번 만들면 여러 번 쓸 수 있는 화면 조각**입니다.

PPT로 비유하면: 매번 새 슬라이드를 처음부터 만드는 게 아니라, 잘 만든 템플릿 하나를 복사해서 내용만 바꾸는 것입니다.

우리 프로젝트에는 컴포넌트 3개가 있습니다:

| 컴포넌트 | 파일명 | 화면에서의 위치 | 사용 횟수 |
|----------|--------|----------------|----------|
| HeroSection | HeroSection.tsx | 맨 위 (카페 이름) | 1번 |
| MenuCard | MenuCard.tsx | 중간 (메뉴 카드) | 3번 |
| InfoSection | InfoSection.tsx | 맨 아래 (매장 정보) | 1번 |

### 컴포넌트 파일 읽는 법

가장 간단한 HeroSection을 먼저 살펴보겠습니다.

```tsx
export default function HeroSection() {
  return (
    <section className="bg-stone-900 text-stone-100 py-16 px-6 text-center">
      <p className="text-amber-400 tracking-[0.3em] text-sm mb-6 font-light">
        SINCE 2024
      </p>
      <h1 className="text-6xl font-bold mb-6 text-white"
          style={{ fontFamily: "'Playfair Display', serif" }}>
        Maison de Cafe
      </h1>
      <p className="text-stone-400 text-lg font-light max-w-md mx-auto leading-relaxed">
        한 잔의 여유가 만드는 특별한 순간.
        <br />
        매일 아침, 정성을 담아 내립니다.
      </p>
    </section>
  );
}
```

복잡해 보이지만, 구조는 단순합니다:

```
function 컴포넌트이름() {    ← "이 부품의 이름은 HeroSection입니다"
  return (
    실제 화면에 보이는 내용    ← HTML과 비슷한 형태로 작성
  );
}
```

코드 안에서 실제 화면에 표시되는 텍스트는 이것뿐입니다:
- "SINCE 2024"
- "Maison de Cafe"
- "한 잔의 여유가 만드는 특별한 순간."
- "매일 아침, 정성을 담아 내립니다."

나머지(`className="..."` 부분)는 전부 **꾸미기 명령**입니다.

---

## 6. Tailwind CSS - 영어 단어로 꾸미기

### Tailwind이란?

`className`에 영어 단어를 나열해서 스타일을 적용하는 도구입니다.
CSS(웹 디자인 언어)를 몰라도, 영어 단어의 뜻만 알면 대략 이해할 수 있습니다.

### 실제 코드로 배우기

HeroSection의 가장 바깥 태그를 보겠습니다:

```tsx
<section className="bg-stone-900 text-stone-100 py-16 px-6 text-center">
```

`className` 안에 6개의 단어가 띄어쓰기로 나열되어 있습니다.
각각의 뜻은 다음과 같습니다:

| Tailwind 클래스 | 영어 뜻 | 실제 효과 |
|-----------------|---------|----------|
| `bg-stone-900` | background: stone색 900단계 | 배경을 아주 진한 갈색(거의 검정)으로 |
| `text-stone-100` | text: stone색 100단계 | 글자를 아주 밝은 색으로 |
| `py-16` | padding-y: 16단위 | 위아래 여백을 넉넉하게 |
| `px-6` | padding-x: 6단위 | 좌우 여백을 적당히 |
| `text-center` | text: center | 글자를 가운데 정렬 |

### Tailwind 단어 읽는 규칙

패턴을 알면 대부분 읽을 수 있습니다:

```
bg-     → background (배경)
text-   → text (글자)
p-      → padding (안쪽 여백)
m-      → margin (바깥 여백)
py-     → padding의 y축, 즉 위아래
px-     → padding의 x축, 즉 좌우
mb-     → margin-bottom (아래쪽 바깥 여백)
w-      → width (너비)
h-      → height (높이)
```

색상 뒤의 숫자는 농도입니다:
```
stone-50   → 아주 연한 (거의 흰색)
stone-400  → 중간
stone-900  → 아주 진한 (거의 검정)
```

### MenuCard에서 Tailwind 확인하기

```tsx
<div className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow text-center">
```

| Tailwind 클래스 | 효과 |
|-----------------|------|
| `bg-white` | 흰색 배경 |
| `rounded-2xl` | 모서리를 둥글게 |
| `p-8` | 안쪽 여백 넉넉하게 |
| `shadow-sm` | 약한 그림자 |
| `hover:shadow-md` | 마우스를 올리면 그림자가 진해짐 |
| `transition-shadow` | 그림자 변화가 부드럽게 |
| `text-center` | 글자 가운데 정렬 |

**핵심**: 코드를 몰라도 `className` 안의 영어 단어를 읽으면 "이 부분이 어떻게 생겼을지" 대략 추측할 수 있습니다.

---

## 7. Props - 같은 부품에 다른 내용 넣기

### Props란?

컴포넌트에 전달하는 **주문서** 같은 것입니다.

카페에서 음료를 주문할 때 "아이스 아메리카노 톨 사이즈"라고 말하듯이,
컴포넌트에 "이름은 이거, 가격은 이거"라고 알려주는 것이 Props입니다.

### page.tsx에서 Props 전달하기 (주문하는 쪽)

```tsx
<MenuCard
  emoji="☕"
  name="시그니처 라떼"
  description="부드러운 우유 거품 위에 은은한 바닐라 향을 더한 시그니처 메뉴"
  price="₩5,500"
/>
```

MenuCard 부품에 4가지 정보를 전달하고 있습니다:
- `emoji` : 표시할 아이콘
- `name` : 메뉴 이름
- `description` : 메뉴 설명
- `price` : 가격

### MenuCard.tsx에서 Props 받기 (주문받는 쪽)

```tsx
interface MenuCardProps {
  emoji: string;       // 전달받을 항목 1: 아이콘 (문자)
  name: string;        // 전달받을 항목 2: 이름 (문자)
  description: string; // 전달받을 항목 3: 설명 (문자)
  price: string;       // 전달받을 항목 4: 가격 (문자)
}

export default function MenuCard({ emoji, name, description, price }: MenuCardProps) {
  return (
    <div className="...">
      <span>{emoji}</span>          ← 전달받은 아이콘을 여기에 표시
      <h3>{name}</h3>               ← 전달받은 이름을 여기에 표시
      <p>{description}</p>          ← 전달받은 설명을 여기에 표시
      <p>{price}</p>                ← 전달받은 가격을 여기에 표시
    </div>
  );
}
```

`{중괄호}` 안에 들어간 단어는 "이 자리에 전달받은 값을 표시하라"는 뜻입니다.

### Props의 흐름을 그림으로 보면

```
page.tsx (주문하는 쪽)                    MenuCard.tsx (주문받는 쪽)
+----------------------------+           +----------------------------+
|                            |           |                            |
|  <MenuCard                 |           |  function MenuCard(...)    |
|    emoji="☕"        ------+--->-------+--->  {emoji}  → ☕ 표시    |
|    name="시그니처 라떼" ---+--->-------+--->  {name}   → 시그니처 라떼|
|    description="부드러운..." -->-------+--->  {description} → 설명   |
|    price="₩5,500"    -----+--->-------+--->  {price}  → ₩5,500     |
|  />                        |           |                            |
+----------------------------+           +----------------------------+
```

같은 MenuCard를 3번 사용하면서 Props만 다르게 전달하면,
**모양은 같지만 내용이 다른 카드 3개**가 만들어집니다.

---

## 8. 전체 흐름 정리: 코드에서 화면까지

브라우저에 웹사이트가 표시되기까지의 전체 흐름입니다.

```
[1] globals.css
    "Tailwind 도구와 글꼴을 준비합니다"
         |
         v
[2] layout.tsx
    "페이지의 공통 틀을 만듭니다 (배경색, 기본 글꼴)"
    "{children} 자리에 page.tsx 내용을 넣습니다"
         |
         v
[3] page.tsx
    "부품 3종을 가져와서 순서대로 배치합니다"
    " 1. HeroSection (상단)"
    " 2. MenuCard x 3 (중간)"
    " 3. InfoSection (하단)"
         |
         v
[4] 각 컴포넌트 파일
    "자기가 맡은 영역의 내용과 디자인을 정의합니다"
    "Tailwind 클래스로 스타일을 적용합니다"
         |
         v
[5] 브라우저에 완성된 카페 웹사이트 표시
```

---

## 9. 핵심 용어 정리

이 교재에서 나온 용어를 한 곳에 모았습니다.

| 용어 | 한 줄 설명 | 비유 |
|------|-----------|------|
| **React** | 컴포넌트를 조합해서 웹사이트를 만드는 도구 | 레고 시스템 |
| **Next.js** | React를 더 편하게 쓸 수 있게 해주는 도구 | 레고 전용 작업대 |
| **컴포넌트 (Component)** | 재사용 가능한 화면 조각 | 레고 블록 1개 |
| **Tailwind CSS** | className에 영어 단어를 써서 꾸미는 도구 | 꾸미기 스티커 |
| **Props** | 컴포넌트에 전달하는 데이터 | 주문서 |
| **App Router** | app 폴더의 파일 구조로 페이지를 관리하는 방식 | 건물 층별 안내도 |
| **layout.tsx** | 모든 페이지에 공통으로 적용되는 틀 | 건물 외벽 |
| **page.tsx** | 하나의 페이지 화면을 정의하는 파일 | 방 인테리어 배치도 |
| **globals.css** | 전체 프로젝트의 기본 스타일 설정 | 건물 인테리어 기본 규칙 |
| **import** | 다른 파일에서 부품을 가져오는 명령 | 재료 꺼내기 |
| **className** | Tailwind 스타일을 적용하는 속성 | 꾸미기 명령 적는 칸 |
| **{중괄호}** | "이 자리에 데이터를 표시하라"는 표시 | 빈칸 채우기 문제의 괄호 |
| **return** | "이것을 화면에 보여줘"라는 명령 | "이게 완성품입니다" 선언 |
| **export default** | "이 부품을 다른 파일에서 쓸 수 있게 공개한다" | 가구를 매장에 진열하는 것 |

---

## 10. 직접 해보기: 텍스트 바꿔보기

코드를 직접 수정해보면 이해가 훨씬 빨라집니다.
아래 3가지를 순서대로 시도해보세요.

### 실습 1: 카페 이름 바꾸기

`components/HeroSection.tsx` 파일을 열고, 11번 줄을 찾습니다:

```tsx
        Maison de Cafe
```

이 텍스트를 원하는 카페 이름으로 바꿔보세요. 예: "나만의 카페"

저장하면 브라우저에서 즉시 바뀌는 것을 확인할 수 있습니다.

### 실습 2: 메뉴 카드 내용 바꾸기

`app/page.tsx` 파일을 열고, 첫 번째 MenuCard를 찾습니다:

```tsx
          <MenuCard
            emoji="☕"
            name="시그니처 라떼"
            description="부드러운 우유 거품 위에 은은한 바닐라 향을 더한 시그니처 메뉴"
            price="₩5,500"
          />
```

`name`, `description`, `price`의 따옴표 안 텍스트를 원하는 메뉴로 바꿔보세요.

### 실습 3: 배경 색상 바꾸기

`components/HeroSection.tsx` 파일의 3번 줄:

```tsx
    <section className="bg-stone-900 ...">
```

`bg-stone-900` 부분을 `bg-blue-900`으로 바꿔보세요.
상단 배경이 진한 파란색으로 변합니다.

다른 색도 시도해보세요: `bg-red-900`, `bg-green-900`, `bg-purple-900`

---

## 요약

```
파일 6개로 하나의 웹사이트가 완성됩니다.

globals.css  → 도구와 글꼴 준비
layout.tsx   → 공통 틀 (배경, 글꼴)
page.tsx     → 부품을 순서대로 배치 (설계도)
HeroSection  → 상단 타이틀 부품
MenuCard     → 메뉴 카드 부품 (3번 재사용)
InfoSection  → 하단 정보 부품

핵심 개념:
- Component = 재사용 가능한 화면 조각
- Tailwind = className에 영어 단어를 써서 꾸미기
- Props = 같은 부품에 다른 내용을 전달하는 방법
```
