"""
VIGGA - Stil Tanımlamaları
Soft glow, round komponent, pastel/text-shadow ve hover efektleri entegre edildi.
"""

RADIUS = 18
FONT_FAMILY = "Segoe UI, Arial"

COLORS = {
    'background': '#362A42',  # Daha soft, çok koyu olmayan mor
    'surface': '#4D3A5D',
    'surface_light': '#65507C',
    'primary': '#C9A8FF',
    'primary_dark': '#B491FF',
    'text_primary': '#F8F6FB',
    'text_secondary': '#E9DEF9',
    'text_muted': '#BCA6D4',
    'accent': '#E8D4FF',
    'glow': '0 0 16px #C9A8FF77',
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
        box-shadow: {COLORS['glow']};
    }}
"""

URL_INPUT_STYLE = f"""
    QLineEdit {{
        background: {COLORS['surface_light']};
        border: 2px solid {COLORS['primary']};
        border-radius: 15px;
        padding: 9px 16px;
        color: {COLORS['text_primary']};
        font-size: 13px;
        box-shadow: {COLORS['glow']};
        transition: box-shadow 0.3s, border 0.3s;
    }}
    QLineEdit:focus {{
        border: 2px solid {COLORS['accent']};
        background: {COLORS['surface']};
        box-shadow: 0 0 24px #E8D4FF55;
    }}
"""

PREVIEW_STYLE = f"""
    QLabel {{
        background: {COLORS['surface']};
        border: 2px solid {COLORS['surface_light']};
        border-radius: 14px;
        color: {COLORS['text_muted']};
        font-size: 14px;
        box-shadow: {COLORS['glow']};
    }}
"""

COMBO_STYLE = f"""
    QComboBox {{
        background: {COLORS['surface_light']};
        border: 2px solid {COLORS['primary']};
        border-radius: 15px;
        padding: 8px 16px;
        color: {COLORS['text_primary']};
        font-size: 13px;
        box-shadow: {COLORS['glow']};
        transition: box-shadow 0.3s, border 0.25s;
    }}
    QComboBox:hover {{
        background: {COLORS['surface']};
        border: 2px solid {COLORS['primary_dark']};
        box-shadow: 0 0 18px #B491FF55;
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
        border-radius: 10px;
        selection-background-color: {COLORS['accent']};
        color: {COLORS['text_primary']};
        padding: 3px;
        box-shadow: {COLORS['glow']};
    }}
"""

BUTTON_STYLE = f"""
    QPushButton {{
        background: {COLORS['primary']};
        border: none;
        border-radius: 16px;
        padding: 12px;
        color: {COLORS['text_primary']};
        font-size: 15px;
        font-weight: bold;
        box-shadow: {COLORS['glow']};
        text-shadow: 0 1px 4px #fff2, 0 0 8px {COLORS['primary_dark']};
        transition: background 0.16s, box-shadow 0.25s;
    }}
    QPushButton:hover {{
        background: {COLORS['primary_dark']};
        box-shadow: 0 0 24px #C9A8FFF7;
    }}
    QPushButton:pressed {{
        background: {COLORS['accent']};
        color: {COLORS['primary_dark']};
        box-shadow: 0 2px 8px #E8D4FFbb;
    }}
"""

ICON_BUTTON_STYLE = f"""
    QToolButton {{
        background: transparent;
        border: none;
        color: {COLORS['text_secondary']};
        padding: 5px;
        border-radius: 2px;
        box-shadow: none;
    }}
    QToolButton:hover {{
        background: {COLORS['accent']};
        border-radius: 8px;
        color: {COLORS['primary']};
        box-shadow: 0 0 10px #E8D4FF66;
    }}
"""

HEADER_STYLE = f"""
    QWidget#Header {{ background: transparent; }}
    QLabel#Title {{
        color: {COLORS['text_primary']};
        font-size: 17px;
        font-weight: 700;
        text-shadow: 0 1px 6px #fff4, 0 0 22px #B491FF99;
    }}
"""

# Yuvarlak progress bar ve glow
PROGRESS_STYLE = f"""
    QProgressBar {{
        background: {COLORS['surface_light']};
        border: none;
        border-radius: 12px;
        height: 11px;
        padding: 2px;
        text-align: center;
        box-shadow: {COLORS['glow']};
    }}
    QProgressBar::chunk {{
        background: {COLORS['progress']};
        border-radius: 11px;
        margin: 0px;
        box-shadow: 0 0 6px #fff2;
    }}
"""

STATUS_LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_secondary']};
        font-size: 12px;
        background: transparent;
        text-shadow: 0 0 7px #fff9, 0 0 10px #B491FF55;
    }}
"""

LABEL_STYLE = f"""
    QLabel {{
        color: {COLORS['text_primary']};
        font-size: 13px;
        font-weight: 500;
        background: transparent;
        text-shadow: 0 1px 4px #fff3, 0 0 4px #C9A8FF22;
    }}
"""
