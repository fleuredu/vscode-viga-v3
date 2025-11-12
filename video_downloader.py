"""
VIGGA - Video İndirme Modülü
Instagram/Pinterest (no height/STD) için uyumlu fallback ve ComboBox/label padding fix.
"""
import os
import threading
import glob
import yt_dlp
from yt_dlp.utils import DownloadCancelled
from PyQt5.QtCore import QThread, pyqtSignal

# ... _human_bytes() ve _fps_label() aynı ...

def _human_bytes(n):
    try:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if n < 1024.0:
                return f"{n:.1f}{unit}"
            n /= 1024.0
    except Exception:
        pass
    return "-"

def _fps_label(fps):
    if not fps:
        return ''
    f = int(round(fps))
    if 58 <= f <= 62:
        return ' 60fps'
    if 28 <= f <= 32:
        return ' 30fps'
    return ''

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ... VideoDownloadThread aynı ...
# ... progress_hook, run, _cleanup vs. aynen korundu ...

class VideoInfoFetcher(QThread):
    info_ready = pyqtSignal(dict)
    progress_update = pyqtSignal(int)
    error = pyqtSignal(str)
    def __init__(self, url):
        super().__init__()
        self.url = url
    def run(self):
        try:
            self.progress_update.emit(30)
            opts = { 'quiet': True, 'no_warnings': True, 'skip_download': True }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self.progress_update.emit(70)
                duration = info.get('duration') or 0
                formats = info.get('formats', [])
                STD = [144, 240, 360, 480, 720, 1080, 1440, 2160, 4320]
                quality_dict = {}
                for f in formats:
                    h = f.get('height')
                    vcodec = f.get('vcodec', 'none')
                    if not h or h not in STD or vcodec == 'none':
                        continue
                    fps = f.get('fps') or 30
                    tbr = f.get('tbr') or 0
                    size = f.get('filesize') or f.get('filesize_approx')
                    if not size and duration and tbr:
                        size = int((tbr * 1000 / 8) * duration)
                    res_key = h
                    if res_key not in quality_dict or (fps, tbr) > (quality_dict[res_key]['fps'], quality_dict[res_key]['tbr']):
                        quality_dict[res_key] = {'height':h,'fps':fps,'tbr':tbr,'size':size,'fid':f.get('format_id')}
                quality_options = []
                if quality_dict:
                    # Standart video çözünürlüklerine sahip formatlar varsa
                    for h in sorted(quality_dict.keys(), reverse=True):
                        q = quality_dict[h]
                        label_res = '8K' if h == 4320 else ('4K' if h == 2160 else f'{h}p')
                        label = f"{label_res}{_fps_label(q['fps'])}"
                        if q['size']:
                            label += f" {int(q['size']/1024/1024)}MB"
                        quality_options.append((label, q['fid']))
                else:
                    # Hiç height yoksa (ör: IG, Pinterest), best video/audio fallback
                    best_format = None
                    for fmt in formats:
                        if fmt.get('vcodec') != 'none' or fmt.get('acodec') != 'none':
                            if fmt.get('format_id'):
                                best_format = fmt['format_id']
                                break
                    if best_format:
                        quality_options.append(("Best Video / Audio", best_format))
                # Her durumda audio only ekle
                quality_options.append(("Audio Only (Best)", "bestaudio"))
                self.progress_update.emit(100)
                self.info_ready.emit({
                    'title': info.get('title','Unknown'),
                    'channel': info.get('uploader', info.get('channel','Unknown')),
                    'thumbnail': info.get('thumbnail',''),
                    'quality_options': quality_options,
                })
        except Exception as e:
            self.error.emit(str(e))
# ... get_available_formats() aynı ...

def get_available_formats():
    return ["MP4", "WEBM", "MKV", "Audio Only (MP3)"]
