CURRENT_CARD = """
    WeatherCard {{
        background-color: {bg};
        border-radius: 15px;
    }}
    QLabel {{ color: white; background: transparent; }}
"""

DEFAULT_CARD = """
    WeatherCard {{
        background-color: {bg};
        border-bottom: 1px solid {border};
        border-radius: {radius};
    }}
    QLabel {{ color: white; background: transparent; border: none; }}
"""

CITY_LABEL = "font-size: 28px; font-weight: bold;"
TIME_LABEL = "font-size: 14px;"
TEMP_LABEL = "font-size: 48px;"
DESC_LABEL = "font-size: 14px;"
MINMAX_LABEL = "font-size: 14px;"

CENTRAL_WIDGET = "background-color: #2E2E2E;"
LEFT_PANEL = """
    QFrame {
        background-color: #6C8281;
        border-right: 1px solid #1A1A1A;
    }
"""
SCROLL_AREA = "background: transparent; border: none;"
CARDS_CONTAINER = "background: transparent;"
RIGHT_PANEL = """
    QFrame {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #87CEFA,
            stop: 1 #FFDF56
        );
        border-radius: 10px;
    }
"""
THEME_BUTTON_SUN = """
    QPushButton {
        background-color: white;
        border-radius: 12px;
        padding-left: 3px;
        padding-right: 31px;
    }
"""
THEME_BUTTON_MOON = """
    QPushButton {
        background-color: white;
        border-radius: 12px;
        padding-left: 31px;
        padding-right: 3px;
    }
"""