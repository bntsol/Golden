# 바이브 코딩과 웹사이트 구축

## BlueEye PoC - Next.js 프로젝트 설정 가이드

> AI(Claude)와 대화하며 웹사이트를 만드는 비개발자용 가이드

---

## 0. Node.js 설치 (최초 1회)

Node.js는 JavaScript를 PC에서 실행할 수 있게 해주는 프로그램입니다.
Node.js를 설치하면 **npm과 npx가 함께 설치**됩니다.

### 이미 설치되어 있는지 확인

VSCode에서 터미널을 열고 (`` Ctrl + ` ``) 아래 명령어를 입력합니다:

```powershell
node -v
npm -v
```

**결과 예시 (설치된 경우):**
```
v22.16.0
11.4.1
```

버전 번호가 나오면 이미 설치된 것입니다. → **"0-1. 사전 지식"으로 건너뛰세요**

**결과 예시 (설치 안 된 경우):**
```
'node'은(는) 내부 또는 외부 명령... 인식할 수 없습니다.
```

이 메시지가 나오면 아래 설치 과정을 따라하세요.

### Node.js 설치 방법

1. **다운로드 사이트 접속**
   - https://nodejs.org 접속

2. **LTS 버전 다운로드**
   - 왼쪽의 **LTS (Long Term Support)** 버튼 클릭
   - `node-v22.x.x-x64.msi` 파일이 다운로드됨

3. **설치 실행**
   - 다운로드된 `.msi` 파일 실행
   - **Next → Next → Next** (기본 설정 그대로 진행)
   - 설치 완료
   - ✅ **npm과 npx는 Node.js와 함께 자동 설치됩니다** (별도 설치 불필요)

4. **VSCode 재시작**
   - 설치 후 **VSCode를 완전히 종료했다가 다시 실행**해야 합니다
   - (터미널만 닫고 다시 여는 것으로는 안 됨)

5. **설치 확인**
   ```powershell
   node -v   # v22.x.x 이상이면 OK
   npm -v    # 10.x.x 이상이면 OK
   ```

> **참고:** LTS는 "장기 지원 버전"으로, 안정적이고 오래 지원됩니다. 특별한 이유가 없으면 항상 LTS를 선택하세요.

---

## 0-1. 사전 지식: npm과 npx 이해하기

### Node.js, npm, npx가 뭔가요?

| 용어 | 설명 | 비유 |
|------|------|------|
| **Node.js** | JavaScript를 PC에서 실행할 수 있게 해주는 프로그램 | 엔진 |
| **npm** | 패키지(라이브러리)를 **설치하고 관리**하는 도구 | 마트에서 물건 사서 집에 보관 |
| **npx** | 패키지를 **설치 없이 바로 실행**하는 도구 | 렌탈해서 쓰고 반납 |

### npm vs npx 차이

```powershell
# npm: 프로젝트에 라이브러리 설치 (계속 사용할 것)
npm install react
npm install @deck.gl/react

# npx: 한 번만 실행할 도구 (설치 없이 바로 실행)
npx create-next-app@latest
```

**언제 뭘 쓰나요?**

| 상황 | 사용 도구 | 예시 |
|------|----------|------|
| 프로젝트에서 계속 쓸 라이브러리 | `npm install` | react, deck.gl, tailwind |
| 한 번만 실행할 도구 | `npx` | create-next-app, create-vite |

### create-next-app은 "프로젝트 생성기"

`create-next-app`은 Next.js 프로젝트의 **초기 폴더/파일 구조를 자동으로 만들어주는 도구**입니다.

```
create-next-app 실행하면 생성되는 것들:

poc/
├── node_modules/      ← 라이브러리들 (수백 MB)
├── app/
│   ├── page.tsx       ← 메인 페이지
│   ├── layout.tsx     ← 레이아웃
│   └── globals.css    ← 전역 스타일
├── package.json       ← 프로젝트 설정
├── tailwind.config.ts
├── tsconfig.json
└── next.config.ts
```

**건물에 비유하면:**

| 도구 | 비유 | 사용 횟수 |
|------|------|----------|
| `create-next-app` | 건물 **기초 공사** | 한 번 |
| `npm install` | 건물에 **가구 배치** | 필요할 때마다 |
| `npm run dev` | 건물에서 **생활하기** | 매일 |

집을 지을 때 기초 공사는 **처음 한 번**만 합니다. 그 다음부터는 그 위에서 생활하고, 가구를 추가하는 것입니다.

---

## 0-2. 버전 관리: 왜 app 폴더만 백업하는가?

### ⚠️ 흔히 하는 오해

처음에는 이렇게 생각할 수 있습니다:

> "버전별로 폴더를 통째로 복사하면 되지 않나?"

```
❌ 비효율적인 방식:
BlueEye/
├── poc-step1/
│   ├── node_modules/   ← 수백 MB
│   └── app/
├── poc-step2/
│   ├── node_modules/   ← 또 수백 MB (중복!)
│   └── app/
└── poc-step3/
    ├── node_modules/   ← 또 수백 MB (중복!)
    └── app/
```

**문제점:**
- `node_modules`는 수백 MB ~ 1GB 이상
- 버전마다 중복 저장 → 용량 낭비
- 복사할 때마다 `npm install` 다시 실행해야 함 (시간 소요)

### ✅ 효율적인 방식: app 폴더만 백업

```
BlueEye/
└── poc/                      ← 프로젝트 루트 (하나만 유지)
    ├── node_modules/         ← 라이브러리 (한 번만 설치)
    ├── app/                  ← 현재 작업 폴더 (Next.js가 인식)
    ├── _backup/              ← 백업 폴더
    │   ├── app-v1/           ← 버전 1 백업
    │   ├── app-v2/           ← 버전 2 백업
    │   └── app-v3/           ← 버전 3 백업
    ├── package.json
    └── next.config.ts
```

**장점:**
- `node_modules`는 한 번만 설치
- 백업은 `app/` 폴더만 복사 (용량 작음, 빠름)
- 사소한 코드 변경마다 `npm install` 불필요

### 작업 흐름

```
1. app/에서 작업
      ↓
2. 작업 완료, 테스트 통과
      ↓
3. app/ 폴더를 _backup/app-v1/로 복사
      ↓
4. app/에서 다음 작업 계속 진행
      ↓
5. 작업 완료 → _backup/app-v2/로 복사
      ↓
   (반복)
```

### 이전 버전 실행하려면?

**중요:** Next.js는 **`app/` 폴더만 인식**합니다.

이전 버전을 실행하려면 폴더명을 교체해야 합니다:

```powershell
# 예: app-v1을 실행하고 싶을 때

# 1. 현재 app 폴더를 임시로 이름 변경
ren app app-current

# 2. 실행할 버전을 app으로 변경
ren _backup\app-v1 app

# 3. 실행
npm run dev

# 4. 확인 끝나면 원복
ren app _backup\app-v1
ren app-current app
```

### 정리: 두 가지 방식 비교

| 방식 | 장점 | 단점 |
|------|------|------|
| **폴더 통째로 복사** | 이전 버전 바로 실행 가능 | 용량 낭비, 매번 npm install |
| **app 폴더만 백업** ✅ | 용량 절약, npm install 불필요 | 이전 버전 실행 시 폴더명 교체 필요 |

**권장:** 사소한 코드 변경이 자주 있다면 **app 폴더만 백업**하는 방식이 효율적입니다.

---

## 1. 프로젝트 생성 (최초 1회만)

### 이 단계에서 하는 일

`npx create-next-app@latest poc` 명령어를 실행하면:

1. **poc 폴더 생성** - 프로젝트 루트 폴더가 만들어짐
2. **기본 파일/폴더 구조 생성** - `app/`, `public/`, 설정 파일들이 자동 생성됨
3. **기본 라이브러리 설치** - React, Next.js, TypeScript, Tailwind CSS 등이 `node_modules/`에 설치됨
4. **Git 저장소 초기화** - 버전 관리를 위한 `.git` 폴더 생성

즉, **빈 폴더에서 바로 개발을 시작할 수 있는 상태**로 만들어주는 과정입니다.

> **왜 "최초 1회만"인가?**  
> 프로젝트 뼈대는 한 번만 만들면 됩니다. 이후에는 이 폴더 안에서 코드를 수정하고, 필요한 패키지만 추가로 설치하면 됩니다. (섹션 0-2 참고)

### 실행 방법

```powershell
# 원하는 위치로 이동
cd D:\claude-projects\BlueEye

# Next.js 프로젝트 생성
npx create-next-app@latest poc
```

**설정 질문이 나오면:**

```
✔ Would you like to use the recommended Next.js defaults? → Yes
```

또는 개별 질문이 나오면:
```
✔ Would you like to use TypeScript? → Yes
✔ Would you like to use ESLint? → Yes
✔ Would you like to use Tailwind CSS? → Yes
✔ Would you like your code inside a `src/` directory? → No
✔ Would you like to use App Router? (recommended) → Yes
✔ Would you like to use Turbopack for `next dev`? → Yes
✔ Would you like to customize the import alias? → No
```

> **주의:** 프로젝트 이름은 **소문자와 하이픈(-)만** 사용 가능합니다.
> - ✅ `poc`, `poc-frontend`, `ocean-ai`
> - ❌ `PoC_step1` (대문자, 밑줄 불가)

---

## 2. 추가 패키지 설치

```powershell
# 생성된 프로젝트 폴더로 이동
cd poc

# deck.gl (지도 시각화) + maplibre (배경지도) + echarts (차트)
npm install "@deck.gl/react" "@deck.gl/core" "@deck.gl/layers" react-map-gl maplibre-gl echarts echarts-for-react
```

> **참고:** PowerShell에서 `@` 기호는 특수 문자로 인식됩니다. 따옴표(`"`)로 감싸야 오류가 발생하지 않습니다.

### 설치되는 패키지 설명

| 패키지 | 설명 |
|--------|------|
| `@deck.gl/react` | deck.gl을 React에서 사용하기 위한 패키지 |
| `@deck.gl/core` | deck.gl 핵심 기능 (지도 위 데이터 시각화 엔진) |
| `@deck.gl/layers` | deck.gl 레이어들 (점, 선, 히트맵 등 시각화 요소) |
| `react-map-gl` | React에서 지도를 쉽게 사용하기 위한 래퍼(wrapper) |
| `maplibre-gl` | **무료 오픈소스** 지도 라이브러리 (배경지도 렌더링) |
| `echarts` | Apache에서 만든 차트 라이브러리 (시계열, 비교 차트 등) |
| `echarts-for-react` | ECharts를 React에서 쉽게 사용하기 위한 래퍼 |

**deck.gl이란?**
- Uber에서 만든 대용량 데이터 시각화 라이브러리
- 지도 위에 수십만 개의 점, 경로, 히트맵 등을 빠르게 표시 가능
- 해양 데이터(관측소 위치, 수온 분포, 해류 등)를 지도에 표시하는 데 사용

**ECharts란?**
- Apache 재단에서 관리하는 오픈소스 차트 라이브러리
- 시계열 차트, 막대 차트, 파이 차트, 게이지 등 다양한 차트 지원
- 해양 플랫폼에서 수온 변화 추이, 조위 비교 등 차트 표시에 사용

| 질문 유형 | 가시화 방식 | 사용 기술 |
|----------|------------|----------|
| "부산 현재 수온" | 게이지 차트 | ECharts |
| "지난 일주일 수온 변화" | 시계열 차트 | ECharts |
| "부산 vs 인천 수온 비교" | 비교 차트 | ECharts |
| "전국 수온 분포" | 지도 히트맵 | deck.gl |
| "관측소 위치" | 지도 마커 | deck.gl |

### MapLibre GL vs Mapbox GL

| 항목 | MapLibre GL | Mapbox GL |
|------|-------------|-----------|
| **비용** | ✅ 완전 무료 | ❌ 유료 (무료 티어 제한 있음) |
| **API 키** | ✅ 불필요 | ❌ 필요 (가입 필수) |
| **라이선스** | 오픈소스 (BSD) | 독점 라이선스 (v2.0 이후) |
| **기능** | Mapbox GL v1 기반, 거의 동일 | 최신 기능 포함 |
| **커뮤니티** | 오픈소스 커뮤니티 | Mapbox 회사 |

**역사:**
- Mapbox GL은 원래 오픈소스였으나, v2.0부터 유료 독점 라이선스로 변경됨
- 이에 반발한 커뮤니티가 v1.x를 포크(fork)하여 **MapLibre GL**을 만듦
- 현재 MapLibre GL은 AWS, Meta, Microsoft 등이 후원하는 활발한 오픈소스 프로젝트

### 왜 CARTO 지도를 쓰면서 MapLibre GL이 필요한가?

**CARTO**와 **MapLibre GL**은 역할이 다릅니다:

| 구분 | 역할 | 비유 |
|------|------|------|
| **CARTO** | 지도 스타일/타일 제공 (지도 데이터) | 그림 도안 |
| **MapLibre GL** | 지도를 화면에 렌더링 (지도 엔진) | 그림 그리는 도구 |

```
CARTO (지도 스타일: dark_matter_nolabels)
         ↓ 제공
    지도 타일 데이터
         ↓ 사용
MapLibre GL (화면에 렌더링)
         ↓ 위에
    deck.gl (해양 데이터 시각화)
```

즉, **CARTO는 "어떤 지도를 보여줄지"**, **MapLibre GL은 "지도를 어떻게 그릴지"**를 담당합니다.

우리 프로젝트에서는:
- **배경지도**: CARTO의 `dark_matter_nolabels` (어두운 테마, 라벨 없음)
- **렌더링 엔진**: MapLibre GL (무료, API 키 불필요)
- **데이터 시각화**: deck.gl (해양 관측소, 수온 분포 등)

---

## 3. 파일 구조

프로젝트 생성 후 최종 폴더 구조:

```
D:\claude-projects\BlueEye\
└── poc/
    ├── .next/                    ← 빌드 결과물 (자동 생성, npm run dev 실행 시)
    ├── app/                      ← 현재 작업 폴더 ⭐
    │   ├── layout.tsx            ← 기본 레이아웃
    │   ├── page.tsx              ← 메인 페이지
    │   ├── globals.css           ← 전역 스타일
    │   └── favicon.ico           ← 브라우저 탭 아이콘
    ├── node_modules/             ← 라이브러리 (자동 생성됨)
    ├── public/                   ← 정적 파일 (이미지 등)
    ├── components/               ← 컴포넌트 폴더 (새로 생성 필요)
    │   └── OceanMap.tsx          ← 지도 컴포넌트
    ├── _backup/                  ← 백업 폴더 (새로 생성 필요)
    │   ├── app-v1/
    │   └── app-v2/
    ├── .gitignore                ← Git 제외 파일 목록
    ├── eslint.config.mjs         ← ESLint 설정
    ├── next-env.d.ts             ← Next.js 타입 정의
    ├── next.config.ts            ← Next.js 설정
    ├── package-lock.json         ← 패키지 버전 잠금
    ├── package.json              ← 프로젝트 설정
    ├── postcss.config.mjs        ← PostCSS 설정 (Tailwind용)
    ├── README.md                 ← 프로젝트 설명
    └── tsconfig.json             ← TypeScript 설정
```

### 각 폴더/파일 설명

#### 📁 자동 생성되는 폴더

| 폴더 | 설명 | 수정 여부 |
|------|------|----------|
| `.next/` | 빌드 결과물. `npm run dev` 실행 시 자동 생성됨 | ❌ 수정 금지 |
| `app/` | **메인 작업 폴더**. 페이지, 레이아웃, 스타일 등 실제 코드가 여기에 있음 | ✅ 여기서 작업 |
| `node_modules/` | 설치된 라이브러리들이 저장되는 폴더 (수백 MB). `npm install` 하면 자동 생성됨 | ❌ 절대 수정 금지 |
| `public/` | 이미지, 아이콘 등 정적 파일을 넣는 폴더 | 필요시 파일 추가 |

#### 📄 자동 생성되는 파일

| 파일 | 설명 | 수정 여부 |
|------|------|----------|
| `.gitignore` | Git에서 제외할 파일 목록 | 보통 수정 불필요 |
| `eslint.config.mjs` | 코드 문법 검사 설정 | 보통 수정 불필요 |
| `next-env.d.ts` | Next.js TypeScript 타입 정의 | ❌ 수정 금지 |
| `next.config.ts` | Next.js 설정 파일 | 필요시 수정 |
| `package-lock.json` | 설치된 라이브러리의 정확한 버전 정보 | ❌ 수정 금지 (자동 관리) |
| `package.json` | 프로젝트 설정. 프로젝트 이름, 설치된 라이브러리 목록 등 | 보통 자동 관리 |
| `postcss.config.mjs` | PostCSS 설정 (Tailwind CSS 처리용) | 보통 수정 불필요 |
| `README.md` | 프로젝트 설명 문서 | 필요시 수정 |
| `tsconfig.json` | TypeScript 설정 파일 | 보통 수정 불필요 |

#### 📁 app/ 폴더 내부 (핵심 작업 영역)

| 파일 | 설명 |
|------|------|
| `page.tsx` | **메인 페이지**. 브라우저에서 `/` 주소로 접속하면 보이는 화면 |
| `layout.tsx` | **레이아웃**. 모든 페이지에 공통으로 적용되는 틀 (HTML head, body 등) |
| `globals.css` | **전역 스타일**. 전체 사이트에 적용되는 CSS |
| `favicon.ico` | 브라우저 탭에 표시되는 아이콘 |

#### 📁 직접 생성할 폴더

| 폴더 | 설명 |
|------|------|
| `components/` | 재사용 가능한 컴포넌트들을 모아두는 폴더. `OceanMap.tsx` 등 |
| `_backup/` | 버전 백업용 폴더. `app-v1/`, `app-v2/` 등 |

### 파일 배치 방법

1. `app/` 폴더에 있는 기존 `page.tsx`, `layout.tsx`, `globals.css`를 **제공된 파일로 교체**
2. `components/` 폴더를 **poc/ 아래에 새로 생성**하고 `OceanMap.tsx` 파일 추가
3. `_backup/` 폴더를 **poc/ 아래에 새로 생성** (버전 백업용)

---

## 4. 실행

```powershell
npm run dev
```

실행 결과:
```
▲ Next.js 16.1.4 (Turbopack)
- Local:         http://localhost:3000
- Network:       http://172.29.112.1:3000
```

| 항목 | 설명 | 접속 가능 범위 |
|------|------|---------------|
| **Local** | 내 PC 전용 주소 | 내 PC에서만 |
| **Network** | 내 PC의 내부 IP 주소 | 같은 네트워크(WiFi/LAN) 내 다른 기기 |

브라우저에서 http://localhost:3000 접속

### 포트 변경 방법

Next.js는 **기본적으로 3000번 포트**를 사용합니다. 다른 서비스(예: Open WebUI)와 포트가 충돌하면 포트를 변경해야 합니다.

**방법: `package.json` 수정 (권장)**

`package.json` 파일을 열고 `scripts` 부분을 수정:

```json
"scripts": {
  "dev": "next dev --port 3001",
  "build": "next build",
  "start": "next start",
  "lint": "next lint"
},
```

저장 후 실행하면 항상 3001번 포트로 실행됩니다:

```powershell
npm run dev
```

```
- Local:         http://localhost:3001
- Network:       http://172.29.112.1:3001
```

> **참고:** 일시적으로만 포트를 바꾸려면 명령어로도 가능합니다: `npm run dev -- --port 3001`

**주요 프레임워크 기본 포트**

| 프레임워크 | 기본 포트 |
|-----------|----------|
| Next.js | 3000 |
| React (Vite) | 5173 |
| Vue | 8080 |
| Angular | 4200 |

### 자주 쓰는 npm 명령어

| 명령어 | 설명 |
|--------|------|
| `npm install` | package.json에 있는 모든 패키지 설치 |
| `npm run dev` | 개발 서버 실행 |
| `npm run build` | 배포용 빌드 |
| `npm install 패키지명` | 새 패키지 추가 설치 |

---

## 5. 버전 백업 방법

### 작업 완료 후 백업

```powershell
# Windows 탐색기에서:
# 1. app 폴더 선택 → Ctrl+C (복사)
# 2. _backup 폴더로 이동 → Ctrl+V (붙여넣기)
# 3. 붙여넣은 폴더 이름을 app-v1, app-v2 등으로 변경

# 또는 PowerShell에서:
Copy-Item -Path "app" -Destination "_backup\app-v1" -Recurse
```

### 이전 버전 실행

```powershell
# 1. 현재 app을 임시로 이름 변경
Rename-Item -Path "app" -NewName "app-current"

# 2. 실행할 버전을 app으로 변경
Copy-Item -Path "_backup\app-v1" -Destination "app" -Recurse

# 3. 실행
npm run dev

# 4. 확인 끝나면 정리
Remove-Item -Path "app" -Recurse
Rename-Item -Path "app-current" -NewName "app"
```

---

## 6. 문제 해결

### Next.js Dev 모드 아이콘 숨기기

개발 서버 실행 시 화면 좌하단에 Next.js 개발자 도구 아이콘이 표시됩니다.

**숨기는 방법:** `next.config.ts` 파일을 수정하세요.

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  devIndicators: false,
};

export default nextConfig;
```

**Dev 모드는 언제 필요한가?**
- 라우트 정보 확인, 빌드 상태 확인 등 디버깅할 때
- 보통 필요 없으면 꺼두셔도 됩니다
- 배포(production) 환경에서는 자동으로 사라집니다

### deck.gl SSR 오류 발생 시

Next.js는 서버에서 먼저 렌더링하는데, deck.gl은 브라우저에서만 동작합니다.
`OceanMap.tsx`에서 `'use client'`와 동적 import를 사용하여 해결합니다.

### maplibre-gl CSS 누락 시

`globals.css`에 maplibre-gl CSS import가 필요합니다:
```css
@import "maplibre-gl/dist/maplibre-gl.css";
```

### "Need to install the following packages" 메시지

```
Need to install the following packages:
create-next-app@16.1.4
Ok to proceed? (y)
```

이 메시지는 `npx`가 임시로 도구를 다운받아 실행하겠다는 의미입니다.
**`y`를 입력하고 Enter**를 누르면 됩니다. 정상적인 과정입니다.

### src/ 폴더가 없어요

Next.js "recommended defaults"를 선택하면 `src/` 폴더 없이 루트에 `app/` 폴더가 생성됩니다.
**정상입니다.** `app/` 폴더에서 바로 작업하면 됩니다.

---

## 부록: 용어 정리

| 용어 | 설명 |
|------|------|
| **package.json** | 프로젝트 설정 파일. 필요한 라이브러리 목록이 저장됨 |
| **node_modules** | 설치된 라이브러리들이 저장되는 폴더 (수백 MB) |
| **TypeScript** | JavaScript에 타입을 추가한 언어. 오류를 미리 잡아줌 |
| **Tailwind CSS** | CSS를 클래스 이름으로 쉽게 작성하게 해주는 도구 |
| **App Router** | Next.js 14의 새로운 라우팅 방식 |
| **SSR** | Server Side Rendering. 서버에서 먼저 HTML을 만드는 방식 |
| **MapLibre GL** | 무료 오픈소스 지도 라이브러리 (Mapbox GL 대체) |
