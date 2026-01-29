================================================================
  BNT Claude Code Skills
================================================================

포함된 스킬:
  - bnt-image-extract : 디자인 이미지에서 스타일 추출 -> Tailwind CSS
  - bnt-style-extract : 라이브 웹사이트에서 스타일 추출 -> Tailwind CSS

----------------------------------------------------------------
  설치 방법 (WSL2)
----------------------------------------------------------------

1. 이 폴더를 WSL2에서 접근 가능한 위치에 복사

2. WSL2 터미널에서 install.sh 실행:

   bash /mnt/d/경로/_skills/install.sh

   이 스크립트가 자동으로 수행하는 작업:
   - ~/.claude/skills/ 디렉토리 생성
   - 스킬 파일 복사
   - Python 의존성 설치 (Pillow, Playwright)
   - Playwright Chromium 브라우저 설치

3. Claude Code 재시작

----------------------------------------------------------------
  수동 설치 (install.sh 없이)
----------------------------------------------------------------

1. 스킬 폴더 복사:
   mkdir -p ~/.claude/skills
   cp -r bnt-image-extract ~/.claude/skills/
   cp -r bnt-style-extract ~/.claude/skills/

2. Python 의존성 설치:
   python3 -m pip install Pillow playwright
   python3 -m playwright install chromium

3. Claude Code 재시작

----------------------------------------------------------------
  사전 요구사항
----------------------------------------------------------------

- Claude Code 설치 완료
- WSL2 환경 (Ubuntu 권장)
- Python 3.10+
- pip (python3 -m pip)

----------------------------------------------------------------
  폴더 구조
----------------------------------------------------------------

_skills/
  README.txt              <- 이 파일
  install.sh              <- 자동 설치 스크립트
  bnt-image-extract/      <- 이미지 스타일 추출 스킬
    SKILL.md              <- 스킬 진입점 (Claude가 자동 인식)
    REFERENCE.md          <- Tailwind CSS 매핑 테이블
    PATTERNS.md           <- 컴포넌트 패턴 템플릿
    scripts/              <- Python 스크립트
    templates/            <- TSX 컴포넌트 템플릿
  bnt-style-extract/      <- 웹사이트 스타일 추출 스킬
    SKILL.md
    REFERENCE.md
    PATTERNS.md
    scripts/
    templates/
