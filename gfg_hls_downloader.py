#!/usr/bin/env python3
"""
GeeksforGeeks HLS Video Downloader

A Python script to download encrypted HLS (.m3u8) videos from GeeksforGeeks
and other similar educational platforms. Supports both direct HLS URLs and
GeeksforGeeks page URLs.

Author: Your Name
License: MIT
"""

import requests
import subprocess
import os
import sys
import time
import json
import getpass
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Try to import tqdm for progress bars, install if not available
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("Installing tqdm for better progress bars...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'tqdm'], check=True)
    from tqdm import tqdm
    TQDM_AVAILABLE = True

# Configuration
CONFIG_FILE = 'config.json'
COOKIES_FILE = 'cookies.txt'

# GeeksforGeeks URLs
LOGOUT_URL = "https://auth.geeksforgeeks.org/logout.php"
LOGIN_URL = "https://auth.geeksforgeeks.org/auth.php"

class GFGDownloader:
    """Main class for downloading GeeksforGeeks videos"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            "host": "auth.geeksforgeeks.org"
        }
        self.session.headers.update(self.headers)
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from config.json or create default"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
                return self.create_default_config()
        else:
            return self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration file"""
        default_config = {
            "email": "",
            "password": "",
            "output_directory": "downloads",
            "preferred_downloader": "yt-dlp",  # or "ffmpeg"
            "video_quality": "best",
            "custom_headers": {
                "Origin": "https://www.geeksforgeeks.org",
                "Referer": "https://www.geeksforgeeks.org"
            }
        }
        
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"Created default config file: {CONFIG_FILE}")
            print("Please edit the config file with your credentials.")
        except IOError as e:
            print(f"Error creating config file: {e}")
        
        return default_config
    
    def get_credentials(self):
        """Get credentials from config or prompt user"""
        email = self.config.get('email', '')
        password = self.config.get('password', '')
        
        if not email:
            email = input("Enter your GeeksforGeeks email: ").strip()
            self.config['email'] = email
            self.save_config()
        
        if not password:
            password = getpass.getpass("Enter your GeeksforGeeks password: ")
            self.config['password'] = password
            self.save_config()
        
        return email, password
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def login(self):
        """Login to GeeksforGeeks"""
        try:
            email, password = self.get_credentials()
            
            if not email or not password:
                print("❌ Email and password are required!")
                return False
            
            print("🔐 Logging in to GeeksforGeeks...")
            
            resp = self.session.post(LOGIN_URL, data={
                "reqType": "Login",
                "user": email,
                "pass": password,
                "rem": False,
                "to": "https%3A%2F%2Fauth.geeksforgeeks.org%2F%3Fto%3Dhttps%253A%252F%252Fpractice.geeksforgeeks.org%252Ftransactions",
                "rem": "on",
                "g-recaptcha-response": ""
            }, headers=self.headers)
            
            if resp.status_code == 200:
                print("✅ Login successful!")
                return True
            else:
                print(f"❌ Login failed with status code: {resp.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def logout(self):
        """Logout from GeeksforGeeks"""
        try:
            resp = self.session.get(LOGOUT_URL)
            return resp.status_code == 200
        except Exception as e:
            print(f"Logout error: {e}")
            return False
    
    def extract_video_url(self, gfg_url):
        """Extract video URL from GeeksforGeeks page"""
        try:
            print(f"🔍 Extracting video URL from: {gfg_url}")
            
            # Parse the URL to get the video ID
            parsed_url = urlparse(gfg_url)
            path_parts = parsed_url.path.split('/')
            video_id = path_parts[-1] if path_parts else ""
            
            if video_id:
                print(f"📹 Video ID: {video_id}")
            
            # Set up headers for the video page request
            video_headers = {
                "Origin": "https://www.geeksforgeeks.org",
                "Referer": gfg_url,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            
            # Get the video page to extract the actual video URL
            resp = self.session.get(gfg_url, headers=video_headers)
            
            if resp.status_code != 200:
                print(f"❌ Failed to fetch page: {resp.status_code}")
                return None
            
            content = resp.text
            print(f"📄 Page content length: {len(content)}")
            
            # Try multiple patterns to find video URLs
            import re
            
            # Pattern 1: Direct m3u8 URLs
            m3u8_pattern = r'https://[^"\']*\.m3u8[^"\']*'
            m3u8_matches = re.findall(m3u8_pattern, content)
            
            # Pattern 2: Look for video URLs in JavaScript variables
            js_video_pattern = r'["\']([^"\']*video[^"\']*\.m3u8[^"\']*)["\']'
            js_matches = re.findall(js_video_pattern, content, re.IGNORECASE)
            
            # Pattern 3: Look for video URLs in data attributes or JSON
            json_video_pattern = r'["\']([^"\']*\.m3u8[^"\']*)["\']'
            json_matches = re.findall(json_video_pattern, content)
            
            # Pattern 4: Look for video URLs in src attributes
            src_pattern = r'src=["\']([^"\']*\.m3u8[^"\']*)["\']'
            src_matches = re.findall(src_pattern, content)
            
            # Pattern 5: Look for video URLs in data-src or similar attributes
            data_src_pattern = r'data-[^=]*=["\']([^"\']*\.m3u8[^"\']*)["\']'
            data_src_matches = re.findall(data_src_pattern, content)
            
            # Combine all matches
            all_matches = m3u8_matches + js_matches + json_matches + src_matches + data_src_matches
            
            print(f"🔍 Found {len(all_matches)} potential video URLs")
            
            if all_matches:
                # Return the first valid URL
                for match in all_matches:
                    if match.startswith('http') and '.m3u8' in match:
                        print(f"✅ Found video URL: {match}")
                        return match
                
                # If no http URLs, try to construct one
                for match in all_matches:
                    if '.m3u8' in match:
                        if not match.startswith('http'):
                            if match.startswith('//'):
                                constructed_url = 'https:' + match
                            elif match.startswith('/'):
                                constructed_url = 'https://www.geeksforgeeks.org' + match
                            else:
                                continue
                            print(f"✅ Constructed video URL: {constructed_url}")
                            return constructed_url
            
            # If no m3u8 found, look for other video formats
            mp4_pattern = r'https://[^"\']*\.mp4[^"\']*'
            mp4_matches = re.findall(mp4_pattern, content)
            
            if mp4_matches:
                print(f"✅ Found MP4 URL: {mp4_matches[0]}")
                return mp4_matches[0]
            
            print("❌ No video URLs found in page content")
            return None
            
        except Exception as e:
            print(f"❌ Error extracting video URL: {e}")
            return None
    
    def download_with_ytdlp(self, video_url, output_filename=None):
        """Download video using yt-dlp with progress bar"""
        try:
            print("🚀 Starting download with yt-dlp...")
            
            # Check if yt-dlp is installed
            result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("📦 Installing yt-dlp...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], check=True)
            
            # Create output directory
            output_dir = self.config.get('output_directory', 'downloads')
            Path(output_dir).mkdir(exist_ok=True)
            
            # Prepare yt-dlp command
            cmd = ['yt-dlp']
            
            # Add cookies if available
            if os.path.exists(COOKIES_FILE):
                cmd.extend(['--cookies', COOKIES_FILE])
            
            # Add headers
            custom_headers = self.config.get('custom_headers', {})
            for key, value in custom_headers.items():
                cmd.extend(['--add-header', f'{key}:{value}'])
            
            # Add user agent
            cmd.extend(['--user-agent', self.headers['User-Agent']])
            
            # Add quality and format options
            quality = self.config.get('video_quality', 'best')
            cmd.extend(['-f', quality])
            
            # Add output template
            if output_filename:
                output_path = os.path.join(output_dir, output_filename)
                cmd.extend(['-o', output_path])
            else:
                output_path = os.path.join(output_dir, '%(title)s.%(ext)s')
                cmd.extend(['-o', output_path])
            
            # Add progress and verbose options
            cmd.extend(['--progress', '--newline'])
            
            # Add the video URL
            cmd.append(video_url)
            
            print(f"🔧 Running command: {' '.join(cmd)}")
            
            # Run yt-dlp with real-time output
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     universal_newlines=True, bufsize=1)
            
            # Print output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            # Get the return code
            return_code = process.poll()
            
            if return_code == 0:
                print("✅ Video downloaded successfully with yt-dlp!")
                return True
            else:
                print("❌ Error downloading video with yt-dlp")
                return False
                
        except Exception as e:
            print(f"❌ Error downloading video with yt-dlp: {e}")
            return False
    
    def download_with_ffmpeg(self, m3u8_url, output_filename="video.mp4"):
        """Download HLS video using ffmpeg with progress"""
        try:
            print("🚀 Starting download with ffmpeg...")
            
            # Check if ffmpeg is available
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ ffmpeg not found. Please install ffmpeg first.")
                print("📖 Installation guide: https://ffmpeg.org/download.html")
                return False
            
            # Create output directory
            output_dir = self.config.get('output_directory', 'downloads')
            Path(output_dir).mkdir(exist_ok=True)
            output_path = os.path.join(output_dir, output_filename)
            
            # Prepare ffmpeg command with proper headers and progress
            custom_headers = self.config.get('custom_headers', {})
            header_string = '\r\n'.join([f'{k}: {v}' for k, v in custom_headers.items()])
            
            cmd = [
                'ffmpeg',
                '-headers', header_string,
                '-i', m3u8_url,
                '-c', 'copy',
                '-bsf:a', 'aac_adtstoasc',
                '-progress', 'pipe:1',
                '-y',
                output_path
            ]
            
            print(f"🔧 Running command: {' '.join(cmd)}")
            
            # Run ffmpeg with real-time progress
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                     universal_newlines=True, bufsize=1)
            
            # Print progress in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    if 'out_time_ms=' in line:
                        try:
                            time_part = line.split('out_time_ms=')[1].split()[0]
                            time_ms = int(time_part)
                            time_sec = time_ms / 1000000
                            print(f"⏱️  Progress: {time_sec:.1f}s processed", end='\r')
                        except:
                            pass
                    elif 'progress=' in line:
                        try:
                            progress = line.split('progress=')[1].split()[0]
                            if progress == 'end':
                                print("\n✅ Download completed!")
                            else:
                                print(f"📊 Progress: {progress}", end='\r')
                        except:
                            pass
            
            # Get the return code
            return_code = process.poll()
            
            if return_code == 0:
                print(f"✅ Video downloaded successfully as {output_path}!")
                return True
            else:
                print("❌ Error downloading video with ffmpeg")
                stderr_output = process.stderr.read()
                if stderr_output:
                    print("Error details:")
                    print(stderr_output)
                return False
                
        except Exception as e:
            print(f"❌ Error downloading video with ffmpeg: {e}")
            return False
    
    def validate_video_url(self, video_url):
        """Validate and potentially extract video URL from GeeksforGeeks page"""
        if video_url.endswith('.m3u8'):
            print("✅ Direct HLS video URL detected")
            return video_url
        
        if 'geeksforgeeks.org' in video_url:
            print("🔍 GeeksforGeeks page URL detected, extracting video URL...")
            extracted_url = self.extract_video_url(video_url)
            if extracted_url:
                print(f"✅ Extracted video URL: {extracted_url}")
                return extracted_url
            else:
                print("❌ Could not extract video URL from page")
                return None
        
        print("✅ Using provided URL directly")
        return video_url
    
    def get_user_input(self):
        """Get video URL and filename from user"""
        print("🎬 GeeksforGeeks HLS Video Downloader")
        print("=" * 50)
        
        # Get video URL from user
        while True:
            video_url = input("\n📹 Enter the video URL (HLS .m3u8 or GeeksforGeeks page URL): ").strip()
            
            if not video_url:
                print("❌ Please enter a valid URL!")
                continue
            
            # Validate URL format
            if not (video_url.startswith('http://') or video_url.startswith('https://')):
                print("❌ Please enter a valid URL starting with http:// or https://")
                continue
            
            break
        
        # Get output filename from user
        while True:
            filename = input("\n📁 Enter the output filename (without extension, or press Enter for auto): ").strip()
            
            if not filename:
                filename = None  # Let yt-dlp auto-generate
                break
            
            # Validate filename
            invalid_chars = '<>:"/\\|?*'
            if any(char in filename for char in invalid_chars):
                print(f"❌ Filename contains invalid characters: {invalid_chars}")
                continue
            
            # Add extension if not provided
            if not any(filename.endswith(ext) for ext in ['.mp4', '.mkv', '.webm', '.avi']):
                filename += '.mp4'
            
            break
        
        return video_url, filename
    
    def download_video(self, video_url, output_filename=None):
        """Main download function"""
        try:
            # Show overall progress
            overall_progress = None
            if TQDM_AVAILABLE:
                overall_progress = tqdm(total=100, desc="Download Progress", unit="%", 
                                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
            
            # Login
            if overall_progress:
                overall_progress.update(10)
            
            if not self.login():
                print("❌ Login failed!")
                if overall_progress:
                    overall_progress.close()
                return False
            
            if overall_progress:
                overall_progress.update(20)
            
            # Validate and potentially extract video URL
            final_video_url = self.validate_video_url(video_url)
            if not final_video_url:
                print("❌ Could not get valid video URL!")
                if overall_progress:
                    overall_progress.close()
                return False
            
            print(f"📹 Using video URL: {final_video_url}")
            if overall_progress:
                overall_progress.update(30)
            
            # Try downloading with preferred method
            preferred_downloader = self.config.get('preferred_downloader', 'yt-dlp')
            
            if preferred_downloader == 'yt-dlp':
                if overall_progress:
                    overall_progress.set_description("Downloading with yt-dlp")
                    overall_progress.update(40)
                
                success = self.download_with_ytdlp(final_video_url, output_filename)
                
                if not success:
                    print("❌ yt-dlp failed, trying ffmpeg...")
                    if overall_progress:
                        overall_progress.set_description("Trying ffmpeg")
                        overall_progress.update(60)
                    
                    success = self.download_with_ffmpeg(final_video_url, output_filename or "video.mp4")
            else:
                if overall_progress:
                    overall_progress.set_description("Downloading with ffmpeg")
                    overall_progress.update(40)
                
                success = self.download_with_ffmpeg(final_video_url, output_filename or "video.mp4")
                
                if not success:
                    print("❌ ffmpeg failed, trying yt-dlp...")
                    if overall_progress:
                        overall_progress.set_description("Trying yt-dlp")
                        overall_progress.update(60)
                    
                    success = self.download_with_ytdlp(final_video_url, output_filename)
            
            if success:
                print("✅ Download completed successfully!")
                if overall_progress:
                    overall_progress.update(100)
                    overall_progress.set_description("Download Complete")
            else:
                print("❌ All download methods failed!")
                print("\n🔧 Troubleshooting tips:")
                print("1. Make sure you have access to the video content")
                print("2. Check if the video URL is still valid")
                print("3. Try running the script again")
                print("4. Install ffmpeg if you haven't already")
                if overall_progress:
                    overall_progress.set_description("Download Failed")
            
            # Logout
            print("\n🚪 Logging out...")
            self.logout()
            print("✅ Logged out successfully!")
            
            if overall_progress:
                overall_progress.close()
            
            return success
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Download cancelled by user")
            if overall_progress:
                overall_progress.close()
            return False
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            if overall_progress:
                overall_progress.close()
            return False

def main():
    """Main function"""
    try:
        downloader = GFGDownloader()
        
        # Get user input
        video_url, output_filename = downloader.get_user_input()
        
        # Download video
        success = downloader.download_video(video_url, output_filename)
        
        if success:
            print("\n🎉 Process completed successfully!")
        else:
            print("\n❌ Process failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
