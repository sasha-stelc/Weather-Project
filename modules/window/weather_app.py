import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from ..card import WeatherCard
from .. import styles
from ..api_request import (
    GET_CITY_EN, get_weather, LOAD_USER_CITIES,
    USER_CITIES_PATH
)
from ..title_bar import TitleBar
from ..settings import Settings
from ..settings.langueges import LanguageManager
from .left_panel import LeftPanel
from .right_panel import RightPanel
from .search_panel import SearchPanel
from .settings_panel import SettingsPanel


class WeatherApp(widget.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(LanguageManager.get_text("WINDOW_TITLE"))
        self.resize(1200, 800)
        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.IS_LIGHT_THEME   = False
        self.IS_SETTINGS_OPEN = False
        self.SETTINGS_FRAME   = None

        # ===== ЦЕНТРАЛЬНЫЙ ВИДЖЕТ =====
        self.CENTRAL_WIDGET = widget.QWidget()
        self.CENTRAL_WIDGET.setObjectName("centralWidget")
        self.CENTRAL_WIDGET.setStyleSheet(styles.CENTRAL_WIDGET)
        self.CENTRAL_WIDGET.setSizePolicy(
            widget.QSizePolicy.Policy.Expanding,
            widget.QSizePolicy.Policy.Expanding,
        )
        self.setCentralWidget(self.CENTRAL_WIDGET)

        self.MAIN_LAYOUT = widget.QVBoxLayout(self.CENTRAL_WIDGET)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAIN_LAYOUT.setSpacing(0)

        # ===== ЗАГОЛОВОК =====
        self.TITLE_BAR = TitleBar(self)
        self.TITLE_BAR.setStyleSheet(styles.TITLE_BAR)
        self.MAIN_LAYOUT.addWidget(self.TITLE_BAR,
            alignment=core.Qt.AlignmentFlag.AlignLeft)

        # ===== ПАНЕЛИ СЛЕВА И СПРАВА =====
        self.PANELS_LAYOUT = widget.QHBoxLayout()
        self.PANELS_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.PANELS_LAYOUT.setSpacing(0)
        self.MAIN_LAYOUT.addLayout(self.PANELS_LAYOUT)

        # Левая панель с карточками городов
        self.LEFT_PANEL = LeftPanel(app=self)
        self.PANELS_LAYOUT.addWidget(self.LEFT_PANEL)

        # Правая панель с информацией о погоде
        self.RIGHT_PANEL = RightPanel()
        self.PANELS_LAYOUT.addWidget(self.RIGHT_PANEL)

        # ===== ПОИСК И НАСТРОЙКИ =====
        self.SEARCH_PANEL = SearchPanel(self.CENTRAL_WIDGET)
        self.SETTINGS_PANEL = SettingsPanel()
        
        # Добавляем панель настроек и кнопку в поиск
        search_layout = self.SEARCH_PANEL.LAYOUT
        search_layout.insertWidget(0, self.SETTINGS_PANEL,
            alignment=core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignVCenter)
        
        # Подключаем сигналы
        self.SEARCH_PANEL.city_selected.connect(self._on_city_added)
        self.SETTINGS_PANEL.settings_clicked.connect(self.on_settings_clicked)
        
        # Устанавливаем панель поиска в правую панель
        self.RIGHT_PANEL.set_search_frame(self.SEARCH_PANEL)

        # ===== ТАЙМЕР ОБНОВЛЕНИЯ ПОГОДЫ =====
        self.UPDATE_TIMER = core.QTimer(self)
        self.UPDATE_TIMER.setInterval(5 * 60 * 1000)  # 5 минут
        self.UPDATE_TIMER.timeout.connect(self.REFRESH_WEATHER)
        self.UPDATE_TIMER.start()

        # ===== НАБЛЮДЕНИЕ ЗА ФАЙЛОМ user_cities.json =====
        self.FILE_WATCHER = core.QFileSystemWatcher(self)
        self._WATCH_CITIES_FILE()
        self.FILE_WATCHER.fileChanged.connect(self._ON_CITIES_FILE_CHANGED)

        # ===== ИНИЦИАЛИЗАЦИЯ КАРТОЧЕК =====
        self.LEFT_PANEL.build_cards(LOAD_USER_CITIES())

        # Выбираем первую карточку по умолчанию
        if self.LEFT_PANEL.WEATHER_CARDS:
            core.QTimer.singleShot(0,
                lambda: self.ON_CARD_SELECTED(self.LEFT_PANEL.WEATHER_CARDS[0]))

    # ──────────────────────────────────────────────
    # НАБЛЮДЕНИЕ ЗА ФАЙЛАМИ
    # ──────────────────────────────────────────────

    def _WATCH_CITIES_FILE(self):
        """Добавляет файл в наблюдатель."""
        if os.path.exists(USER_CITIES_PATH):
            watched = self.FILE_WATCHER.files()
            if USER_CITIES_PATH not in watched:
                self.FILE_WATCHER.addPath(USER_CITIES_PATH)

    def _ON_CITIES_FILE_CHANGED(self, path: str):
        """Обрабатывает изменение файла user_cities.json."""
        core.QTimer.singleShot(150, self._RELOAD_CARDS_FROM_JSON)
        core.QTimer.singleShot(200, self._WATCH_CITIES_FILE)

    def _RELOAD_CARDS_FROM_JSON(self):
        """Синхронизирует карточки с содержимым user_cities.json."""
        cities_in_json = LOAD_USER_CITIES()
        cities_lower   = [GET_CITY_EN(c).lower() for c in cities_in_json if GET_CITY_EN(c)]

        # Удаляем карточки, которых нет в JSON
        cards_to_remove = [
            c for c in self.LEFT_PANEL.WEATHER_CARDS
            if c.weather_data.get("city", "").lower() not in cities_lower
        ]
        for card in cards_to_remove:
            if self.LEFT_PANEL.SELECTED_CARD is card:
                self.RIGHT_PANEL.clear_weather_ui()
                self.LEFT_PANEL.SELECTED_CARD = None
            self.LEFT_PANEL.remove_card(card)

        # Добавляем новые карточки
        existing_lower = [
            c.weather_data.get("city", "").lower()
            for c in self.LEFT_PANEL.WEATHER_CARDS
        ]
        for city in cities_in_json:
            city_en = GET_CITY_EN(city)
            if not city_en:
                continue
            if city_en.lower() in existing_lower:
                continue
            data = get_weather(city_en)
            if not data:
                continue
            data["city_display"] = city.get("display") or city_en
            data["country"] = city.get("country", "")
            self.LEFT_PANEL.add_card(data)

    # ──────────────────────────────────────────────
    # РАЗМЕР ОКНА
    # ──────────────────────────────────────────────

    def APPLY_WINDOW_SIZE(self, width: int, height: int):
        """Применяет размер окна."""
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.resize(width, height)

        left_width  = max(320, min(420, int(width * 0.28)))
        right_width = max(620, width - left_width - 40)

        self.LEFT_PANEL.setFixedWidth(left_width)
        self.RIGHT_PANEL.WEATHER_PANEL.setFixedSize(right_width, max(140, int(height * 0.195)))
        self.RIGHT_PANEL.BOTTOM_PANEL.setFixedSize(right_width,  max(160, int(height * 0.23)))
        self.SEARCH_PANEL.SEARCH_CONTAINER.setFixedWidth(max(220, int(width * 0.22)))

        if hasattr(self, "SETTINGS_WINDOW"):
            self.SETTINGS_WINDOW.setGeometry(0, 26, width, height)

    # ──────────────────────────────────────────────
    # НАСТРОЙКИ
    # ──────────────────────────────────────────────
    def on_settings_clicked(self):
        """Открывает или закрывает панель настроек."""
        if self.IS_SETTINGS_OPEN:
            self.close_settings()
            return

        self.RIGHT_PANEL.clear_weather_ui()

        search_h = self.SEARCH_PANEL.height()
        self.SETTINGS_FRAME = Settings(self.RIGHT_PANEL, main_app=self)
        self.SETTINGS_FRAME.setGeometry(
            0, search_h,
            self.RIGHT_PANEL.width(),
            self.RIGHT_PANEL.height() - search_h,
        )
        self.SETTINGS_FRAME.show()
        self.SETTINGS_FRAME.raise_()
        self.IS_SETTINGS_OPEN = True

        # Показуємо на карті поточне вибране місто
        if self.LEFT_PANEL.SELECTED_CARD:
            data = self.LEFT_PANEL.SELECTED_CARD.weather_data
            lat = data.get("lat") or data.get("latitude")
            lon = data.get("lon") or data.get("longitude")
            city_name = data.get("city_display") or data.get("city")
            
            if lat and lon:
                try:
                    lat_f = float(lat)
                    lon_f = float(lon)
                    # Добавляем небольшую задержку, чтобы карта успела загрузиться
                    core.QTimer.singleShot(200, 
                        lambda: self.SETTINGS_FRAME.update_map_for_city(lat_f, lon_f, city_name))
                except Exception as e:
                    msg = LanguageManager.get_text("ERROR_UPDATE_MAP", e=e)
                    print(msg)
    def close_settings(self):
        """Закрывает панель настроек."""
        if self.SETTINGS_FRAME:
            self.RIGHT_PANEL.LAYOUT.removeWidget(self.SETTINGS_FRAME)
            self.SETTINGS_FRAME.deleteLater()
            self.SETTINGS_FRAME = None
        self.IS_SETTINGS_OPEN = False
        if self.LEFT_PANEL.SELECTED_CARD:
            self.ON_CARD_SELECTED(self.LEFT_PANEL.SELECTED_CARD)

    # ──────────────────────────────────────────────
    # ТЕМА
    # ──────────────────────────────────────────────

    def SET_THEME_LIGHT(self):
        """Включает светлую тему."""
        self.IS_LIGHT_THEME = True
        self.CENTRAL_WIDGET.setStyleSheet(styles.LIGHT_THEME_CENTRAL)
        self.RIGHT_PANEL.setStyleSheet(styles.LIGHT_THEME_RIGHT_PANEL)

    def SET_THEME_DARK(self):
        """Включает темную тему."""
        self.IS_LIGHT_THEME = False
        self.CENTRAL_WIDGET.setStyleSheet(styles.CENTRAL_WIDGET)

    # ──────────────────────────────────────────────
    # ПОГОДА
    # ──────────────────────────────────────────────

    def REFRESH_WEATHER(self):
        """Обновляет погоду для всех карточек."""
        self.LEFT_PANEL.refresh_weather()

    def ON_CARD_SELECTED(self, card: WeatherCard):
        """Обработчик выбора карточки."""
        
        # Закриваємо налаштування, якщо вони відкриті
        if self.IS_SETTINGS_OPEN:
            self.close_settings()

        # Знімаємо виділення з попередньої картки
        if self.LEFT_PANEL.SELECTED_CARD and self.LEFT_PANEL.SELECTED_CARD != card:
            self.LEFT_PANEL.SELECTED_CARD.set_selected(False)

        # Перемикаємо стан виділення
        card.set_selected(not card.IS_SELECTED)
        
        # Оновлюємо поточну вибрану картку
        self.LEFT_PANEL.SELECTED_CARD = card if card.IS_SELECTED else None

        # Очищуємо праву панель
        self.RIGHT_PANEL.clear_weather_ui()

        # Показуємо інформацію по вибраній картці
        if self.LEFT_PANEL.SELECTED_CARD:
            weather_data = self.LEFT_PANEL.SELECTED_CARD.weather_data
            self.RIGHT_PANEL.set_city_info(weather_data)
            self.RIGHT_PANEL.set_hourly_forecast(weather_data)
            self.RIGHT_PANEL.set_twelve_hour_graph(weather_data)

    def _on_city_added(self, city_data):
        """Обработчик добавления города."""
        pass  # Синхронизация происходит через файловый наблюдатель

    def on_language_changed(self):
        """Обработчик изменения языка приложения"""
        # Обновляем заголовок главного окна
        self.setWindowTitle(LanguageManager.get_text("WINDOW_TITLE"))
        # Можно добавить другие обновления интерфейса при необходимости


window = WeatherApp()
