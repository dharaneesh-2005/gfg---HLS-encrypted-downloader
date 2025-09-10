#!/bin/bash

echo "Installing GeeksforGeeks HLS Video Downloader..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "Python found. Installing dependencies..."
echo

# Install requirements
pip3 install -r requirements.txt

# Install yt-dlp
echo "Installing yt-dlp..."
pip3 install yt-dlp

echo
echo "Installation completed!"
echo
echo "Next steps:"
echo "1. Copy config.json.example to config.json"
echo "2. Edit config.json with your GeeksforGeeks credentials"
echo "3. Run: python3 gfg_hls_downloader.py"
echo
echo "Note: You may also need to install ffmpeg for HLS support"
echo "Ubuntu/Debian: sudo apt install ffmpeg"
echo "macOS: brew install ffmpeg"
echo "CentOS/RHEL: sudo yum install ffmpeg"
echo
