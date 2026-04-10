@echo off
echo ========================================
echo  Gift Recommendation Agent - CLI
echo ========================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo.
    echo Please create a .env file with your API keys:
    echo   - OPENAI_API_KEY
    echo   - TAVILY_API_KEY
    echo.
    echo See .env.example for reference.
    echo.
    pause
    exit /b 1
)

echo [INFO] Starting Gift Recommendation Agent...
echo.

python run.py %*

if errorlevel 1 (
    echo.
    echo [ERROR] Agent stopped with an error.
    echo Check the logs above for details.
)

pause
