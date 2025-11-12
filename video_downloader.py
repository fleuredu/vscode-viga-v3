"""
VIGGA - Video İndirme Modülü
Cancel desteği, downloads klasörü, resolution deduplikasyonu, audio-only desteği ve format yönetimi
"""

import os
import yt_dlp
import threading
from PyQt5.QtCore import QThread, pyqtSignal


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

class VideoDownloadThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, format_id, download_format='MP4'):
        super().__init__()
        self.url = url
        self.format_id = format_id
        self.download_format = download_format
        self._cancel_event = threading.Event()
        self._current_file = None

    def cancel(self):
        """İndirmeyi iptal et"""
        self._cancel_event.set()

    # yt-dlp progress hook
    def progress_hook(self, d):
        try:
            if self._cancel_event.is_set():
                raise Exception('CANCELLED')
            status = d.get('status')
            self._current_file = d.get('filename', self._current_file)
            downloaded = d.get('downloaded_bytes') or 0
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            speed = d.get('speed') or 0
            if status == 'downloading' and total:
                pct = int(downloaded * 100 / total)
                label = f"Downloading… {_human_bytes(speed)}/s • {_human_bytes(downloaded)}/{_human_bytes(total)}"
                self.progress.emit(pct, label)
            elif status == 'finished':
                self.progress.emit(100, 'Processing…')
        except Exception as e:
            raise e

    def run(self):
        try:
            outtmpl = os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')

            if self.download_format == "Audio Only (MP3)":
                ydl_opts = {
                    'outtmpl': outtmpl,
                    'quiet': True,
                    'no_warnings': True,
                    'progress_hooks': [self.progress_hook],
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
            else:
                merge_format = 'mp4'
                if self.download_format == 'WEBM':
                    merge_format = 'webm'
                elif self.download_format == 'MKV':
                    merge_format = 'mkv'
                ydl_opts = {
                    'outtmpl': outtmpl,
                    'quiet': True,
                    'no_warnings': True,
                    'progress_hooks': [self.progress_hook],
                    'format': f"{self.format_id}+bestaudio/best",
                    'merge_output_format': merge_format,
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(self.url, download=True)
                    if self._cancel_event.is_set():
                        raise Exception('CANCELLED')
                    self.finished.emit(f"Downloaded: {info.get('title','Video')}")
                except Exception as e:
                    if str(e) == 'CANCELLED':
                        # Sil kısmen inmiş dosya
                        if self._current_file and os.path.exists(self._current_file):
                            try:
                                os.remove(self._current_file)
                            except Exception:
                                pass
                        self.error.emit('Cancelled')
                    else:
                        raise
        except Exception as e:
            self.error.emit(str(e))


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
                for h in sorted(quality_dict.keys(), reverse=True):
                    q = quality_dict[h]
                    label_res = '8K' if h == 4320 else ('4K' if h == 2160 else f'{h}p')
                    label = f"{label_res}{_fps_label(q['fps'])}"
                    if q['size']:
                        label += f" {int(q['size']/1024/1024)}MB"
                    quality_options.append((label, q['fid']))
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


def get_available_formats():
    return ["MP4", "WEBM", "MKV", "Audio Only (MP3)"]
