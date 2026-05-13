import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .card import WeatherCard, CityInfoFrame, HourlyForecastFrame, TwelveHourGraphFrame
from . import styles
from .api_request import get_weather, CITY_MAP
from .create_path import create_media_path
from .title_bar import TitleBar


class ImageThemeSwitch(widget.QPushButton):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
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
        
        if checked:
            # print("солнце")
            if self.app:
                self.app.SET_THEME_LIGHT()
        else:
            # print("луна")
            if self.app:
                self.app.SET_THEME_DARK()




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
        self.IS_LIGHT_THEME = False
        # ===== ГЛАВНЫЙ ЛЕЙАУТ (вертикальный) =====
        self.MAIN_LAYOUT = widget.QVBoxLayout(self.CENTRAL_WIDGET)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAIN_LAYOUT.setSpacing(0)
        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)

        # ===== TITLE BAR =====
        self.TITLE_BAR = TitleBar(self)
        self.TITLE_BAR.setStyleSheet("background: white; border-top-left-radius: 20px; border-top-right-radius: 20px;")
        self.MAIN_LAYOUT.addWidget(self.TITLE_BAR)

        self.THEME_SWITCH = ImageThemeSwitch(app=self)


        
        







        
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
        self.RIGHT_LAYOUT.setSpacing(15)
        self.RIGHT_LAYOUT.setContentsMargins(20, 10, 20, 10)

        self.WEATHER_PANEL = widget.QFrame()
        self.WEATHER_PANEL.setFixedSize(788, 157)
        self.WEATHER_PANEL.setStyleSheet("background-color: transparent;")
        self.WEATHER_LAYOUT = widget.QVBoxLayout(self.WEATHER_PANEL)
        self.WEATHER_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.WEATHER_LAYOUT.setSpacing(0)
        self.HOURLY_FRAME = None

        self.BOTTOM_PANEL = widget.QFrame()
        self.BOTTOM_PANEL.setFixedSize(788, 197)
        self.BOTTOM_PANEL.setStyleSheet("background-color: transparent;")
        self.BOTTOM_LAYOUT = widget.QVBoxLayout(self.BOTTOM_PANEL)
        self.BOTTOM_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.BOTTOM_LAYOUT.setSpacing(0)
        self.GRAPH_FRAME = None


        


        self.SEARCH_FRAME = widget.QFrame()
        self.SEARCH_FRAME.setFixedSize(788, 36)
        self.SEARCH_FRAME.setStyleSheet(styles.SEARCH_FRAME)



        # self.CITY_SEARCH = widget.QComboBox(parent = self.SEARCH_FRAME)
        # self.CITY_SEARCH.setFixedSize(261, 36)
        # self.CITY_SEARCH.setEditable(True)
        # self.CITY_SEARCH.setStyleSheet("background-color: rgba(0, 0, 0, 50);")
        # self.CITY_SEARCH.lineEdit().setPlaceholderText("Пошук")
        # # self.CITY_SEARCH.addItems(list(CITY_MAP.keys()))

        

        # self.SEARCH_LAYOUT = widget.QHBoxLayout(self.SEARCH_FRAME)
        # self.SEARCH_LAYOUT.setContentsMargins(0, 0, 0, 0)
        # self.SEARCH_LAYOUT.setSpacing(0)
        
        # self.SETTINGS_LAYOUT = widget.QVBoxLayout(self.SEARCH_FRAME)
        # self.SETTINGS_LAYOUT.setContentsMargins(0, 0, 0, 0)
        # self.SETTINGS_LAYOUT.setSpacing(0)

        # self.SEARCH_FRAME.setLayout(self.SETTINGS_LAYOUT)
        # self.SEARCH_FRAME.setLayout(self.SEARCH_LAYOUT)
        
        # self.SETTINGS_FRAME = widget.QFrame(parent = self.SEARCH_FRAME)
        # self.SETTINGS_FRAME.setFixedSize(150, 45)
        # self.SETTINGS_FRAME.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        # self.SETTINGSL = widget.QHBoxLayout(self.SETTINGS_FRAME)
        # self.SETTINGS_FRAME.setLayout(self.SETTINGSL)

        # self.SETTINGS_NAME = widget.QLabel("Налаштування")
        # self.SETTINGS_NAME.setStyleSheet("background-color: rgba(0, 0, 0, 0); font-size: 14px; font-weight: 500;")
        # self.SETTINGS_NAME.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignTop)


        
        




        # self.SETTINGS = widget.QFrame(parent = self.SETTINGS_FRAME)
        # self.SETTINGS.setFixedSize(45, 45)
        # self.SETTINGS.setStyleSheet("background-color: rgba(0, 0, 0, 50); border-radius: 15px;")

        # self.SETTINGSL.addWidget(self.SETTINGS_NAME, alignment=core.Qt.AlignmentFlag.AlignRight)


        # self.SETT_LABEL = widget.QLabel(self.SETTINGS)
        # self.SETT_LABEL.setFixedSize(45, 45)
        # self.SETT_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        # self.PIXMAP = gui.QPixmap(create_media_path("vector.png"))
        # self.SETT_LABEL.setPixmap(self.PIXMAP)





        # self.SETTINGS_NAME = widget.QLabel("Налаштування")
        # self.SETTINGS_NAME.setStyleSheet("background-color: green")
        # self.SETTINGS_NAME.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignTop)

        # self.SEARCH_LAYOUT.addWidget(self.SETTINGS_FRAME, alignment=core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignTop)

        # # self.SEARCH_LAYOUT.addWidget(self.SETTINGS_NAME, alignment=core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignCenter)
        # self.SEARCH_LAYOUT.addWidget(self.CITY_SEARCH, alignment=core.Qt.AlignmentFlag.AlignRight)
        # self.CITY_SEARCH.activated.connect(self.ON_CARD_SELECTED)

        self.PANELS_LAYOUT.addWidget(self.LEFT_PANEL)
        self.PANELS_LAYOUT.addWidget(self.RIGHT_PANEL)
        self.RIGHT_LAYOUT.addWidget(self.SEARCH_FRAME, alignment=core.Qt.AlignmentFlag.AlignTop)

        # ы
        self.RIGHT_LAYOUT.addStretch()
        self.RIGHT_LAYOUT.addWidget(self.WEATHER_PANEL, alignment=core.Qt.AlignmentFlag.AlignBottom)
        self.RIGHT_LAYOUT.addWidget(self.BOTTOM_PANEL, alignment=core.Qt.AlignmentFlag.AlignBottom)

    def SET_THEME_LIGHT(self):
        """Установить светлую тему (солнце) - жёлтые фреймы"""
        self.IS_LIGHT_THEME = True
        self.CENTRAL_WIDGET.setStyleSheet("""
            background: rgba(255, 255, 200, 1);
        """)
        self.RIGHT_PANEL.setStyleSheet("QFrame { background: rgba(255, 223, 86, 0.3); border: none; }")
        # self.WEATHER_PANEL.setStyleSheet("background-color: rgba(255, 200, 50, 0.5); border-radius: 15px;")
        # self.BOTTOM_PANEL.setStyleSheet("background-color: rgba(255, 200, 50, 0.5); border-radius: 15px;")

    def SET_THEME_DARK(self):
        """Установить тёмную тему (луна) - текущие цвета"""
        self.IS_LIGHT_THEME = False
        self.CENTRAL_WIDGET.setStyleSheet(styles.CENTRAL_WIDGET)
        # self.RIGHT_PANEL.setStyleSheet(styles.RIGHT_PANEL)
        # self.WEATHER_PANEL.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 15px;")
        # self.BOTTOM_PANEL.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 15px;")

    def REFRESH_WEATHER(self):
        for card in self.WEATHER_CARDS:
            city = card.weather_data.get("city")

            data = get_weather(city)
            if data:
                card.update_data(data)

# метод ON_CARD_SELECTED:
    def ON_CARD_SELECTED(self, card: WeatherCard):
        if self.SELECTED_CARD and self.SELECTED_CARD != card: self.SELECTED_CARD.set_selected(False)
        card.set_selected(not card.IS_SELECTED)
        self.SELECTED_CARD = card if card.IS_SELECTED else None

        # Удаляем старый фрейм с информацией о городе
        if self.CITY_INFO_FRAME:
            self.RIGHT_LAYOUT.removeWidget(self.CITY_INFO_FRAME)
            self.CITY_INFO_FRAME.deleteLater()
            self.CITY_INFO_FRAME = None

        # Удаляем старый почасовой фрейм
        if self.HOURLY_FRAME:
            self.WEATHER_LAYOUT.removeWidget(self.HOURLY_FRAME)
            self.HOURLY_FRAME.deleteLater()
            self.HOURLY_FRAME = None

        # Удаляем старый график
        if self.GRAPH_FRAME:
            self.BOTTOM_LAYOUT.removeWidget(self.GRAPH_FRAME)
            self.GRAPH_FRAME.deleteLater()
            self.GRAPH_FRAME = None

        # Создаем новые фреймы если карточка выбрана
        if self.SELECTED_CARD:
            # Информация о городе на правой панели
            self.CITY_INFO_FRAME = CityInfoFrame(self.SELECTED_CARD.weather_data)
            self.RIGHT_LAYOUT.insertWidget(1, self.CITY_INFO_FRAME)

            # Почасовой прогноз на WEATHER_PANEL
            self.HOURLY_FRAME = HourlyForecastFrame(self.SELECTED_CARD.weather_data)
            self.WEATHER_LAYOUT.addWidget(self.HOURLY_FRAME)
            

            # График на BOTTOM_PANEL
            self.GRAPH_FRAME = TwelveHourGraphFrame(self.SELECTED_CARD.weather_data)
            self.BOTTOM_LAYOUT.addWidget(self.GRAPH_FRAME)


window = WeatherApp()