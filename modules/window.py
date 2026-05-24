import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .card import WeatherCard, CityInfoFrame, HourlyForecastFrame, TwelveHourGraphFrame
from . import styles
from .api_request import get_weather, SEARCH_CITIES, FORMAT_CITY, LOAD_USER_CITIES, ADD_USER_CITY, REMOVE_USER_CITY
from .create_path import create_media_path
from .title_bar import TitleBar
from .settings import Settings

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
            if self.app:
                self.app.SET_THEME_LIGHT()
        else:
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
        self._SELECTED_CITY = None
        self.SETTINGS_WINDOW = Settings(self.CENTRAL_WIDGET)
        self.SETTINGS_WINDOW.setGeometry(0, 26, 1200, 800)
        self.SETTINGS_WINDOW.hide()
        self.SETTINGS_WINDOW.raise_()
        self.MAIN_LAYOUT = widget.QVBoxLayout(self.CENTRAL_WIDGET)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAIN_LAYOUT.setSpacing(0)
        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        self.TITLE_BAR = TitleBar(self)
        self.TITLE_BAR.setStyleSheet(styles.TITLE_BAR)
        self.MAIN_LAYOUT.addWidget(self.TITLE_BAR, alignment=core.Qt.AlignmentFlag.AlignLeft)
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

        for city_en in LOAD_USER_CITIES():
            data = get_weather(city_en)
            if not data:
                continue
            card = WeatherCard(
                data.get("city_display", data["city"]),
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

        # ===== RIGHT PANEL =====
        self.RIGHT_PANEL = widget.QFrame()
        self.RIGHT_PANEL.setStyleSheet(styles.RIGHT_PANEL)
        self.RIGHT_LAYOUT = widget.QVBoxLayout(self.RIGHT_PANEL)
        self.RIGHT_LAYOUT.setSpacing(15)
        self.RIGHT_LAYOUT.setContentsMargins(20, 10, 20, 10)
        self.WEATHER_PANEL = widget.QFrame()
        self.WEATHER_PANEL.setFixedSize(788, 157)
        self.WEATHER_PANEL.setStyleSheet(styles.TRANSPARENT_BG)
        self.WEATHER_LAYOUT = widget.QVBoxLayout(self.WEATHER_PANEL)
        self.WEATHER_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.WEATHER_LAYOUT.setSpacing(0)
        self.HOURLY_FRAME = None
        self.BOTTOM_PANEL = widget.QFrame()
        self.BOTTOM_PANEL.setFixedSize(788, 197)
        self.BOTTOM_PANEL.setStyleSheet(styles.TRANSPARENT_BG)
        self.BOTTOM_LAYOUT = widget.QVBoxLayout(self.BOTTOM_PANEL)
        self.BOTTOM_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.BOTTOM_LAYOUT.setSpacing(0)
        self.GRAPH_FRAME = None

        # ===== SEARCH FRAME =====
        self.SEARCH_FRAME = widget.QFrame()
        self.SEARCH_FRAME.setFixedHeight(45)
        self.SEARCH_FRAME.setStyleSheet(styles.SEARCH_FRAME)
        self.SEARCH_LAYOUT = widget.QHBoxLayout(self.SEARCH_FRAME)
        self.SEARCH_LAYOUT.setContentsMargins(8, 0, 8, 0)
        self.SEARCH_LAYOUT.setSpacing(8)

        # ===== SETTINGS =====
        self.SETTINGS_FRAME = widget.QFrame()
        self.SETTINGS_FRAME.setFixedSize(150, 45)
        self.SETTINGS_FRAME.setStyleSheet(styles.SETTINGS_FRAME)
        self.SETTINGSL = widget.QHBoxLayout(self.SETTINGS_FRAME)
        self.SETTINGSL.setContentsMargins(0, 0, 0, 0)
        self.SETTINGSL.setSpacing(5)

        self.SETTINGS = widget.QFrame(parent=self.SETTINGS_FRAME)
        self.SETTINGS.setFixedSize(45, 45)
        self.SETTINGS.setStyleSheet(styles.SETTINGS_BOX)

        self.SETT_LABEL = widget.QPushButton(self.SETTINGS)
        self.SETT_LABEL.setFixedSize(45, 45)

        self.PIXMAP = gui.QPixmap(create_media_path("Vector.png"))
        self.SETT_LABEL.setIcon(gui.QIcon(self.PIXMAP))
        self.SETT_LABEL.setIconSize(core.QSize(20, 20))
        self.SETT_LABEL.setStyleSheet(styles.SETTINGS_BUTTON)

        self.SETTINGS_NAME = widget.QLabel("Налаштування")
        self.SETTINGS_NAME.setStyleSheet(styles.SETTINGS_LABEL)
        self.SETTINGS_NAME.setAlignment(core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignVCenter)

        self.SETTINGSL.addWidget(self.SETTINGS, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.SETTINGSL.addWidget(self.SETTINGS_NAME, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.SETT_LABEL.clicked.connect(self.on_settings_clicked)

        # ===== КНОПКА ДОДАТИ =====
        self.ADD_CITY_BTN = widget.QPushButton("⊕ Додати")
        self.ADD_CITY_BTN.setFixedSize(100, 34)
        self.ADD_CITY_BTN.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.ADD_CITY_BTN.setStyleSheet(styles.ADD_CITY_BUTTON)
        self.ADD_CITY_BTN.hide()
        self.ADD_CITY_BTN.clicked.connect(self.ON_ADD_CITY_CLICKED)

        # ===== КОНТЕЙНЕР ПОШУКУ =====
        self.SEARCH_CONTAINER = widget.QFrame()
        self.SEARCH_CONTAINER.setFixedSize(261, 36)
        self.SEARCH_CONTAINER.setStyleSheet(styles.SEARCH_CONTAINER)
        self.SEARCH_CONTAINER_LAYOUT = widget.QHBoxLayout(self.SEARCH_CONTAINER)
        self.SEARCH_CONTAINER_LAYOUT.setContentsMargins(10, 0, 8, 0)
        self.SEARCH_CONTAINER_LAYOUT.setSpacing(6)

        self.SEARCH_ICON_LBL = widget.QLabel()
        self.SEARCH_ICON_LBL.setFixedSize(18, 18)
        self.SEARCH_ICON_LBL.setStyleSheet(styles.TRANSPARENT_NO_BORDER)
        search_icon_path = create_media_path("search.png")
        if os.path.exists(search_icon_path):
            self.SEARCH_ICON_LBL.setPixmap(
                gui.QPixmap(search_icon_path).scaled(
                    18, 18,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation
                )
            )

        self.CITY_SEARCH = widget.QLineEdit()
        self.CITY_SEARCH.setStyleSheet(styles.CITY_SEARCH)
        self.CITY_SEARCH.setPlaceholderText("Пошук")
        self.CITY_SEARCH.textChanged.connect(self.ON_SEARCH_TEXT_CHANGED)

        self.CLEAR_BTN = widget.QPushButton()
        self.CLEAR_BTN.setFixedSize(18, 18)
        self.CLEAR_BTN.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.CLEAR_BTN.setStyleSheet(styles.TRANSPARENT_NO_BORDER)
        remove_icon_path = create_media_path("remove.png")
        if os.path.exists(remove_icon_path):
            self.CLEAR_BTN.setIcon(gui.QIcon(remove_icon_path))
            self.CLEAR_BTN.setIconSize(core.QSize(18, 18))
        self.CLEAR_BTN.hide()
        self.CLEAR_BTN.clicked.connect(self._CLEAR_SEARCH)

        self.SEARCH_CONTAINER_LAYOUT.addWidget(self.SEARCH_ICON_LBL)
        self.SEARCH_CONTAINER_LAYOUT.addWidget(self.CITY_SEARCH)
        self.SEARCH_CONTAINER_LAYOUT.addWidget(self.CLEAR_BTN)

        self.SEARCH_LAYOUT.addWidget(self.SETTINGS_FRAME, alignment=core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignVCenter)
        self.SEARCH_LAYOUT.addStretch()
        self.SEARCH_LAYOUT.addWidget(self.ADD_CITY_BTN, alignment=core.Qt.AlignmentFlag.AlignVCenter)
        self.SEARCH_LAYOUT.addWidget(self.SEARCH_CONTAINER, alignment=core.Qt.AlignmentFlag.AlignVCenter)

        self.RIGHT_LAYOUT.addWidget(self.SEARCH_FRAME, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.PANELS_LAYOUT.addWidget(self.LEFT_PANEL)
        self.PANELS_LAYOUT.addWidget(self.RIGHT_PANEL)
        self.RIGHT_LAYOUT.addStretch()
        self.RIGHT_LAYOUT.addWidget(self.WEATHER_PANEL, alignment=core.Qt.AlignmentFlag.AlignBottom)
        self.RIGHT_LAYOUT.addWidget(self.BOTTOM_PANEL, alignment=core.Qt.AlignmentFlag.AlignBottom)

        # ===== DROPDOWN =====
        self.SEARCH_DROPDOWN = widget.QFrame(self.CENTRAL_WIDGET)
        self.SEARCH_DROPDOWN.setStyleSheet(styles.SEARCH_DROPDOWN)
        self.DROPDOWN_LAYOUT = widget.QVBoxLayout(self.SEARCH_DROPDOWN)
        self.DROPDOWN_LAYOUT.setContentsMargins(12, 10, 12, 10)
        self.DROPDOWN_LAYOUT.setSpacing(2)
        self.DROPDOWN_TITLE = widget.QLabel("Результати пошуку")
        self.DROPDOWN_TITLE.setStyleSheet(styles.DROPDOWN_TITLE)
        self.DROPDOWN_LAYOUT.addWidget(self.DROPDOWN_TITLE)
        self.DROPDOWN_LIST = widget.QListWidget()
        self.DROPDOWN_LIST.setFrameShape(widget.QFrame.Shape.NoFrame)
        self.DROPDOWN_LIST.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.DROPDOWN_LIST.setStyleSheet(styles.DROPDOWN_LIST)
        self.DROPDOWN_LIST.itemClicked.connect(self.ON_SEARCH_ITEM_SELECTED)
        self.DROPDOWN_LAYOUT.addWidget(self.DROPDOWN_LIST)
        self.SEARCH_DROPDOWN.hide()
        self.SEARCH_DROPDOWN.raise_()

        # Выбрать первую карточку по умолчанию
        if self.WEATHER_CARDS:
            core.QTimer.singleShot(0, lambda: self.ON_CARD_SELECTED(self.WEATHER_CARDS[0]))

    def on_settings_clicked(self):
        self.SETTINGS_WINDOW.raise_()
        self.SETTINGS_WINDOW.show()

    def ON_SEARCH_TEXT_CHANGED(self, text: str):
        text_stripped = text.strip()
        self.CLEAR_BTN.setVisible(bool(text_stripped))
        self._SELECTED_CITY = None
        self.ADD_CITY_BTN.hide()
        if not text_stripped:
            self.SEARCH_DROPDOWN.hide()
            return
        try:
            suggestions = SEARCH_CITIES(text_stripped)
        except Exception:
            suggestions = []
        self.DROPDOWN_LIST.clear()
        for city in suggestions:
            item = widget.QListWidgetItem(FORMAT_CITY(city))
            item.setData(core.Qt.ItemDataRole.UserRole, city)
            self.DROPDOWN_LIST.addItem(item)
        if self.DROPDOWN_LIST.count():
            row_h = 42
            rows = min(6, self.DROPDOWN_LIST.count())
            total_h = rows * row_h + 40
            self.SEARCH_DROPDOWN.setFixedSize(self.SEARCH_CONTAINER.width(), total_h)
            self._UPDATE_DROPDOWN_POS()
            self.SEARCH_DROPDOWN.show()
            self.SEARCH_DROPDOWN.raise_()
        else:
            self.SEARCH_DROPDOWN.hide()

    def ON_SEARCH_ITEM_SELECTED(self, item: widget.QListWidgetItem):
        city = item.data(core.Qt.ItemDataRole.UserRole)
        if not city:
            return
        self.CITY_SEARCH.blockSignals(True)
        self.CITY_SEARCH.setText(city.get("en", ""))
        self.CITY_SEARCH.blockSignals(False)
        self._SELECTED_CITY = city
        self.SEARCH_DROPDOWN.hide()
        self.ADD_CITY_BTN.show()

    def _UPDATE_DROPDOWN_POS(self):
        g = self.SEARCH_CONTAINER.mapToGlobal(core.QPoint(0, self.SEARCH_CONTAINER.height() + 4))
        p = self.CENTRAL_WIDGET.mapFromGlobal(g)
        self.SEARCH_DROPDOWN.move(p)

    def _CLEAR_SEARCH(self):
        self.CITY_SEARCH.clear()
        self.SEARCH_DROPDOWN.hide()
        self.ADD_CITY_BTN.hide()
        self._SELECTED_CITY = None

    def ON_ADD_CITY_CLICKED(self):
        if not self._SELECTED_CITY:
            return
        city_en = self._SELECTED_CITY.get("en", "")
        if not city_en:
            return
        if any(c.weather_data.get("city", "").lower() == city_en.lower() for c in self.WEATHER_CARDS):
            self._CLEAR_SEARCH()
            return
        ADD_USER_CITY(city_en)

        data = get_weather(city_en)
        if data:
            card = WeatherCard(
                data.get("city_display", data["city"]), data["time"], data["temp"],
                data["desc"], data["minmax"], data["is_current"]
            )
            card.weather_data = data
            card.selected.connect(self.ON_CARD_SELECTED)
            self.WEATHER_CARDS.append(card)
            self.CARDS_LAYOUT.insertWidget(self.CARDS_LAYOUT.count() - 1, card)
        self._CLEAR_SEARCH()

    def SET_THEME_LIGHT(self):
        self.IS_LIGHT_THEME = True
        self.CENTRAL_WIDGET.setStyleSheet(styles.LIGHT_THEME_CENTRAL)
        self.RIGHT_PANEL.setStyleSheet(styles.LIGHT_THEME_RIGHT_PANEL)

    def SET_THEME_DARK(self):
        self.IS_LIGHT_THEME = False
        self.CENTRAL_WIDGET.setStyleSheet(styles.CENTRAL_WIDGET)

    def REFRESH_WEATHER(self):
        for card in self.WEATHER_CARDS:
            city = card.weather_data.get("city")
            data = get_weather(city)
            if data:
                card.update_data(data)

    def ON_CARD_SELECTED(self, card: WeatherCard):
        if self.SELECTED_CARD and self.SELECTED_CARD != card:
            self.SELECTED_CARD.set_selected(False)
        card.set_selected(not card.IS_SELECTED)
        self.SELECTED_CARD = card if card.IS_SELECTED else None
        if self.CITY_INFO_FRAME:
            self.RIGHT_LAYOUT.removeWidget(self.CITY_INFO_FRAME)
            self.CITY_INFO_FRAME.deleteLater()
            self.CITY_INFO_FRAME = None
        if self.HOURLY_FRAME:
            self.WEATHER_LAYOUT.removeWidget(self.HOURLY_FRAME)
            self.HOURLY_FRAME.deleteLater()
            self.HOURLY_FRAME = None
        if self.GRAPH_FRAME:
            self.BOTTOM_LAYOUT.removeWidget(self.GRAPH_FRAME)
            self.GRAPH_FRAME.deleteLater()
            self.GRAPH_FRAME = None
        if self.SELECTED_CARD:
            self.CITY_INFO_FRAME = CityInfoFrame(self.SELECTED_CARD.weather_data)
            self.RIGHT_LAYOUT.insertWidget(1, self.CITY_INFO_FRAME)
            self.HOURLY_FRAME = HourlyForecastFrame(self.SELECTED_CARD.weather_data)
            self.WEATHER_LAYOUT.addWidget(self.HOURLY_FRAME)
            self.GRAPH_FRAME = TwelveHourGraphFrame(self.SELECTED_CARD.weather_data)
            self.BOTTOM_LAYOUT.addWidget(self.GRAPH_FRAME)


window = WeatherApp()