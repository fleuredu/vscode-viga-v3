"""
VIGGA - Video İndirme Modülü
yt-dlp ile video indirme fonksiyonları + akıllı kalite seçici
"""

import yt_dlp
from PyQt5.QtCore import QThread, pyqtSignal


class VideoDownloadThread(QThread):
    """Async video indirme thread'i"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, url, format_id):
        super().__init__()
        self.url = url
        self.format_id = format_id
    
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
                'format': self.format_id,
                'merge_output_format': 'mp4',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                title = info.get('title', 'Video')
                self.finished.emit(f"Downloaded: {title}")
        
        except Exception as e:
            error_msg = str(e)
            self.error.emit(error_msg)


class VideoInfoFetcher(QThread):
    """Video bilgilerini async olarak getiren thread"""
    info_ready = pyqtSignal(dict)
    progress_update = pyqtSignal(int)
    error = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
    
    def run(self):
        """Video bilgilerini çek"""
        try:
            self.progress_update.emit(30)
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self.progress_update.emit(70)
                
                # Format filtreleme ve gruplama
                formats = info.get('formats', [])
                quality_map = {}
                
                STANDARD_HEIGHTS = [144, 240, 360, 480, 720, 1080, 1440, 2160, 4320]
                
                for f in formats:
                    if not f.get('height') or f.get('acodec') == 'none':
                        continue
                    
                    height = f['height']
                    if height not in STANDARD_HEIGHTS:
                        continue
                    
                    fps = f.get('fps', 0) or 0
                    filesize = f.get('filesize') or f.get('filesize_approx', 0)
                    tbr = f.get('tbr', 0) or 0
                    format_id = f['format_id']
                    vcodec = f.get('vcodec', '')
                    
                    # 4K/8K etiketleri
                    if height == 2160:
                        label_res = '4K'
                    elif height == 4320:
                        label_res = '8K'
                    else:
                        label_res = f'{height}p'
                    
                    # FPS bilgisi
                    fps_label = f' {int(fps)}fps' if fps >= 50 else ''
                    
                    # Dosya boyutu
                    if filesize > 0:
                        size_mb = filesize / (1024 * 1024)
                        size_label = f' {int(size_mb)}MB'
                    else:
                        size_label = ''
                    
                    quality_label = f'{label_res}{fps_label}{size_label}'.strip()
                    
                    # En iyi formatı seç (fps, bitrate, codec öncelikli)
                    key = (height, fps)
                    if key not in quality_map:
                        quality_map[key] = (quality_label, format_id, fps, tbr)
                    else:
                        existing = quality_map[key]
                        if (fps, tbr) > (existing[2], existing[3]):
                            quality_map[key] = (quality_label, format_id, fps, tbr)
                
                # Sıralama: yüksek kalite üstte
                sorted_formats = sorted(quality_map.values(), key=lambda x: (x[2], x[3]), reverse=True)
                quality_options = [(label, fid) for label, fid, _, _ in sorted_formats]
                
                self.progress_update.emit(100)
                
                self.info_ready.emit({
                    'title': info.get('title', 'Unknown'),
                    'channel': info.get('uploader', info.get('channel', 'Unknown')),
                    'thumbnail': info.get('thumbnail', ''),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'quality_options': quality_options
                })
        
        except Exception as e:
            self.error.emit(str(e))


def get_available_formats():
    """Kullanılabilir format listesi"""
    return ["MP4", "WEBM", "MKV", "Audio Only (MP3)"]