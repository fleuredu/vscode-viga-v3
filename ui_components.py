"""
VIGGA - UI Bileşenleri
Arayüz widget'ları ve bileşenleri
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QComboBox, QLineEdit, QProgressBar, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from styles import *


class ModernLineEdit(QLineEdit):
    """Modern stil URL input alanı"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(URL_INPUT_STYLE)
        self.setMinimumHeight(45)


class ModernComboBox(QComboBox):
    """Modern stil dropdown menü"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet(COMBO_STYLE)
        self.setMinimumHeight(45)


class PreviewWidget(QLabel):
    """Video önizleme alanı"""
    def __init__(self):
        super().__init__()
        self.setText("Video preview will appear here")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(PREVIEW_STYLE)
        self.setMinimumHeight(200)
        self.setMaximumHeight(250)


class PrimaryButton(QPushButton):
    """Ana aksiyon butonu"""
    def __init__(self, text=""):
        super().__init__(text)
        self.setStyleSheet(BUTTON_STYLE)
        self.setMinimumHeight(50)
        self.setCursor(Qt.PointingHandCursor)


class IconButton(QPushButton):
    """İkon butonu (folder, delete vb.)"""
    def __init__(self, icon_text=""):
        super().__init__(icon_text)
        self.setStyleSheet(ICON_BUTTON_STYLE)
        self.setFixedSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)


class ProgressWidget(QWidget):
    """İndirme progress barı"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Progress label ve percentage
        info_layout = QHBoxLayout()
        self.progress_label = QLabel("Downloading...")
        self.progress_label.setStyleSheet(LABEL_STYLE)
        self.percentage_label = QLabel("0%")
        self.percentage_label.setStyleSheet(LABEL_STYLE)
        self.percentage_label.setAlignment(Qt.AlignRight)
        
        info_layout.addWidget(self.progress_label)
        info_layout.addWidget(self.percentage_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(PROGRESS_STYLE)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        
        layout.addLayout(info_layout)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
        self.hide()  # Başlangıçta gizli
    
    def update_progress(self, value, text="Downloading..."):
        """Progress güncelleme"""
        self.progress_bar.setValue(value)
        self.percentage_label.setText(f"{value}%")
        self.progress_label.setText(text)
        if not self.isVisible():
            self.show()
    
    def reset(self):
        """Progress sıfırlama"""
        self.progress_bar.setValue(0)
        self.percentage_label.setText("0%")
        self.hide()


class StatusBar(QWidget):
    """Alt durum çubuğu"""
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Sol taraf - ikonlar
        self.folder_btn = IconButton("📁")
        self.delete_btn = IconButton("🗑️")
        
        # Sağ taraf - durum
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        self.status_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(self.folder_btn)
        layout.addWidget(self.delete_btn)
        layout.addStretch()
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def set_status(self, status):
        """Durum güncelleme"""
        self.status_label.setText(f"Status: {status}")