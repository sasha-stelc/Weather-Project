import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from ..api_request import GET_CITY_EN, get_weather
from ..card import WeatherCard
from .. import styles
from ..settings.size_config import SizeManager
from ..settings.langueges import LANGUAGE_SIGNAL, LanguageManager
from .theme_switch import ImageThemeSwitch


class LeftPanel(widget.QFrame):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setFixedWidth(SizeManager.get("left_panel_width"))
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

        self.WEATHER_CARDS: list[WeatherCard] = []
        self.SELECTED_CARD: WeatherCard | None = None

        self.CARDS_LAYOUT.addStretch()
        self.SCROLL_AREA.setWidget(self.CARDS_CONTAINER)
        self.LAYOUT.addWidget(self.SCROLL_AREA)

        # ── підписка на зміну мови ──
        LANGUAGE_SIGNAL.language_changed.connect(self.retranslate)

    # ────────────────────────── ПОБУДОВА / КЕРУВАННЯ КАРТКАМИ ──────────────────────────

    def build_cards(self, cities: list[dict]):
        """Створює картки погоди для переданого списку міст."""
        for city in cities:
            city_en = GET_CITY_EN(city)
            if not city_en:
                continue
            data = get_weather(city_en)
            if not data:
                continue
            data["city_display"] = city.get("display") or city_en
            data["country"]      = city.get("country", "")
            self._create_card(data)

    def add_card(self, city_data: dict) -> WeatherCard:
        """Додає нову картку."""
        city_data = dict(city_data)
        city_data.setdefault("city_display", city_data.get("city", ""))
        return self._create_card(city_data)

    def _create_card(self, data: dict) -> WeatherCard:
        """Внутрішній фабричний метод: створює картку і реєструє її."""
        card = WeatherCard(
            data.get("city_display", data["city"]),
            data["time"],
            data["temp"],
            data["desc"],
            data["minmax"],
            data["is_current"],
        )
        card.weather_data = data
        card.selected.connect(self.on_card_selected)
        self.WEATHER_CARDS.append(card)
        self.CARDS_LAYOUT.insertWidget(self.CARDS_LAYOUT.count() - 1, card)
        return card

    def remove_card(self, card: WeatherCard):
        """Видаляє картку."""
        if card in self.WEATHER_CARDS:
            self.CARDS_LAYOUT.removeWidget(card)
            card.deleteLater()
            self.WEATHER_CARDS.remove(card)

    def clear_cards(self):
        """Очищає всі картки."""
        for card in self.WEATHER_CARDS[:]:
            self.remove_card(card)

    def get_card_by_city(self, city: str) -> WeatherCard | None:
        """Повертає картку за назвою міста (en або display)."""
        city_lower = city.lower()
        for card in self.WEATHER_CARDS:
            if (
                card.weather_data.get("city", "").lower() == city_lower
                or card.weather_data.get("city_display", "").lower() == city_lower
            ):
                return card
        return None

    # ────────────────────────── ОНОВЛЕННЯ ДАНИХ ──────────────────────────

    def refresh_weather(self):
        """Оновлює погоду для всіх карток (новий запит до API / кеш)."""
        for card in self.WEATHER_CARDS:
            city_en = GET_CITY_EN(card.weather_data)
            data    = get_weather(city_en)
            if data:
                # зберігаємо display-поля, які прийшли ззовні
                data["city_display"] = card.weather_data.get("city_display", data["city"])
                data["country"]      = card.weather_data.get("country", "")
                card.weather_data    = data
                card.update_data(data)

    def retranslate(self, lang: str | None = None):
        """Оновлює текст усіх карток при зміні мови.

        Не робить нових запитів до API — бере готові переклади з
        полів ``city_names``, ``desc_i18n`` і ``minmax_i18n``,
        які зберігаються у weather_data після кешування.
        """
        cur_lang = lang or LanguageManager.get_language()

        for card in self.WEATHER_CARDS:
            data = card.weather_data

            # ── назва міста ──
            city_names   = data.get("city_names", {})
            city_display = (
                city_names.get(cur_lang)
                or data.get("city_display")
                or data.get("city", "")
            )

            # ── опис погоди ──
            desc_i18n = data.get("desc_i18n", {})
            desc      = desc_i18n.get(cur_lang) or data.get("desc", "")

            # ── рядок min/max ──
            minmax_i18n = data.get("minmax_i18n", {})
            minmax      = minmax_i18n.get(cur_lang) or data.get("minmax", "")

            # синхронізуємо weather_data з поточною мовою
            data["city_display"] = city_display
            data["desc"]         = desc
            data["minmax"]       = minmax

            card.update_data(data)

    # ────────────────────────── ПОДІЇ ──────────────────────────

    def on_card_selected(self, card: WeatherCard):
        """Обробник вибору картки."""
        if self.app:
            self.app.ON_CARD_SELECTED(card)