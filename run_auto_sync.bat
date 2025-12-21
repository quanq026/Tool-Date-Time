@echo off
REM Batch file để chạy auto sync với quyền Administrator

cd /d "%~dp0"

echo ============================================================
echo   AUTO TIME SYNC SERVICE
echo   Dang chay voi quyen Administrator...
echo   Nhan Ctrl+C de dung dich vu
echo ============================================================
echo.

python auto_sync.py

pause
