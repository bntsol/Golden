#!/bin/bash
# =============================================================================
# BNT Claude Code Skills Installer
#
# Claude Code 스킬 설치 스크립트
# WSL2 환경에서 실행: bash install.sh
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

echo "========================================"
echo " BNT Claude Code Skills Installer"
echo "========================================"
echo ""

# 1. skills 디렉토리 생성
echo "[1/4] skills 디렉토리 확인..."
mkdir -p "$SKILLS_DIR"
echo "      -> $SKILLS_DIR"

# 2. 스킬 복사
echo "[2/4] 스킬 파일 복사..."

if [ -d "$SCRIPT_DIR/bnt-image-extract" ]; then
    cp -r "$SCRIPT_DIR/bnt-image-extract" "$SKILLS_DIR/"
    echo "      -> bnt-image-extract 설치 완료"
else
    echo "      -> [SKIP] bnt-image-extract 폴더를 찾을 수 없음"
fi

if [ -d "$SCRIPT_DIR/bnt-style-extract" ]; then
    cp -r "$SCRIPT_DIR/bnt-style-extract" "$SKILLS_DIR/"
    echo "      -> bnt-style-extract 설치 완료"
else
    echo "      -> [SKIP] bnt-style-extract 폴더를 찾을 수 없음"
fi

# 3. Python 의존성 설치
echo "[3/4] Python 의존성 설치..."
if command -v python3 &> /dev/null; then
    python3 -m pip install Pillow>=10.0.0 --quiet 2>/dev/null && echo "      -> Pillow 설치 완료" || echo "      -> [WARN] Pillow 설치 실패. 수동 설치: python3 -m pip install Pillow"
    python3 -m pip install playwright>=1.40.0 --quiet 2>/dev/null && echo "      -> Playwright 설치 완료" || echo "      -> [WARN] Playwright 설치 실패. 수동 설치: python3 -m pip install playwright"
else
    echo "      -> [WARN] python3을 찾을 수 없음. 수동 설치 필요:"
    echo "         sudo apt install python3 python3-pip"
    echo "         python3 -m pip install Pillow playwright"
fi

# 4. Playwright 브라우저 설치
echo "[4/4] Playwright Chromium 설치..."
if command -v python3 &> /dev/null; then
    python3 -m playwright install chromium --quiet 2>/dev/null && echo "      -> Chromium 설치 완료" || echo "      -> [WARN] Chromium 설치 실패. 수동 설치: python3 -m playwright install chromium"
else
    echo "      -> [SKIP] python3 없음"
fi

echo ""
echo "========================================"
echo " 설치 완료!"
echo "========================================"
echo ""
echo "설치 경로: $SKILLS_DIR/"
echo ""
echo "설치된 스킬:"
ls -d "$SKILLS_DIR"/bnt-* 2>/dev/null | while read dir; do
    echo "  - $(basename "$dir")"
done
echo ""
echo "Claude Code를 재시작하면 스킬이 자동으로 인식됩니다."
