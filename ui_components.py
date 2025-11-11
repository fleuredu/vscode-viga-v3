"""
VIGGA - UI Bileşenleri
Arayüz widget'ları ve bileşenleri (ikonlu, header'lı)
"""

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolButton,
                             QPushButton, QLabel, QComboBox, QLineEdit, QProgressBar)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from styles import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, 'assets', 'icons')

def icon_path(name):
    return os.path.join(ICON_DIR, name)

class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(URL_INPUT_STYLE)
        self.setMinimumHeight(45)

class ModernComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(COMBO_STYLE)
        self.setMinimumHeight(45)

class PreviewWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("Video preview will appear here")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(PREVIEW_STYLE)
        self.setMinimumHeight(200)
        self.setMaximumHeight(250)

class PrimaryButton(QPushButton):
    def __init__(self, text=""):
        super().__init__(text)
        self.setStyleSheet(BUTTON_STYLE)
        self.setMinimumHeight(50)
        self.setCursor(Qt.PointingHandCursor)

class IconButton(QToolButton):
    def __init__(self, name, tooltip=""):
        super().__init__()
        self.setStyleSheet(ICON_BUTTON_STYLE)
        self.setIcon(QIcon(icon_path(name)))
        self.setIconSize(QSize(18, 18))
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)

class ProgressWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        info_layout = QHBoxLayout()
        self.progress_label = QLabel("Downloading...")
        self.progress_label.setStyleSheet(LABEL_STYLE)
        self.percentage_label = QLabel("0%")
        self.percentage_label.setStyleSheet(LABEL_STYLE)
        self.percentage_label.setAlignment(Qt.AlignRight)
        info_layout.addWidget(self.progress_label)
        info_layout.addWidget(self.percentage_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(PROGRESS_STYLE)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addLayout(info_layout)
        layout.addWidget(self.progress_bar)
        self.hide()
    def update_progress(self, value, text="Downloading..."):
        self.progress_bar.setValue(value)
        self.percentage_label.setText(f"{value}%")
        self.progress_label.setText(text)
        if not self.isVisible():
            self.show()
    def reset(self):
        self.progress_bar.setValue(0)
        self.percentage_label.setText("0%")
        self.hide()

class StatusBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.folder_btn = IconButton('folder.svg', 'Open downloads folder')
        self.delete_btn = IconButton('trash.svg', 'Clear')
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet(STATUS_LABEL_STYLE)
        self.status_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.folder_btn)
        layout.addWidget(self.delete_btn)
        layout.addStretch()
        layout.addWidget(self.status_label)
    def set_status(self, status):
        self.status_label.setText(f"Status: {status}")

class HeaderBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('Header')
        self.setStyleSheet(HEADER_STYLE)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel("VIGGA")
        self.title.setObjectName('Title')
        layout.addWidget(self.title)
        layout.addStretch()
        self.close_btn = IconButton('close.svg', 'Close')
        layout.addWidget(self.close_btn)
