import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from ..api_request import LOAD_USER_CITIES, get_weather
from ..card import WeatherCard
from .. import styles
from .theme_switch import ImageThemeSwitch


class LeftPanel(widget.QFrame):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setFixedWidth(370)
        self.setStyleSheet(styles.LEFT_PANEL)
        
        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setContentsMargins(20, 20, 20, 0)
        self.LAYOUT.setSpacing(10)
        
        # Кнопка переключения темы
        self.THEME_SWITCH = ImageThemeSwitch(app=self.app)
        self.LAYOUT.addWidget(self.THEME_SWITCH,
            alignment=core.Qt.AlignmentFlag.AlignRight)
        
        # Область прокрутки
        self.SCROLL_AREA = widget.QScrollArea()
        self.SCROLL_AREA.setVerticalScrollBarPolicy(
            core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
        
        self.CARDS_LAYOUT.addStretch()
        self.SCROLL_AREA.setWidget(self.CARDS_CONTAINER)
        self.LAYOUT.addWidget(self.SCROLL_AREA)
    
    def build_cards(self, cities: list[str]):
        """Создает карточки погоды для переданного списка городов."""
        for city_en in cities:
            data = get_weather(city_en)
            if not data:
                continue
            card = WeatherCard(
                data.get("city_display", data["city"]),
                data["time"], data["temp"],
                data["desc"], data["minmax"],
                data["is_current"],
            )
            card.weather_data = data
            card.selected.connect(self.on_card_selected)
            self.WEATHER_CARDS.append(card)
            self.CARDS_LAYOUT.insertWidget(
                self.CARDS_LAYOUT.count() - 1, card)
    
    def on_card_selected(self, card: WeatherCard):
        """Обработчик выбора карточки."""
        if self.app:
            self.app.ON_CARD_SELECTED(card)
    
    def refresh_weather(self):
        """Обновляет погоду для всех карточек."""
        for card in self.WEATHER_CARDS:
            city = card.weather_data.get("city")
            data = get_weather(city)
            if data:
                card.update_data(data)
    
    def add_card(self, city_data):
        """Добавляет новую карточку."""
        card = WeatherCard(
            city_data.get("city_display", city_data["city"]),
            city_data["time"], city_data["temp"],
            city_data["desc"], city_data["minmax"],
            city_data["is_current"],
        )
        card.weather_data = city_data
        card.selected.connect(self.on_card_selected)
        self.WEATHER_CARDS.append(card)
        self.CARDS_LAYOUT.insertWidget(
            self.CARDS_LAYOUT.count() - 1, card)
        return card
    
    def remove_card(self, card: WeatherCard):
        """Удаляет карточку."""
        if card in self.WEATHER_CARDS:
            self.CARDS_LAYOUT.removeWidget(card)
            card.deleteLater()
            self.WEATHER_CARDS.remove(card)
    
    def clear_cards(self):
        """Очищает все карточки."""
        for card in self.WEATHER_CARDS[:]:
            self.remove_card(card)
    
    def get_card_by_city(self, city: str):
        """Получает карточку по названию города."""
        city_lower = city.lower()
        for card in self.WEATHER_CARDS:
            if card.weather_data.get("city", "").lower() == city_lower:
                return card
        return None
