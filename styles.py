"""
VIGGA - Stil Tanımlamaları
Progress bar: yuvarlatılmış köşeler ve ince fetch bar desteği
"""

RADIUS = 20
FONT_FAMILY = "Segoe UI, Arial"

COLORS = {
    'background': '#3F3350',
    'surface': '#524364',
    'surface_light': '#615274',
    'primary': '#C9A8FF',
    'primary_dark': '#B491FF',
    'text_primary': '#FFFFFF',
    'text_secondary': '#E4DAF3',
    'text_muted': '#B9AACD',
    'accent': '#E8D4FF',
    'progress': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8B7FFF, stop:1 #C9A8FF)',
}

MAIN_WINDOW_STYLE = f"""
    QWidget {{
        background: transparent;
        color: {COLORS['text_primary']};
        font-family: {FONT_FAMILY};
    }}
"""

CARD_STYLE = f"""
    QWidget#Card {{
        background: {COLORS['background']};
        border-radius: {RADIUS}px;
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
"""

ICON_BUTTON_STYLE = f"""
    QToolButton {{
        background: transparent;
        border: none;
        color: {COLORS['text_secondary']};
        padding: 6px;
    }}
    QToolButton:hover {{
        background: {COLORS['surface_light']};
        border-radius: 8px;
        color: {COLORS['text_primary']};
    }}
"""

HEADER_STYLE = f"""
    QWidget#Header {{ background: transparent; }}
    QLabel#Title {{ color: {COLORS['text_primary']}; font-size: 16px; font-weight: 700; }}
"""

# Yuvarlak progress bar
PROGRESS_STYLE = f"""
    QProgressBar {{
        background: {COLORS['surface']};
        border: none;
        border-radius: 12px;
        height: 10px;
        padding: 2px; /* chunk'ın yuvarlak görünmesi için iç boşluk */
        text-align: center;
    }}
    QProgressBar::chunk {{
        background: {COLORS['progress']};
        border-radius: 10px; /* bar radius - padding kadar küçük */
        margin: 0px; /* kesintisiz şerit */
    }}
"""

STATUS_LABEL_STYLE = f"""
    QLabel {{ color: {COLORS['text_secondary']}; font-size: 12px; background: transparent; }}
"""

LABEL_STYLE = f"""
    QLabel {{ color: {COLORS['text_primary']}; font-size: 13px; font-weight: 500; background: transparent; }}
"""