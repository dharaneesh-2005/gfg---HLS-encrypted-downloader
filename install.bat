@echo off
echo Installing GeeksforGeeks HLS Video Downloader...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
echo.

REM Install requirements
pip install -r requirements.txt

REM Install yt-dlp
echo Installing yt-dlp...
pip install yt-dlp

echo.
echo Installation completed!
echo.
echo Next steps:
echo 1. Copy config.json.example to config.json
echo 2. Edit config.json with your GeeksforGeeks credentials
echo 3. Run: python gfg_hls_downloader.py
echo.
echo Note: You may also need to install ffmpeg for HLS support
echo Download from: https://ffmpeg.org/download.html
echo.
pause
