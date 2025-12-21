@echo off
REM Batch file để chạy time sync với quyền Administrator

cd /d "%~dp0"

echo ============================================================
echo   WINDOWS TIME SYNCHRONIZATION TOOL
echo   Dang chay voi quyen Administrator...
echo ============================================================
echo.

python time_sync.py

echo.
echo Nhan phim bat ky de dong cua so nay...
pause >nul
