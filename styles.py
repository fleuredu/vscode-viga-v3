"""
VIGGA - Stil Tanımlamaları
Tüm hatalı/uyumsuz CSS kaldırıldı. Soft mor arka plan, round butonlar, text için okunaklı font ve bold header, spacing optimize. box-shadow ve transition yok, pastel ve kontrastlar uyumlu.
"""

RADIUS = 15
FONT_FAMILY = "Segoe UI, Arial, Helvetica, sans-serif"

COLORS = {
    'background': '#362A42',
    'surface': '#4D3A5D',
    'surface_light': '#65507C',
    'primary': '#C9A8FF',
    'primary_dark': '#B491FF',
    'text_primary': '#F8F6FB',
    'text_secondary': '#E9DEF9',
    'text_muted': '#BCA6D4',
    'accent': '#E8D4FF',
    'progress': 'qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #A185FF, stop:1 #EBCFFF)',
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
        background: {COLORS['surface_light']};
        border: 2px solid {COLORS['primary']};
        border-radius: 13px;
        padding: 10px 15px;
        color: {COLORS['text_primary']};
        font-size: 14px;
    }}
    QLineEdit:focus {{
        border: 2px solid {COLORS['accent']};
        background: {COLORS['surface']};
    }}
"""

PREVIEW_STYLE = f"""
    QLabel {{
        background: {COLORS['surface']};
        border: 2px solid {COLORS['surface_light']};
        border-radius: 12px;
        color: {COLORS['text_muted']};
        font-size: 14px;
    }}
"""

COMBO_STYLE = f"""
    QComboBox {{
        background: {COLORS['surface_light']};
        border: 2px solid {COLORS['primary']};
        border-radius: 13px;
        padding: 8px 16px;
        color: {COLORS['text_primary']};
        font-size: 14px;
    }}
    QComboBox:hover {{
        background: {COLORS['surface']};
        border: 2px solid {COLORS['primary_dark']};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 25px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {COLORS['text_secondary']};
        margin-right: 7px;
    }}
    QComboBox QAbstractItemView {{
        background: {COLORS['surface_light']};
        border: 2px solid {COLORS['primary']};
        border-radius: 9px;
        selection-background-color: {COLORS['accent']};
        color: {COLORS['text_primary']};
        padding: 3px;
    }}
"""

BUTTON_STYLE = f"""
    QPushButton {{
        background: {COLORS['primary']};
        border: none;
        border-radius: 14px;
        padding: 10px;
        color: {COLORS['text_primary']};
        font-size: 15px;
        font-family: {FONT_FAMILY};
        font-weight: 600;
        letter-spacing: 0.2px;
    }}
    QPushButton:hover {{
        background: {COLORS['primary_dark']};
    }}
    QPushButton:pressed {{
        background: {COLORS['accent']};
        color: {COLORS['primary_dark']};
    }}
"""

ICON_BUTTON_STYLE = f"""
    QToolButton {{
        background: transparent;
        border: none;
        color: {COLORS['text_secondary']};
        padding: 4px;
        border-radius: 2px;
    }}
    QToolButton:hover {{
        background: {COLORS['accent']};
        border-radius: 7px;
        color: {COLORS['primary']};
    }}
"""

HEADER_STYLE = f"""
    QWidget#Header {{ background: transparent; }}
    QLabel#Title {{
        color: {COLORS['text_primary']};
        font-size: 18px;
        font-family: {FONT_FAMILY};
        font-weight: 900;
        letter-spacing: 0.2px;
    }}
"""

PROGRESS_STYLE = f"""
    QProgressBar {{
        background: {COLORS['surface_light']};
        border: none;
        border-radius: 8px;
        height: 11px;
        padding: 2px;
        text-align: center;
    }}
    QProgressBar::chunk {{
        background: {COLORS['progress']};
        border-radius: 7px;
        margin: 0px;
    }}
"""

STATUS_LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_secondary']};
        font-size: 12px;
        background: transparent;
        font-family: {FONT_FAMILY};
    }}
"""

LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_primary']};
        font-size: 14px;
        font-weight: 600;
        font-family: {FONT_FAMILY};
        letter-spacing: 0.1px;
        background: transparent;
    }}
"""
