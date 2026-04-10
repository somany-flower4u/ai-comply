@echo off
REM ============================================================
REM AI 컴플리 실행 스크립트 (Windows)
REM AI 기본법 규제 자동 진단 서비스 설정 및 실행
REM ============================================================

setlocal enabledelayedexpansion

cls
echo.
echo ============================================================
echo 🚀 AI 컴플리 설정 및 실행 스크립트
echo ============================================================
echo.

REM 1단계: Python 버전 확인
echo [1단계] Python 버전 확인 중...

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python을 찾을 수 없습니다. Python 3.11 이상을 설치하세요.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✓ Python 버전 확인 완료 (%python_version%)
echo.

REM 2단계: 가상환경 확인 및 생성
echo [2단계] 가상환경 확인 중...

if not exist "venv" (
    echo 가상환경이 없습니다. 생성 중...
    python -m venv venv
    echo ✓ 가상환경 생성 완료
) else (
    echo ✓ 기존 가상환경 사용
)

echo.

REM 3단계: 가상환경 활성화
call venv\Scripts\activate.bat

REM 4단계: 패키지 설치
echo [3단계] 패키지 설치 중...

python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ✓ 패키지 설치 완료
echo.

REM 5단계: Ollama 확인
echo [4단계] Ollama 확인 중...

curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Ollama가 실행 중입니다 (http://localhost:11434)
) else (
    echo.
    echo ⚠️  Ollama가 실행되지 않은 것 같습니다.
    echo.
    echo Ollama를 시작하려면:
    echo   1. 명령 프롬프트에서 'ollama serve' 실행
    echo   2. 또는 https://ollama.ai 에서 Ollama 설치
    echo.
    set /p continue="계속 진행하시겠습니까? (y/n): "
    if /i not "!continue!"=="y" (
        call venv\Scripts\deactivate.bat
        exit /b 1
    )
)

echo.

REM 6단계: .env 파일 확인
echo [5단계] 환경 설정 파일 확인 중...

if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo ✓ .env.example에서 .env 파일 생성 완료
        echo ⚠️  .env 파일을 편집하여 API 키를 설정하세요.
    ) else (
        echo ⚠️  .env.example 파일을 찾을 수 없습니다.
    )
) else (
    echo ✓ .env 파일 존재 확인
)

echo.

REM 7단계: 애플리케이션 실행
echo [6단계] 애플리케이션 실행 중...
echo.
echo ============================================================
echo Streamlit 앱이 시작됩니다.
echo 브라우저에서 http://localhost:8501 을 열어주세요.
echo.
echo 종료하려면 Ctrl+C를 누르세요.
echo ============================================================
echo.

streamlit run app.py

call venv\Scripts\deactivate.bat
pause
