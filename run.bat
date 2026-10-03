```bat
@echo off
cd /d "%~dp0"

echo ===================================================
echo Python Environment Setup
echo ===================================================
echo This script will automatically detect your Python installation,
echo.

:: ===================================================
:: 1. Automatically locate Python
:: ===================================================

set "TARGET_PY="

echo Detecting Python installation...

:: FIX: Use the Windows Python launcher first because it can
:: return the exact Python executable path without user input.
for /f "delims=" %%P in ('py -c "import sys; print(sys.executable)" 2^>nul') do (
    set "TARGET_PY=%%P"
)

:: FIX: Fall back to the Python command if the py launcher
:: is unavailable.
if not defined TARGET_PY (
    for /f "delims=" %%P in ('where python 2^>nul') do (
        if not defined TARGET_PY set "TARGET_PY=%%P"
    )
)

:: ===================================================
:: 2. Verify Python
:: ===================================================

if not defined TARGET_PY (
    echo.
    echo [Error] Python could not be located automatically.
    echo.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure Python is added to PATH.
    pause
    exit /b 1
)

echo Python detected:
echo "%TARGET_PY%"
echo.

echo Verifying Python installation...

"%TARGET_PY%" --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo [Error] The detected Python executable could not be started.
    echo Path:
    echo "%TARGET_PY%"
    echo.
    pause
    exit /b 1
)

echo Python found successfully.

:: ===================================================
:: 3. Check Pygame
:: ===================================================

echo.
echo Checking Pygame...
echo Python:
echo "%TARGET_PY%"
echo.

"%TARGET_PY%" -c "import pygame" >nul 2>&1

if errorlevel 0 (
    echo Pygame is already installed. Skipping download.
) else (
    echo Pygame was not found. Installing now...
    echo.

    "%TARGET_PY%" -m pip install pygame

    if errorlevel 1 (
        echo.
        echo [Error] Pygame installation failed.
        pause
        exit /b 1
    )

    echo.
    echo Pygame installed successfully.
)

:: ===================================================
:: 4. Launch main.py
:: ===================================================

echo.
echo Launching main.py...
echo.

"%TARGET_PY%" "%~dp0main.py"

echo.
echo Program finished.
pause
```
