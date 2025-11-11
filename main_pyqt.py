
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
import yt_dlp
import logging

# LOGGING
logging.basicConfig(filename='vigga_debug.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s')

def log_terminal(msg):
    print(f"[VIGGA] {msg}")

class ViggaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VIGGA")
        self.setFixedSize(360, 600)
        self.setStyleSheet("background-color: #1C1423; border-radius: 16px;")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.init_ui()
        self.init_glow()
        log_terminal("UI başlatıldı.")
        logging.info("UI başlatıldı.")

    def init_ui(self):
        title = QLabel("VIGGA")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #8F5AFF; margin-bottom: 8px;")
        self.layout.addWidget(title)

        self.preview = QLabel("No preview")
        self.preview.setFixedSize(328, 184)
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setStyleSheet("background-color: #0b0710; color: #a59abc; border-radius: 8px;")
        self.layout.addWidget(self.preview)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com/video")
        self.url_input.setStyleSheet("background-color: #0b0710; color: white; border: none; padding: 12px; border-radius: 8px;")
        self.layout.addWidget(self.url_input)

        self.status = QLabel("Ready")
        self.status.setStyleSheet("color: #a59abc; margin: 4px;")
        self.layout.addWidget(self.status)

        self.format_combo = QComboBox()
        self.format_combo.addItem("Format")
        self.layout.addWidget(self.format_combo)

        self.resolution_combo = QComboBox()
        self.resolution_combo.addItem("Resolution")
        self.layout.addWidget(self.resolution_combo)

        self.download_btn = QPushButton("Download")
        self.download_btn.setStyleSheet("background-color: #8F5AFF; color: white; border-radius: 8px; padding: 12px; font-weight: bold;")
        self.download_btn.clicked.connect(self.download_video)
        self.layout.addWidget(self.download_btn)

        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setStyleSheet("background-color: #220A2E; color: #F0EBFF; border-radius: 8px;")
        self.layout.addWidget(self.log_panel)

    def init_glow(self):
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(30)
        effect.setColor(QColor("#8F5AFF"))
        effect.setOffset(0, 0)
        self.setGraphicsEffect(effect)
        # Animate blurRadius for a smooth breathing glow
        self.anim = QPropertyAnimation(effect, b"blurRadius")
        self.anim.setStartValue(20.0)
        self.anim.setEndValue(40.0)
        self.anim.setDuration(2000)
        self.anim.setLoopCount(-1)
        # Use a smooth easing curve for breathing effect
        self.anim.setEasingCurve(QEasingCurve.InOutSine)
        self.anim.start()

    def download_video(self):
        url = self.url_input.text()
        fmt = self.format_combo.currentText()
        res = self.resolution_combo.currentText()
        self.status.setText("Downloading...")
        log_terminal(f"Download started: {url}, format: {fmt}, resolution: {res}")
        logging.info(f"Download started: {url}, format: {fmt}, resolution: {res}")
        self.log_panel.append(f"Download started: {url}, format: {fmt}, resolution: {res}")
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }
        if fmt != "Format" and res != "Resolution":
            # Çözünürlük stringinden height'ı ayıkla
            import re
            match = re.match(r"(\d+)p", res)
            height = match.group(1) if match else None
            if height:
                ydl_opts['format'] = f"bestvideo[height={height}]+bestaudio/best"
            else:
                ydl_opts['format'] = "bestvideo+bestaudio/best"
        else:
            ydl_opts['format'] = "bestvideo+bestaudio/best"
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Video')
                self.log_panel.append(f"Downloaded: {title}")
                self.status.setText("Download finished.")
                log_terminal("Download finished.")
                logging.info("Download finished.")
        except Exception as e:
            self.status.setText(f"Error: {str(e)}")
            self.log_panel.append(f"Error: {str(e)}")
            log_terminal(f"Error: {str(e)}")
            logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ViggaApp()
    window.show()
    sys.exit(app.exec_())
