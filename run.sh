#!/bin/bash

###############################################################################
# AI 컴플리 실행 스크립트
# AI 기본법 규제 자동 진단 서비스 설정 및 실행
###############################################################################

set -e  # 에러 발생 시 종료

echo "============================================================"
echo "🚀 AI 컴플리 설정 및 실행 스크립트"
echo "============================================================"
echo ""

# 1. Python 버전 확인
echo "[1단계] Python 버전 확인 중..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

# 버전 비교 (간단한 방식)
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "❌ Python 3.11 이상이 필요합니다. (현재: $python_version)"
    exit 1
fi

echo "✓ Python 버전 확인 완료 ($python_version)"
echo ""

# 2. 가상환경 확인 및 생성
echo "[2단계] 가상환경 확인 중..."

if [ ! -d "venv" ]; then
    echo "가상환경이 없습니다. 생성 중..."
    python3 -m venv venv
    echo "✓ 가상환경 생성 완료"
else
    echo "✓ 기존 가상환경 사용"
fi

# 가상환경 활성화
source venv/bin/activate

echo ""

# 3. 패키지 설치
echo "[3단계] 패키지 설치 중..."

pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "✓ 패키지 설치 완료"
echo ""

# 4. Ollama 실행 확인
echo "[4단계] Ollama 확인 중..."

if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama가 실행 중입니다 (http://localhost:11434)"
else
    echo "⚠️  Ollama가 실행되지 않은 것 같습니다."
    echo ""
    echo "Ollama를 시작하려면 다음 명령어를 실행하세요:"
    echo "  Windows: ollama serve"
    echo "  Mac/Linux: ollama serve"
    echo ""
    echo "또는 Ollama 공식 사이트에서 다운로드하세요: https://ollama.ai"
    echo ""
    read -p "계속하시겠습니까? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# 5. .env 파일 확인
echo "[5단계] 환경 설정 파일 확인 중..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ .env.example에서 .env 파일 생성 완료"
        echo "⚠️  .env 파일을 편집하여 API 키를 설정하세요."
    else
        echo "⚠️  .env.example 파일을 찾을 수 없습니다."
    fi
else
    echo "✓ .env 파일 존재 확인"
fi

echo ""

# 6. 애플리케이션 실행
echo "[6단계] 애플리케이션 실행 중..."
echo ""
echo "============================================================"
echo "Streamlit 앱이 시작됩니다."
echo "브라우저에서 http://localhost:8501 을 열어주세요."
echo ""
echo "종료하려면 Ctrl+C를 누르세요."
echo "============================================================"
echo ""

streamlit run app.py

deactivate
