"""
VIGGA - Ana Uygulama
Frameless & yuvarlatılmış panel, akıllı kalite seçici, loading spinner, iOS tarzı preview
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
        self.resize(480, 780)
        self.setWindowIcon(QIcon(icon_path('close.svg')))

    def init_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(0)

        self.card = QWidget()
        self.card.setObjectName('Card')
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(36)
        shadow.setOffset(0, 8)
        shadow.setColor(Qt.black)
        self.card.setGraphicsEffect(shadow)

        self.header = HeaderBar()
        self.header.close_btn.clicked.connect(self.close)
        card_layout.addWidget(self.header)

        url_row = QHBoxLayout()
        self.url_input = ModernLineEdit("Paste video URL here")
        self.url_input.textChanged.connect(self.on_url_changed)
        url_row.addWidget(self.url_input)
        self.spinner = LoadingSpinner()
        self.spinner.hide()
        url_row.addWidget(self.spinner)
        card_layout.addLayout(url_row)

        self.preview = VideoPreviewCard()
        card_layout.addWidget(self.preview)

        format_label = QLabel("Format")
        format_label.setStyleSheet(LABEL_STYLE)
        card_layout.addWidget(format_label)
        self.format_combo = ModernComboBox()
        for fmt in get_available_formats():
            self.format_combo.addItem(fmt)
        card_layout.addWidget(self.format_combo)

        resolution_label = QLabel("Resolution")
        resolution_label.setStyleSheet(LABEL_STYLE)
        card_layout.addWidget(resolution_label)
        self.resolution_combo = ModernComboBox()
        self.resolution_combo.addItem("Select quality")
        card_layout.addWidget(self.resolution_combo)

        self.progress_widget = ProgressWidget()
        card_layout.addWidget(self.progress_widget)

        self.download_btn = PrimaryButton("Download")
        self.download_btn.clicked.connect(self.start_download)
        card_layout.addWidget(self.download_btn)

        card_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.status_bar = StatusBar()
        self.status_bar.folder_btn.clicked.connect(self.open_folder)
        self.status_bar.delete_btn.clicked.connect(self.clear_all)
        card_layout.addWidget(self.status_bar)

        outer.addWidget(self.card)

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
            self.status_bar.set_status("Fetching...")
            self.spinner.start()
            self.info_thread = VideoInfoFetcher(url)
            self.info_thread.info_ready.connect(self.on_info_ready)
            self.info_thread.progress_update.connect(self.on_fetch_progress)
            self.info_thread.error.connect(self.on_info_error)
            self.info_thread.start()

    def on_fetch_progress(self, percent):
        pass

    def on_info_ready(self, info):
        self.spinner.stop()
        self.preview.set_video_info(info['title'], info['channel'], info['thumbnail'], info.get('description',''))
        self.resolution_combo.set_quality_options(info['quality_options'])
        self.status_bar.set_status("Ready")

    def on_info_error(self, error):
        self.spinner.stop()
        self.status_bar.set_status(f"Error")

    def start_download(self):
        url = self.url_input.text()
        if not url:
            self.status_bar.set_status("Please enter a URL")
            return
        format_id = self.resolution_combo.get_selected_format_id()
        if not format_id:
            self.status_bar.set_status("Select quality")
            return
        self.download_btn.setEnabled(False)
        self.status_bar.set_status("Downloading")
        self.progress_widget.reset()
        self.progress_widget.show()
        self.download_thread = VideoDownloadThread(url, format_id)
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
        self.preview.reset()
        self.resolution_combo.clear()
        self.resolution_combo.addItem("Select quality")
        self.progress_widget.reset()
        self.status_bar.set_status("Ready")


def main():
    app = QApplication(sys.argv)
    window = ViggaApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
