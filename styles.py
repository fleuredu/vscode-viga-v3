"""
VIGGA - Stil Tanımlamaları
Modern, glassmorphism tarzı arayüz stilleri
"""

COLORS = {
    'background': '#4A3C5C',
    'surface': '#5C4D6E',
    'surface_light': '#6B5C7F',
    'primary': '#C9A8FF',
    'primary_dark': '#B491FF',
    'text_primary': '#FFFFFF',
    'text_secondary': '#D4C4E8',
    'text_muted': '#9B8AAF',
    'accent': '#E8D4FF',
    'progress': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8B7FFF, stop:1 #C9A8FF)',
    'shadow': 'rgba(0, 0, 0, 0.3)'
}

MAIN_WINDOW_STYLE = f"""
    QWidget {{
        background: {COLORS['background']};
        color: {COLORS['text_primary']};
        font-family: 'Segoe UI', Arial, sans-serif;
    }}
"""

URL_INPUT_STYLE = f"""
    QLineEdit {{
        background: {COLORS['surface']};
        border: 2px solid {COLORS['surface_light']};
        border-radius: 20px;
        padding: 12px 20px;
        color: {COLORS['text_primary']};
        font-size: 13px;
    }}
    QLineEdit:focus {{
        border: 2px solid {COLORS['primary']};
        background: {COLORS['surface_light']};
    }}
"""

PREVIEW_STYLE = f"""
    QLabel {{
        background: {COLORS['surface']};
        border: 2px solid {COLORS['surface_light']};
        border-radius: 16px;
        color: {COLORS['text_muted']};
        font-size: 14px;
    }}
"""

COMBO_STYLE = f"""
    QComboBox {{
        background: {COLORS['surface']};
        border: 2px solid {COLORS['surface_light']};
        border-radius: 20px;
        padding: 10px 20px;
        color: {COLORS['text_primary']};
        font-size: 13px;
    }}
    QComboBox:hover {{
        background: {COLORS['surface_light']};
        border: 2px solid {COLORS['primary']};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {COLORS['text_secondary']};
        margin-right: 10px;
    }}
    QComboBox QAbstractItemView {{
        background: {COLORS['surface']};
        border: 2px solid {COLORS['surface_light']};
        border-radius: 12px;
        selection-background-color: {COLORS['primary']};
        color: {COLORS['text_primary']};
        padding: 5px;
    }}
"""

BUTTON_STYLE = f"""
    QPushButton {{
        background: {COLORS['primary']};
        border: none;
        border-radius: 25px;
        padding: 14px;
        color: white;
        font-size: 15px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background: {COLORS['primary_dark']};
    }}
    QPushButton:pressed {{
        background: {COLORS['primary']};
    }}
"""

ICON_BUTTON_STYLE = f"""
    QPushButton {{
        background: transparent;
        border: none;
        color: {COLORS['text_secondary']};
        padding: 8px;
    }}
    QPushButton:hover {{
        color: {COLORS['text_primary']};
        background: {COLORS['surface_light']};
        border-radius: 8px;
    }}
"""

PROGRESS_STYLE = f"""
    QProgressBar {{
        background: {COLORS['surface']};
        border: none;
        border-radius: 10px;
        height: 10px;
        text-align: center;
    }}
    QProgressBar::chunk {{
        background: {COLORS['progress']};
        border-radius: 10px;
    }}
"""

STATUS_LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_secondary']};
        font-size: 12px;
        background: transparent;
    }}
"""

LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_primary']};
        font-size: 13px;
        font-weight: 500;
        background: transparent;
    }}
"""