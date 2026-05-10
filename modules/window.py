import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .card import WeatherCard, CityInfoFrame
from . import styles
from .api_request import get_weather, CITY_MAP
from .create_path import create_media_path
from .title_bar import TitleBar


class ImageThemeSwitch(widget.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(52, 24)
        self.setIconSize(core.QSize(18, 18))

        self.SUN_ICON = gui.QIcon(create_media_path("Frame_51.png"))
        self.MOON_ICON = gui.QIcon(create_media_path("Frame_52.png"))

        self.toggled.connect(self.UPDATE_IMAGE)
        self.setChecked(False)
        self.UPDATE_IMAGE(False)

    def UPDATE_IMAGE(self, checked: bool):
        self.setStyleSheet(styles.THEME_BUTTON_SUN if checked else styles.THEME_BUTTON_MOON)
        self.setIcon(self.SUN_ICON if checked else self.MOON_ICON)


class WeatherApp(widget.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle("Погода")
        self.resize(1200, 800)
        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.CENTRAL_WIDGET = widget.QWidget()
        self.CENTRAL_WIDGET.setObjectName("centralWidget")
        self.CENTRAL_WIDGET.setStyleSheet(styles.CENTRAL_WIDGET)
        self.setCentralWidget(self.CENTRAL_WIDGET)
        self.CITY_INFO_FRAME = None
        # ===== ГЛАВНЫЙ ЛЕЙАУТ (вертикальный) =====
        self.MAIN_LAYOUT = widget.QVBoxLayout(self.CENTRAL_WIDGET)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAIN_LAYOUT.setSpacing(0)
        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)

        # ===== TITLE BAR =====
        self.TITLE_BAR = TitleBar(self)
        self.TITLE_BAR.setStyleSheet("background: white; border-top-left-radius: 20px; border-top-right-radius: 20px;")
        self.MAIN_LAYOUT.addWidget(self.TITLE_BAR)

        self.THEME_SWITCH = ImageThemeSwitch()


        
        self.PANELS_LAYOUT = widget.QHBoxLayout()
        self.PANELS_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.PANELS_LAYOUT.setSpacing(0)

        self.MAIN_LAYOUT.addLayout(self.PANELS_LAYOUT)

        # ===== LEFT PANEL =====
        self.LEFT_PANEL = widget.QFrame()
        self.LEFT_PANEL.setFixedWidth(370)
        self.LEFT_PANEL.setStyleSheet(styles.LEFT_PANEL)

        self.LEFT_LAYOUT = widget.QVBoxLayout(self.LEFT_PANEL)
        self.LEFT_LAYOUT.setContentsMargins(20, 20, 20, 0)
        self.LEFT_LAYOUT.setSpacing(10)
        self.LEFT_LAYOUT.addWidget(self.THEME_SWITCH, alignment=core.Qt.AlignmentFlag.AlignRight)
        self.SCROLL_AREA = widget.QScrollArea()
        self.SCROLL_AREA.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL_AREA.setWidgetResizable(True)
        self.SCROLL_AREA.setFrameShape(widget.QFrame.Shape.NoFrame)
        self.SCROLL_AREA.setStyleSheet(styles.SCROLL_AREA)

        self.CARDS_CONTAINER = widget.QWidget()
        self.CARDS_CONTAINER.setStyleSheet(styles.CARDS_CONTAINER)

        self.CARDS_LAYOUT = widget.QVBoxLayout(self.CARDS_CONTAINER)
        self.CARDS_LAYOUT.setContentsMargins(10, 10, 10, 20)
        self.CARDS_LAYOUT.setSpacing(10)

        self.WEATHER_CARDS = []
        self.SELECTED_CARD = None

        for city_ua in CITY_MAP:
            data = get_weather(city_ua)
            card = WeatherCard(
                data["city"],
                data["time"],
                data["temp"],
                data["desc"],
                data["minmax"],
                data["is_current"]
            )
            card.weather_data = data
            card.selected.connect(self.ON_CARD_SELECTED)

            self.WEATHER_CARDS.append(card)
            self.CARDS_LAYOUT.addWidget(card)

        self.CARDS_LAYOUT.addStretch()
        self.SCROLL_AREA.setWidget(self.CARDS_CONTAINER)
        self.LEFT_LAYOUT.addWidget(self.SCROLL_AREA)

        self.UPDATE_TIMER = core.QTimer(self)
        self.UPDATE_TIMER.setInterval(5 * 60 * 1000)
        self.UPDATE_TIMER.timeout.connect(self.REFRESH_WEATHER)
        self.UPDATE_TIMER.start()

   
        self.RIGHT_PANEL = widget.QFrame()
        self.RIGHT_PANEL.setStyleSheet(styles.RIGHT_PANEL)
        self.RIGHT_LAYOUT = widget.QVBoxLayout(self.RIGHT_PANEL)
        self.SEARCH_FRAME = widget.QFrame()
        self.SEARCH_FRAME.setFixedHeight(26)

        self.SEARCH_FRAME.setStyleSheet(styles.SEARCH_FRAME)
        self.SEARCH_LAYOUT = widget.QHBoxLayout(self.SEARCH_FRAME)
        self.SEARCH_LAYOUT.setContentsMargins(20, 20, 20, 0)
        self.PANELS_LAYOUT.addWidget(self.LEFT_PANEL)
        self.PANELS_LAYOUT.addWidget(self.RIGHT_PANEL)
        self.RIGHT_LAYOUT.addWidget(self.SEARCH_FRAME, alignment=core.Qt.AlignmentFlag.AlignTop)

    def REFRESH_WEATHER(self):
        for card in self.WEATHER_CARDS:
            city = card.weather_data.get("city")

            data = get_weather(city)
            if data:
                card.update_data(data)

    def ON_CARD_SELECTED(self, card: WeatherCard):
        if self.SELECTED_CARD and self.SELECTED_CARD != card: self.SELECTED_CARD.set_selected(False)
        card.set_selected(not card.IS_SELECTED)
        self.SELECTED_CARD = card if card.IS_SELECTED else None

        #  удаляем старый фрейм
        if self.CITY_INFO_FRAME:
            self.RIGHT_LAYOUT.removeWidget(self.CITY_INFO_FRAME)
            self.CITY_INFO_FRAME.deleteLater()
            self.CITY_INFO_FRAME = None

        #  создаём новый если карточка выбрана
        if self.SELECTED_CARD:
            self.CITY_INFO_FRAME = CityInfoFrame(self.SELECTED_CARD.weather_data)
            self.RIGHT_LAYOUT.insertWidget(1, self.CITY_INFO_FRAME)


window = WeatherApp()