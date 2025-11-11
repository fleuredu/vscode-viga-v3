"""
VIGGA - Video İndirme Modülü
yt-dlp ile video indirme fonksiyonları
"""

import yt_dlp
from PyQt5.QtCore import QThread, pyqtSignal


class VideoDownloadThread(QThread):
    """Async video indirme thread'i"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, url, format_type, resolution):
        super().__init__()
        self.url = url
        self.format_type = format_type
        self.resolution = resolution
    
    def progress_hook(self, d):
        """İndirme ilerlemesi callback'i"""
        if d['status'] == 'downloading':
            try:
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                if total > 0:
                    percentage = int((downloaded / total) * 100)
                    self.progress.emit(percentage, "Downloading...")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress.emit(100, "Processing...")
    
    def run(self):
        """Thread çalıştırma"""
        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
            }
            
            # Format ve çözünürlük ayarları
            if self.resolution and self.resolution != "Resolution":
                import re
                match = re.match(r"(\d+)p", self.resolution)
                height = match.group(1) if match else None
                if height:
                    ydl_opts['format'] = f"bestvideo[height={height}]+bestaudio/best"
                else:
                    ydl_opts['format'] = "bestvideo+bestaudio/best"
            else:
                ydl_opts['format'] = "bestvideo+bestaudio/best"
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                title = info.get('title', 'Video')
                self.finished.emit(f"Downloaded: {title}")
                print(f"Download completed: {title}")
        
        except Exception as e:
            error_msg = str(e)
            self.error.emit(error_msg)
            print(f"Download error: {error_msg}")


class VideoInfoFetcher(QThread):
    """Video bilgilerini async olarak getiren thread"""
    info_ready = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
    
    def run(self):
        """Video bilgilerini çek"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                
                # Format listesi
                formats = info.get('formats', [])
                resolutions = set()
                
                for f in formats:
                    if f.get('height'):
                        resolutions.add(f"{f['height']}p")
                
                self.info_ready.emit({
                    'title': info.get('title', 'Unknown'),
                    'thumbnail': info.get('thumbnail', ''),
                    'duration': info.get('duration', 0),
                    'resolutions': sorted(list(resolutions), reverse=True)
                })
        
        except Exception as e:
            self.error.emit(str(e))


def get_available_formats():
    """Kullanılabilir format listesi"""
    return ["MP4", "WEBM", "MKV", "Audio Only (MP3)"]