"""
VIGGA - Ana Uygulama
Modern Video İndirici
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui_components import *
from video_downloader import VideoDownloadThread, VideoInfoFetcher, get_available_formats
from styles import MAIN_WINDOW_STYLE, COLORS


class ViggaApp(QWidget):
    """Ana uygulama penceresi"""
    
    def __init__(self):
        super().__init__()
        self.download_thread = None
        self.info_thread = None
        self.init_window()
        self.init_ui()
    
    def init_window(self):
        """Pencere ayarları"""
        self.setWindowTitle("VIGGA")
        self.setFixedSize(420, 720)
        self.setStyleSheet(MAIN_WINDOW_STYLE)
    
    def init_ui(self):
        """Arayüz oluşturma"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)
        
        # Başlık - daha üstte ve küçük
        title = QLabel("VIGGA")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']}; background: transparent;")
        title.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title)
        
        # URL Input
        self.url_input = ModernLineEdit("Paste video URL here")
        self.url_input.textChanged.connect(self.on_url_changed)
        main_layout.addWidget(self.url_input)
        
        # Preview
        self.preview = PreviewWidget()
        main_layout.addWidget(self.preview)
        
        # Format Label + Dropdown
        format_label = QLabel("Format")
        format_label.setStyleSheet(LABEL_STYLE)
        main_layout.addWidget(format_label)
        
        self.format_combo = ModernComboBox()
        for fmt in get_available_formats():
            self.format_combo.addItem(fmt)
        main_layout.addWidget(self.format_combo)
        
        # Resolution Label + Dropdown
        resolution_label = QLabel("Resolution")
        resolution_label.setStyleSheet(LABEL_STYLE)
        main_layout.addWidget(resolution_label)
        
        self.resolution_combo = ModernComboBox()
        self.resolution_combo.addItem("Resolution")
        main_layout.addWidget(self.resolution_combo)
        
        # Progress Widget
        self.progress_widget = ProgressWidget()
        main_layout.addWidget(self.progress_widget)
        
        # Download Button
        self.download_btn = PrimaryButton("Download")
        self.download_btn.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_btn)
        
        # Spacer
        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Status Bar
        self.status_bar = StatusBar()
        self.status_bar.folder_btn.clicked.connect(self.open_folder)
        self.status_bar.delete_btn.clicked.connect(self.clear_all)
        main_layout.addWidget(self.status_bar)
        
        self.setLayout(main_layout)
    
    def on_url_changed(self, url):
        """URL değiştiğinde video bilgilerini çek"""
        if url and len(url) > 10:
            self.status_bar.set_status("Fetching info...")
            self.info_thread = VideoInfoFetcher(url)
            self.info_thread.info_ready.connect(self.on_info_ready)
            self.info_thread.error.connect(self.on_info_error)
            self.info_thread.start()
    
    def on_info_ready(self, info):
        """Video bilgileri hazır"""
        self.preview.setText(f"📹 {info['title']}")
        
        # Çözünürlükleri ekle
        self.resolution_combo.clear()
        for res in info['resolutions']:
            self.resolution_combo.addItem(res)
        
        self.status_bar.set_status("Ready")
    
    def on_info_error(self, error):
        """Video bilgisi hatası"""
        self.status_bar.set_status(f"Error: {error[:30]}")
    
    def start_download(self):
        """İndirme başlat"""
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
        """İndirme ilerlemesi"""
        self.progress_widget.update_progress(value, text)
    
    def on_download_finished(self, message):
        """İndirme tamamlandı"""
        self.status_bar.set_status("Complete")
        self.download_btn.setEnabled(True)
        self.progress_widget.reset()
    
    def on_download_error(self, error):
        """İndirme hatası"""
        self.status_bar.set_status(f"Error")
        self.download_btn.setEnabled(True)
        self.progress_widget.reset()
    
    def open_folder(self):
        """İndirilen dosyaların klasörünü aç"""
        import os
        import subprocess
        path = os.path.abspath(".")
        if sys.platform == 'win32':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
    
    def clear_all(self):
        """Formu temizle"""
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