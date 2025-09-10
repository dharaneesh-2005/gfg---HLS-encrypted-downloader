# 🎬 GeeksforGeeks HLS Video Downloader

A powerful Python script to download encrypted HLS (.m3u8) videos from GeeksforGeeks and other similar educational platforms. This tool supports both direct HLS URLs and GeeksforGeeks page URLs, with automatic video URL extraction and multiple download methods.

## ✨ Features

- 🔐 **Secure Authentication**: Login to GeeksforGeeks with your credentials
- 🎯 **Smart URL Detection**: Automatically detects and extracts video URLs from GeeksforGeeks pages
- 📹 **Multiple Download Methods**: Supports both `yt-dlp` and `ffmpeg` for maximum compatibility
- 📊 **Progress Tracking**: Real-time download progress with beautiful progress bars
- ⚙️ **Configurable**: JSON-based configuration for easy customization
- 🔄 **Fallback Support**: Automatically tries alternative download methods if one fails
- 🛡️ **Error Handling**: Comprehensive error handling and troubleshooting tips
- 📁 **Organized Output**: Automatic file organization in configurable directories

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection
- GeeksforGeeks account (for protected content)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/gfg-hls-downloader.git
   cd gfg-hls-downloader
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install additional tools (recommended):**
   ```bash
   # Install yt-dlp (recommended)
   pip install yt-dlp
   
   # Install ffmpeg (for HLS support)
   # Windows: Download from https://ffmpeg.org/download.html
   # macOS: brew install ffmpeg
   # Ubuntu/Debian: sudo apt install ffmpeg
   ```

### Configuration

1. **Copy the example configuration:**
   ```bash
   cp config.json.example config.json
   ```

2. **Edit `config.json` with your credentials:**
   ```json
   {
       "email": "your_email@example.com",
       "password": "your_password",
       "output_directory": "downloads",
       "preferred_downloader": "yt-dlp",
       "video_quality": "best",
       "custom_headers": {
           "Origin": "https://www.geeksforgeeks.org",
           "Referer": "https://www.geeksforgeeks.org"
       }
   }
   ```

## 📖 Usage

### Basic Usage

Run the script and follow the interactive prompts:

```bash
python gfg_hls_downloader.py
```

The script will:
1. Ask for the video URL (GeeksforGeeks page or direct HLS URL)
2. Ask for output filename (optional)
3. Login to GeeksforGeeks
4. Extract video URL (if needed)
5. Download the video using your preferred method

### Command Line Examples

```bash
# Download from GeeksforGeeks page URL
python gfg_hls_downloader.py

# Use example scripts for batch downloads
python example_usage.py single
python example_usage.py multiple
```

### Programmatic Usage

```python
from gfg_hls_downloader import GFGDownloader

# Initialize downloader
downloader = GFGDownloader()

# Download a single video
success = downloader.download_video(
    "https://www.geeksforgeeks.org/your-video-url",
    "my_video.mp4"
)

if success:
    print("Download completed!")
```

## 🔧 Configuration Options

### config.json Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `email` | Your GeeksforGeeks email | Required | Your email address |
| `password` | Your GeeksforGeeks password | Required | Your password |
| `output_directory` | Download directory | `"downloads"` | Any valid path |
| `preferred_downloader` | Preferred download tool | `"yt-dlp"` | `"yt-dlp"`, `"ffmpeg"` |
| `video_quality` | Video quality preference | `"best"` | `"best"`, `"worst"`, `"720p"`, etc. |
| `custom_headers` | Custom HTTP headers | GeeksforGeeks headers | Any valid headers |

### Download Methods

#### yt-dlp (Recommended)
- ✅ Best compatibility with various video formats
- ✅ Automatic format selection
- ✅ Built-in progress tracking
- ✅ Cookie support

#### ffmpeg
- ✅ Direct HLS stream processing
- ✅ Hardware acceleration support
- ✅ Custom encoding options
- ❌ Requires manual installation

## 🌐 Adapting for Other Sites

This tool can be adapted for other educational platforms by modifying a few key components:

### 1. Authentication URLs
```python
# In gfg_hls_downloader.py, modify these URLs:
LOGOUT_URL = "https://your-site.com/logout"
LOGIN_URL = "https://your-site.com/login"
```

### 2. Login Data Format
```python
# Modify the login data structure in the login() method:
resp = self.session.post(LOGIN_URL, data={
    "username": email,  # Change field names as needed
    "password": password,
    "csrf_token": "your_csrf_token"  # Add required fields
})
```

### 3. Video URL Extraction
```python
# Modify the extract_video_url() method to match your site's HTML structure:
# Update regex patterns to match your site's video URL format
m3u8_pattern = r'your_site_specific_pattern'
```

### 4. Headers and Referrers
```python
# Update custom headers in config.json:
"custom_headers": {
    "Origin": "https://your-site.com",
    "Referer": "https://your-site.com"
}
```

### Example: Adapting for Coursera

```python
# 1. Change URLs
LOGIN_URL = "https://www.coursera.org/api/login"
LOGOUT_URL = "https://www.coursera.org/logout"

# 2. Update login data
resp = self.session.post(LOGIN_URL, data={
    "email": email,
    "password": password,
    "webrequest": True
})

# 3. Update video extraction patterns
coursera_pattern = r'https://[^"\']*coursera[^"\']*\.m3u8[^"\']*'
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Login Failed
- ✅ Check your email and password in `config.json`
- ✅ Verify your GeeksforGeeks account is active
- ✅ Try logging in manually on the website first

#### 2. Video URL Not Found
- ✅ Ensure the URL is a valid GeeksforGeeks video page
- ✅ Check if the video is publicly accessible
- ✅ Try refreshing the page and getting a new URL

#### 3. Download Failed
- ✅ Install both `yt-dlp` and `ffmpeg` for maximum compatibility
- ✅ Check your internet connection
- ✅ Verify the video URL is still valid
- ✅ Try running the script again

#### 4. Permission Errors
- ✅ Ensure you have write permissions to the output directory
- ✅ Check if the file is already open in another application
- ✅ Try running with administrator privileges (if needed)

### Debug Mode

Enable debug mode by setting environment variable:
```bash
export DEBUG=1
python gfg_hls_downloader.py
```

This will save the page content to `debug_page.html` for inspection.

## 📁 Project Structure

```
gfg-hls-downloader/
├── gfg_hls_downloader.py    # Main downloader script
├── example_usage.py         # Example usage scripts
├── requirements.txt         # Python dependencies
├── config.json.example     # Configuration template
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
└── README.md               # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect the terms of service of the websites you use this tool with. The authors are not responsible for any misuse of this software.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Excellent video downloader
- [ffmpeg](https://ffmpeg.org/) - Powerful multimedia framework
- [tqdm](https://github.com/tqdm/tqdm) - Beautiful progress bars
- [requests](https://requests.readthedocs.io/) - HTTP library for Python

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/dharaneesh-2005/gfg---HLS-encrypted-downloader/issues)
3. Create a new issue with detailed information
4. Include error messages and steps to reproduce

---

**Happy Downloading! 🎉**
