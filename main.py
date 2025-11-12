"""
VIGGA - Ana Uygulama
Küçültülmüş boyut, yeni layout: progress bar download butonunun altında, panel %30 küçüldü
"""

import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout, QProgressBar
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from ui_components import *
from video_downloader import VideoDownloadThread, VideoInfoFetcher, get_available_formats, DOWNLOAD_DIR
from styles import MAIN_WINDOW_STYLE, CARD_STYLE, COLORS, RADIUS, PROGRESS_STYLE

class ViggaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.download_thread = None
        self.info_thread = None
        self._drag_pos = None
        self.current_url = ""
        self.current_video_info = None
        self.is_downloading = False
        self.init_window()
        self.init_ui()

    def init_window(self):
        self.setWindowTitle("VIGGA")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(MAIN_WINDOW_STYLE + CARD_STYLE)
        self.setFixedSize(336, 546)
        self.setWindowIcon(QIcon(icon_path('close.svg')))

    def init_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 12, 12, 12)
        outer.setSpacing(0)
        self.card = QWidget()
        self.card.setObjectName('Card')
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(12)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(Qt.black)
        self.card.setGraphicsEffect(shadow)
        self.header = HeaderBar()
        self.header.close_btn.clicked.connect(self.close)
        card_layout.addWidget(self.header)
        url_row = QHBoxLayout()
        url_row.setSpacing(6)
        self.url_input = ModernLineEdit("Paste video URL here")
        self.url_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.url_input.textChanged.connect(self.on_url_changed)
        url_row.addWidget(self.url_input, 1)
        self.spinner = LoadingSpinner()
        self.spinner.setFixedSize(22, 22)
        self.spinner.hide()
        url_row.addWidget(self.spinner, 0)
        url_row.setStretch(0, 1)
        url_row.setStretch(1, 0)
        card_layout.addLayout(url_row)
        self.fetch_bar = QProgressBar()
        self.fetch_bar.setStyleSheet(PROGRESS_STYLE)
        self.fetch_bar.setTextVisible(False)
        self.fetch_bar.setFixedHeight(4)
        self.fetch_bar.hide()
        card_layout.addWidget(self.fetch_bar)
        self.preview = VideoPreviewCard()
        card_layout.addWidget(self.preview)
        format_label = QLabel("Format")
        format_label.setStyleSheet(LABEL_STYLE)
        card_layout.addWidget(format_label)
        self.format_combo = ModernComboBox()
        for fmt in get_available_formats():
            self.format_combo.addItem(fmt)
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        card_layout.addWidget(self.format_combo)
        resolution_label = QLabel("Resolution")
        resolution_label.setStyleSheet(LABEL_STYLE)
        card_layout.addWidget(resolution_label)
        self.resolution_combo = ModernComboBox()
        self.resolution_combo.addItem("Select quality")
        card_layout.addWidget(self.resolution_combo)
        self.download_btn = PrimaryButton("Download")
        self.download_btn.clicked.connect(self.on_download_button_clicked)
        card_layout.addWidget(self.download_btn)
        self.progress_widget = ProgressWidget()
        card_layout.addWidget(self.progress_widget)
        card_layout.addSpacerItem(QSpacerItem(10, 8, QSizePolicy.Minimum, QSizePolicy.Expanding))
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
        if url and len(url) > 10 and url != self.current_url:
            self.current_url = url
            self.status_bar.set_status("Fetching…")
            self.fetch_bar.setRange(0, 0)
            self.fetch_bar.show()
            self.spinner.hide()
            self.info_thread = VideoInfoFetcher(url)
            self.info_thread.info_ready.connect(self.on_info_ready)
            self.info_thread.error.connect(self.on_info_error)
            self.info_thread.start()
    def on_info_ready(self, info):
        self.fetch_bar.hide()
        self.current_video_info = info
        self.preview.set_video_info(info['title'], info['channel'], info['thumbnail'])
        self.update_resolution_options()
        self.status_bar.set_status("Ready")
    def on_info_error(self, error):
        self.fetch_bar.hide()
        self.status_bar.set_status("Error")
        self.current_video_info = None
    def on_format_changed(self, format_text):
        self.update_resolution_options()
    def update_resolution_options(self):
        if not self.current_video_info:
            return
        selected_format = self.format_combo.currentText()
        if selected_format == "Audio Only (MP3)":
            self.resolution_combo.clear()
            self.resolution_combo.addItem("Best Quality")
            self.resolution_combo.set_quality_options([("Best Quality", "bestaudio")])
            self.resolution_combo.setEnabled(True)
        else:
            quality_options = self.current_video_info.get('quality_options', [])
            video_options = [opt for opt in quality_options if 'Audio Only' not in opt[0]]
            self.resolution_combo.set_quality_options(video_options)
            self.resolution_combo.setEnabled(True)
    def _dim_widget(self, w, dim=True):
        if dim:
            eff = QGraphicsOpacityEffect(w)
            eff.setOpacity(0.5)
            w.setGraphicsEffect(eff)
            w.setEnabled(False)
        else:
            w.setGraphicsEffect(None)
            w.setEnabled(True)
    def _set_controls_enabled(self, enabled: bool):
        widgets = [self.url_input, self.format_combo, self.resolution_combo, self.status_bar.delete_btn]
        for w in widgets:
            self._dim_widget(w, dim=not enabled)
    def on_download_button_clicked(self):
        if self.is_downloading:
            self.cancel_download()
        else:
            self.start_download()
    def start_download(self):
        url = self.url_input.text()
        if not url:
            self.status_bar.set_status("Please enter a URL")
            return
        format_id = self.resolution_combo.get_selected_format_id()
        if not format_id:
            self.status_bar.set_status("Select quality")
            return
        selected_format = self.format_combo.currentText()
        self.is_downloading = True
        self.download_btn.setText("Cancel")
        self._set_controls_enabled(False)
        self.status_bar.set_status("Downloading")
        self.progress_widget.reset()
        self.progress_widget.show()
        self.down_thread = VideoDownloadThread(url, format_id, selected_format)
        self.down_thread.progress.connect(self.on_progress)
        self.down_thread.finished.connect(self.on_download_finished)
        self.down_thread.error.connect(self.on_download_error)
        self.down_thread.start()
    def cancel_download(self):
        if self.down_thread and self.down_thread.isRunning():
            self.down_thread.cancel()
            self.status_bar.set_status("Cancelling...")
    def on_progress(self, value, text):
        self.progress_widget.update_progress(value, text)
    def on_download_finished(self, message):
        self.is_downloading = False
        self.download_btn.setText("Download")
        self._set_controls_enabled(True)
        self.status_bar.set_status("Complete")
        self.progress_widget.reset()
    def on_download_error(self, error):
        self.is_downloading = False
        self.download_btn.setText("Download")
        self._set_controls_enabled(True)
        if error == 'Cancelled':
            self.status_bar.set_status("Cancelled")
        else:
            self.status_bar.set_status("Error")
        self.progress_widget.reset()
    def open_folder(self):
        import subprocess
        if sys.platform == 'win32':
            os.startfile(DOWNLOAD_DIR)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', DOWNLOAD_DIR])
        else:
            subprocess.Popen(['xdg-open', DOWNLOAD_DIR])
    def clear_all(self):
        self.url_input.clear()
        self.current_url = ""
        self.current_video_info = None
        self.preview.reset()
        self.resolution_combo.clear()
        self.resolution_combo.addItem("Select quality")
        self.format_combo.setCurrentIndex(0)
        self.progress_widget.reset()
        self.status_bar.set_status("Ready")

def main():
    app = QApplication(sys.argv)
    window = ViggaApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
