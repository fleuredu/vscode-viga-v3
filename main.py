"""
VIGGA - Ana Uygulama
Frameless & yuvarlatılmış panel, ikonlu başlık ve status bar
"""

import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from ui_components import *
from video_downloader import VideoDownloadThread, VideoInfoFetcher, get_available_formats
from styles import MAIN_WINDOW_STYLE, CARD_STYLE, COLORS, RADIUS

class ViggaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.download_thread = None
        self.info_thread = None
        self._drag_pos = None
        self.init_window()
        self.init_ui()

    def init_window(self):
        self.setWindowTitle("VIGGA")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(MAIN_WINDOW_STYLE + CARD_STYLE)
        self.resize(460, 760)
        self.setWindowIcon(QIcon(icon_path('close.svg')))

    def init_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(0)

        # Card container
        self.card = QWidget()
        self.card.setObjectName('Card')
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)

        # Shadow glow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 8)
        shadow.setColor(Qt.black)
        self.card.setGraphicsEffect(shadow)

        # Header bar
        self.header = HeaderBar()
        self.header.close_btn.clicked.connect(self.close)
        card_layout.addWidget(self.header)

        # URL Input
        self.url_input = ModernLineEdit("Paste video URL here")
        self.url_input.textChanged.connect(self.on_url_changed)
        card_layout.addWidget(self.url_input)

        # Preview
        self.preview = PreviewWidget()
        card_layout.addWidget(self.preview)

        # Format
        format_label = QLabel("Format")
        format_label.setStyleSheet(LABEL_STYLE)
        card_layout.addWidget(format_label)
        self.format_combo = ModernComboBox()
        for fmt in get_available_formats():
            self.format_combo.addItem(fmt)
        card_layout.addWidget(self.format_combo)

        # Resolution
        resolution_label = QLabel("Resolution")
        resolution_label.setStyleSheet(LABEL_STYLE)
        card_layout.addWidget(resolution_label)
        self.resolution_combo = ModernComboBox()
        self.resolution_combo.addItem("Resolution")
        card_layout.addWidget(self.resolution_combo)

        # Progress
        self.progress_widget = ProgressWidget()
        card_layout.addWidget(self.progress_widget)

        # Download Button
        self.download_btn = PrimaryButton("Download")
        self.download_btn.clicked.connect(self.start_download)
        card_layout.addWidget(self.download_btn)

        # Spacer & StatusBar
        card_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.status_bar = StatusBar()
        self.status_bar.folder_btn.clicked.connect(self.open_folder)
        self.status_bar.delete_btn.clicked.connect(self.clear_all)
        card_layout.addWidget(self.status_bar)

        outer.addWidget(self.card)

    # Window drag for frameless
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()
    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def on_url_changed(self, url):
        if url and len(url) > 10:
            self.status_bar.set_status("Fetching info...")
            self.info_thread = VideoInfoFetcher(url)
            self.info_thread.info_ready.connect(self.on_info_ready)
            self.info_thread.error.connect(self.on_info_error)
            self.info_thread.start()

    def on_info_ready(self, info):
        self.preview.setText(f"📹 {info['title']}")
        self.resolution_combo.clear()
        for res in info['resolutions']:
            self.resolution_combo.addItem(res)
        self.status_bar.set_status("Ready")

    def on_info_error(self, error):
        self.status_bar.set_status(f"Error: {error[:30]}")

    def start_download(self):
        url = self.url_input.text()
        if not url:
            self.status_bar.set_status("Please enter a URL")
            return
        fmt = self.format_combo.currentText()
        res = self.resolution_combo.currentText()
        self.download_btn.setEnabled(False)
        self.status_bar.set_status("Downloading")
        self.progress_widget.reset()
        self.progress_widget.show()
        self.download_thread = VideoDownloadThread(url, fmt, res)
        self.download_thread.progress.connect(self.on_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.error.connect(self.on_download_error)
        self.download_thread.start()

    def on_progress(self, value, text):
        self.progress_widget.update_progress(value, text)
    def on_download_finished(self, message):
        self.status_bar.set_status("Complete")
        self.download_btn.setEnabled(True)
        self.progress_widget.reset()
    def on_download_error(self, error):
        self.status_bar.set_status("Error")
        self.download_btn.setEnabled(True)
        self.progress_widget.reset()

    def open_folder(self):
        import subprocess
        path = os.path.abspath(".")
        if sys.platform == 'win32':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])

    def clear_all(self):
        self.url_input.clear()
        self.preview.setText("Video preview will appear here")
        self.resolution_combo.clear()
        self.resolution_combo.addItem("Resolution")
        self.progress_widget.reset()
        self.status_bar.set_status("Ready")


def main():
    app = QApplication(sys.argv)
    window = ViggaApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
