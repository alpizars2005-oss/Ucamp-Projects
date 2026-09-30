@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
  py -3 app\server.py --open
) else (
  python app\server.py --open
)
if errorlevel 1 (
  echo.
  echo Se requiere Python 3.11 o posterior. Revisa el error anterior.
  pause
)
