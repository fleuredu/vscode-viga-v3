"""
VIGGA - UI Bileşenleri
Glow/soft stilleri ve tam pastel entegrasyonu ile tamamlanmış.
"""

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolButton,
                             QPushButton, QLabel, QComboBox, QLineEdit, QProgressBar)
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QPainterPath, QFontMetrics
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, pyqtProperty, QRect, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from styles import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, 'assets', 'icons')

def icon_path(name):
    return os.path.join(ICON_DIR, name)

# ... Diğer componentler aynı kalıp sadece style değişti
class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(URL_INPUT_STYLE)
        self.setMinimumHeight(32)

class ModernComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(COMBO_STYLE)
        self.setMinimumHeight(32)
        self.format_ids = []
    def set_quality_options(self, options):
        self.clear()
        self.format_ids = []
        for label, fid in options:
            self.addItem(label)
            self.format_ids.append(fid)
    def get_selected_format_id(self):
        idx = self.currentIndex()
        if 0 <= idx < len(self.format_ids):
            return self.format_ids[idx]
        return None

class CoverLabel(QLabel):
    def __init__(self):
        super().__init__()
        self._pixmap = None
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(162)
        self.setMaximumHeight(162)
        self.setSizePolicy(self.sizePolicy().Expanding, self.sizePolicy().Fixed)
    def set_pixmap(self, pixmap: QPixmap):
        self._pixmap = pixmap
        self._update_scaled()
    def clear_pixmap(self):
        self._pixmap = None
        self.clear()
    def resizeEvent(self, event):
        self._update_scaled()
        super().resizeEvent(event)
    def _update_scaled(self):
        if not self._pixmap or self.width() <= 0 or self.height() <= 0:
            return
        target = QSize(self.width(), self.height())
        scaled = self._pixmap.scaled(target, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.setPixmap(scaled)

class VideoPreviewCard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(PREVIEW_STYLE)
        self.setMinimumHeight(192)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        self.thumbnail_label = CoverLabel()
        self.thumbnail_label.setStyleSheet('background: transparent;')
        layout.addWidget(self.thumbnail_label)
        self.title_label = QLabel('Video preview will appear here')
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_label.setStyleSheet(LABEL_STYLE)
        layout.addWidget(self.title_label)
        self.channel_label = QLabel('')
        self.channel_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.channel_label.setStyleSheet(LABEL_STYLE.replace('font-size: 13px;', 'font-size: 11px;'))
        self.channel_label.setWordWrap(False)
        layout.addWidget(self.channel_label)
        layout.addStretch()
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.on_thumbnail_loaded)
    def set_video_info(self, title, channel, thumbnail_url):
        self._title_full = title or ''
        self._apply_elide()
        self.channel_label.setText(channel or '')
        if thumbnail_url:
            request = QNetworkRequest(QUrl(thumbnail_url))
            self.network_manager.get(request)
    def on_thumbnail_loaded(self, reply):
        if reply.error() == QNetworkReply.NoError:
            pixmap = QPixmap()
            pixmap.loadFromData(reply.readAll())
            self.thumbnail_label.set_pixmap(pixmap)
        reply.deleteLater()
    def resizeEvent(self, event):
        self._apply_elide()
        super().resizeEvent(event)
    def _apply_elide(self):
        fm_title = QFontMetrics(self.title_label.font())
        elided_title = fm_title.elidedText(getattr(self, '_title_full', ''), Qt.ElideRight, max(70, self.width()-24))
        self.title_label.setText(elided_title)
    def reset(self):
        self._title_full = ''
        self.title_label.setText('Video preview will appear here')
        self.channel_label.setText('')
        self.thumbnail_label.clear_pixmap()

class LoadingSpinner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self._angle = 0
        self.animation = QPropertyAnimation(self, b"angle")
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(-1)
        self.animation.setDuration(1000)
    @pyqtProperty(int)
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()
    def start(self):
        self.animation.start()
        self.show()
    def stop(self):
        self.animation.stop()
        self.hide()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(15, 15)
        painter.rotate(self._angle)
        from PyQt5.QtGui import QPen, QColor
        pen = QPen(QColor(COLORS['primary']), 2, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        painter.drawArc(-10, -10, 20, 20, 0, 270 * 16)

class PrimaryButton(QPushButton):
    def __init__(self, text=""):
        super().__init__(text)
        self.setStyleSheet(BUTTON_STYLE)
        self.setMinimumHeight(36)
        self.setCursor(Qt.PointingHandCursor)

class IconButton(QToolButton):
    def __init__(self, name, tooltip=""):
        super().__init__()
        self.setStyleSheet(ICON_BUTTON_STYLE)
        self.setIcon(QIcon(icon_path(name)))
        self.setIconSize(QSize(14, 14))
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)

class ProgressWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        info_layout = QHBoxLayout()
        self.progress_label = QLabel("")
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
        self.setFixedHeight(54)
        self.show()
    def update_progress(self, value, text=""):
        self.progress_bar.setValue(value)
        self.percentage_label.setText(f"{value}%")
        self.progress_label.setText(text)
    def reset(self):
        self.progress_bar.setValue(0)
        self.percentage_label.setText("0%")
        self.progress_label.setText("")

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
