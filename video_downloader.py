"""
VIGGA - Video İndirme Modülü
Hız/ETA ve boyut etiketleri; kalite listesini fps (30/60) ve MB ile zenginleştir
"""

import yt_dlp
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


class VideoDownloadThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, format_id):
        super().__init__()
        self.url = url
        self.format_id = format_id

    def progress_hook(self, d):
        try:
            status = d.get('status')
            downloaded = d.get('downloaded_bytes') or 0
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            speed = d.get('speed') or 0
            if status == 'downloading' and total:
                pct = int(downloaded * 100 / total)
                label = f"Downloading… {_human_bytes(speed)}/s • {_human_bytes(downloaded)}/{_human_bytes(total)}"
                self.progress.emit(pct, label)
            elif status == 'finished':
                self.progress.emit(100, 'Processing…')
        except Exception:
            pass

    def run(self):
        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
                # Seçilen video formatını en iyi sesle birleştir
                'format': f"{self.format_id}+bestaudio/best",
                'merge_output_format': 'mp4',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                self.finished.emit(f"Downloaded: {info.get('title','Video')}")
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
                quality_map = {}
                STD = [144, 240, 360, 480, 720, 1080, 1440, 2160, 4320]
                for f in formats:
                    h = f.get('height')
                    if not h or h not in STD:
                        continue
                    # Muxlu formatı tercih; yoksa yine de video kabul (sonradan +bestaudio ile birleşir)
                    fps = f.get('fps') or 0
                    tbr = f.get('tbr') or 0  # kbps
                    size = f.get('filesize') or f.get('filesize_approx')
                    if not size and duration and tbr:
                        # tahmini boyut
                        size = int((tbr * 1000 / 8) * duration)
                    label_res = '4K' if h == 2160 else ('8K' if h == 4320 else f'{h}p')
                    label = f"{label_res}{_fps_label(fps)}"
                    if size:
                        label += f" {int(size/1024/1024)}MB"
                    key = (h, int(round(fps)), int(tbr))
                    if key not in quality_map:
                        quality_map[key] = (label, f.get('format_id'), fps, tbr)
                    else:
                        if (fps, tbr) > (quality_map[key][2], quality_map[key][3]):
                            quality_map[key] = (label, f.get('format_id'), fps, tbr)
                ordered = sorted(quality_map.values(), key=lambda x: (x[2], x[3], x[0]), reverse=True)
                self.progress_update.emit(100)
                self.info_ready.emit({
                    'title': info.get('title','Unknown'),
                    'channel': info.get('uploader', info.get('channel','Unknown')),
                    'thumbnail': info.get('thumbnail',''),
                    'quality_options': [(lbl, fid) for (lbl, fid, _, _) in ordered],
                })
        except Exception as e:
            self.error.emit(str(e))


def get_available_formats():
    return ["MP4", "WEBM", "MKV", "Audio Only (MP3)"]
