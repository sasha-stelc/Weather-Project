import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .card import WeatherCard
from . import styles
from .api_request import get_weather, CITY_MAP
from .create_path import create_media_path


class ImageThemeSwitch(widget.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(52, 24)
        self.setIconSize(core.QSize(18, 18))
        self.SUN_ICON = gui.QIcon(create_media_path("Frame_51.png"))
        self.MOON_ICON = gui.QIcon(create_media_path("Frame_52.png"))
        self.toggled.connect(self.update_image)
        self.setChecked(False)
        self.update_image(False)

    def update_image(self, checked: bool):
        self.setStyleSheet(styles.THEME_BUTTON_SUN if checked else styles.THEME_BUTTON_MOON)
        self.setIcon(self.SUN_ICON if checked else self.MOON_ICON)

class WeatherApp(widget.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Погода")
        self.resize(1200, 800)

        central_widget = widget.QWidget()
        central_widget.setStyleSheet(styles.CENTRAL_WIDGET)
        self.setCentralWidget(central_widget)

        main_layout = widget.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        left_panel = widget.QFrame()
        left_panel.setFixedWidth(370)
        left_panel.setStyleSheet(styles.LEFT_PANEL)

        left_layout = widget.QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 0)
        left_layout.setSpacing(10)

        top_bar = widget.QFrame(left_panel)
        top_bar.setFixedSize(core.QSize(330, 44))
        top_bar_layout = widget.QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        top_bar_layout.addWidget(ImageThemeSwitch(), alignment=core.Qt.AlignmentFlag.AlignRight)
        left_layout.addWidget(top_bar)

        scroll_area = widget.QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(widget.QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet(styles.SCROLL_AREA)

        cards_container = widget.QWidget()
        cards_container.setStyleSheet(styles.CARDS_CONTAINER)

        self.CARDS_LAYOUT = widget.QVBoxLayout(cards_container)
        self.CARDS_LAYOUT.setContentsMargins(10, 10, 10, 20)
        self.CARDS_LAYOUT.setSpacing(10)

        self.WEATHER_CARDS = []
        self.SELECTED_CARD = None

        for city_ua in CITY_MAP:
            data = get_weather(city_ua) 
            card = WeatherCard(data["city"], data["time"], data["temp"], data["desc"], data["minmax"], data["is_current"])
            card.weather_data = data
            card.selected.connect(self.on_card_selected)
            self.WEATHER_CARDS.append(card)
            self.CARDS_LAYOUT.addWidget(card)

        self.CARDS_LAYOUT.addStretch()
        scroll_area.setWidget(cards_container)
        left_layout.addWidget(scroll_area)

        right_panel = widget.QFrame()
        right_panel.setStyleSheet(styles.RIGHT_PANEL)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

    def on_card_selected(self, card: WeatherCard):
        if self.SELECTED_CARD and self.SELECTED_CARD != card: self.SELECTED_CARD.set_selected(False)
        card.set_selected(not card.IS_SELECTED)
        self.SELECTED_CARD = card if card.IS_SELECTED else None



window = WeatherApp()