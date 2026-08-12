@echo off
setlocal

"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync_repo.ps1"
set "SYNC_EXIT_CODE=%ERRORLEVEL%"

echo.
if not "%SYNC_EXIT_CODE%"=="0" (
    echo Sync ended with exit code %SYNC_EXIT_CODE%.
)
echo Press any key to close this window.
pause >nul

exit /b %SYNC_EXIT_CODE%
