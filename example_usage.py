#!/usr/bin/env python3
"""
Example usage of the GeeksforGeeks HLS Video Downloader

This script demonstrates how to use the GFGDownloader class programmatically
for batch downloads or integration into other applications.
"""

from gfg_hls_downloader import GFGDownloader
import sys

def download_single_video():
    """Example: Download a single video"""
    print("=== Single Video Download Example ===")
    
    # Initialize downloader
    downloader = GFGDownloader()
    
    # Example video URL (replace with actual URL)
    video_url = "https://www.geeksforgeeks.org/your-video-url-here"
    output_filename = "my_video.mp4"
    
    # Download the video
    success = downloader.download_video(video_url, output_filename)
    
    if success:
        print("✅ Video downloaded successfully!")
    else:
        print("❌ Video download failed!")

def download_multiple_videos():
    """Example: Download multiple videos"""
    print("=== Multiple Videos Download Example ===")
    
    # Initialize downloader
    downloader = GFGDownloader()
    
    # List of video URLs to download
    video_urls = [
        "https://www.geeksforgeeks.org/video1-url",
        "https://www.geeksforgeeks.org/video2-url",
        "https://www.geeksforgeeks.org/video3-url"
    ]
    
    # Download each video
    for i, video_url in enumerate(video_urls, 1):
        print(f"\n📹 Downloading video {i}/{len(video_urls)}")
        output_filename = f"video_{i}.mp4"
        
        success = downloader.download_video(video_url, output_filename)
        
        if success:
            print(f"✅ Video {i} downloaded successfully!")
        else:
            print(f"❌ Video {i} download failed!")

def download_with_custom_config():
    """Example: Download with custom configuration"""
    print("=== Custom Configuration Example ===")
    
    # Initialize downloader
    downloader = GFGDownloader()
    
    # Modify configuration
    downloader.config['output_directory'] = 'my_downloads'
    downloader.config['preferred_downloader'] = 'ffmpeg'
    downloader.config['video_quality'] = '720p'
    
    # Save the configuration
    downloader.save_config()
    
    # Download video with custom settings
    video_url = "https://www.geeksforgeeks.org/your-video-url-here"
    success = downloader.download_video(video_url, "custom_video.mp4")
    
    if success:
        print("✅ Video downloaded with custom configuration!")
    else:
        print("❌ Video download failed!")

def extract_video_url_only():
    """Example: Extract video URL without downloading"""
    print("=== Video URL Extraction Example ===")
    
    # Initialize downloader
    downloader = GFGDownloader()
    
    # Login first
    if not downloader.login():
        print("❌ Login failed!")
        return
    
    # Extract video URL from GeeksforGeeks page
    gfg_url = "https://www.geeksforgeeks.org/your-video-page-url"
    video_url = downloader.extract_video_url(gfg_url)
    
    if video_url:
        print(f"✅ Extracted video URL: {video_url}")
    else:
        print("❌ Could not extract video URL!")
    
    # Logout
    downloader.logout()

def main():
    """Main function to run examples"""
    print("🎬 GeeksforGeeks HLS Downloader - Example Usage")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        example_type = sys.argv[1].lower()
        
        if example_type == "single":
            download_single_video()
        elif example_type == "multiple":
            download_multiple_videos()
        elif example_type == "custom":
            download_with_custom_config()
        elif example_type == "extract":
            extract_video_url_only()
        else:
            print("❌ Unknown example type!")
            print("Available examples: single, multiple, custom, extract")
    else:
        print("Available examples:")
        print("1. single   - Download a single video")
        print("2. multiple - Download multiple videos")
        print("3. custom   - Download with custom configuration")
        print("4. extract  - Extract video URL only")
        print("\nUsage: python example_usage.py <example_type>")
        print("Example: python example_usage.py single")

if __name__ == "__main__":
    main()
