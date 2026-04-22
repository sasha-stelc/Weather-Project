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