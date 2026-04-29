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
        border-radius: {radius}
    }}
    QLabel {{ color: white; background: transparent; border: none; }}
"""

CITY_LABEL = "font-family: Medium; font-size: 24px; font-weight: 700"
TIME_LABEL = "font-family: Medium; font-size: 12px; font-weight: 500"
TEMP_LABEL = "font-family: Medium; font-size: 44px; font-weight: 500"
DESC_LABEL = "font-family: Medium; font-size: 12px; font-weight: 500"
MINMAX_LABEL = "font-family: Medium; font-size: 12px; font-weight: 500"

CENTRAL_WIDGET =  """
    QFrame {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 rgba(135, 206, 250, 1),
            stop: 1 rgba(255, 223, 86, 1)
        );
       
    }
"""
LEFT_PANEL = """
    QFrame {
        background-color: #6C8281;
    }
"""
SCROLL_AREA = "background: transparent; border: none;"
CARDS_CONTAINER = "background: transparent;"
RIGHT_PANEL = """
    QFrame {
        ;
        
    }
"""
THEME_BUTTON_SUN = """
    QPushButton {
        background-color: rgba(0, 0, 0, 0.2);
        border-radius: 12px;
        padding-left: 3px;
        padding-right: 31px;
    }
"""
THEME_BUTTON_MOON = """
    QPushButton {
        background-color: rgba(236, 236, 236, 1);
        border-radius: 12px;
        padding-left: 31px;
        padding-right: 3px;
    }
"""