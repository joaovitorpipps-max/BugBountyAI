@echo off
REM Quick setup script untuk BugBountyAI v2 (Windows)

echo =====================================================
echo    BugBountyAI v2 - Quick Setup Script (Windows)
echo =====================================================
echo.

echo Checking Python version...
python --version
echo.

echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Upgrading pip...
python -m pip install --upgrade pip -q
echo pip upgraded
echo.

echo Installing dependencies...
echo Note: Using minimal requirements for Python 3.14 compatibility
pip install -r requirements-minimal.txt -q
echo Dependencies installed
echo.

echo Setting up configuration...
if not exist ".env.gemini" (
    copy .env.gemini.example .env.gemini
    echo .env.gemini created
    echo Please edit .env.gemini and add your Gemini API Key
) else (
    echo .env.gemini already exists
)
echo.

echo =====================================================
echo    Setup Complete!
echo =====================================================
echo.
echo Next Steps:
echo   1. Edit .env.gemini and add your Gemini API Key
echo   2. Test basic scan: python -m bugbountyai.cli.main scan https://example.com
echo   3. Test with Gemini AI: python -m bugbountyai.cli.gemini_cli scan-gemini https://example.com --gemini-key YOUR_KEY
echo.
pause
