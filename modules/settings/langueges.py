import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
from .. import styles
from .size_config import SizeManager
import json
import os
class _LanguageSignalEmitter(core.QObject):
    language_changed = core.pyqtSignal(str)


# Глобальный экземпляр сигнала
LANGUAGE_SIGNAL = _LanguageSignalEmitter()

# ===== СИСТЕМА ЛОКАЛИЗАЦИИ =====
class LanguageManager:
    """Глобальный менеджер языков для приложения"""
    language_changed = core.pyqtSignal(str)
    # Словари с переводами на все поддерживаемые языки
    TRANSLATIONS = {
        "uk": {  # Українська
            # settings/langueges.py
            "DESC_PAGE_LANGUAGE": "Мова додатку",
            "TITLE_CHOOSE_LANGUAGE": "Оберіть мову додатку",
            "LABEL_LANGUAGE": "Мова додатку",
            "LANG_UKRAINIAN": "Українська",
            "LANG_RUSSIAN": "Русский",
            "LANG_ENGLISH": "English",
            "LANG_NORWEGIAN": "Norsk",
            "BTN_SAVE": "Зберегти",

            # settings/images.py
            "LISTS": "Списки зображень",
            "LISTS_IMAGES": "Список зображень №1",
            "LISTS_IMAGES2": "Список зображень №2",
            
            # settings/application_size.py
            "DESC_PAGE_SIZE": "Розмір додатку",
            "TITLE_CHOOSE_SIZE": "Оберіть розмір додатку",
            "SIZE_SELECTED": "Обрано розмір: {text} ({width}x{height})",
            "SIZE_ERROR": "❌ Помилка: не вдалося отримати розмір",
            
            # settings/search_sity.py
            "DESC_PAGE_SEARCH": "Пошук міста",
            "TITLE_SEARCH_CITY": "Пошук міста",
            "LABEL_COUNTRY": "Країна",
            "PLACEHOLDER_COUNTRY": "Пошук країни",
            "LABEL_CITY": "Місто",
            "PLACEHOLDER_CITY": "Пошук міста",
            "LABEL_COORDINATES": "Координати",
            "PLACEHOLDER_COORDINATES": "lat, lon",
            "RESULT_COUNTRIES": "Результати пошуку країн",
            "RESULT_CITIES": "Результати пошуку",
            "LABEL_ADDED_CITIES": "Додані міста",
            "ERROR_CACHE_LOAD": "Помилка завантаження кешу: {e}",
            
            # settings/settings.py
            "TITLE_SETTINGS": "Налаштування",
            "BTN_CLOSE": "✕",
            "NAV_SEARCH_CITY": "Пошук міста",
            "NAV_APP_SIZE": "Розмір додатку",
            "NAV_LANGUAGE": "Мова додатку",
            "NAV_IMAGE_LISTS": "Списки зображень",
            "PAGE_IMAGE_LISTS": "Списки зображень",
            
            # window/weather_app.py
            "WINDOW_TITLE": "Погода",
            "ERROR_UPDATE_MAP": "Помилка оновлення карти: {e}",
            
            # window/search_panel.py
            "PLACEHOLDER_SEARCH": "Пошук",
            "BTN_ADD_CITY": "⊕ Додати",
            "RESULT_SEARCH": "Результати пошуку",
            
            # window/settings_panel.py
            "LABEL_SETTINGS": "Налаштування",
            
            # card/city_info_frame.py
            "LABEL_CURRENT_POSITION": "Поточна позиція",
            "LABEL_TODAY": "Сьогодні",
            "DAY_MONDAY": "Понеділок",
            "DAY_TUESDAY": "Вівторок",
            "DAY_WEDNESDAY": "Середа",
            "DAY_THURSDAY": "Четвер",
            "DAY_FRIDAY": "П'ятниця",
            "DAY_SATURDAY": "Субота",
            "DAY_SUNDAY": "Неділя",
            
            # card/hourly_forecast_frame.py
            "TEXT_NOW": "Зараз",
            "TEXT_SUNSET": "Захід сонця",
            "TEXT_SUNRISE": "Схід сонця",
            
            # card/twelve_hour_graph_frame.py
            "TITLE_12H_FORECAST": "Прогноз на 12 годин",
            # weather api
            "WEATHER_CLEAR_SKY": "Ясно",
            "WEATHER_FEW_CLOUDS": "Малохмарно",
            "WEATHER_SCATTERED_CLOUDS": "Мінлива хмарність",
            "WEATHER_BROKEN_CLOUDS": "Хмарно",
            "WEATHER_OVERCAST_CLOUDS": "Похмуро",

            "WEATHER_MIST": "Туман",
            "WEATHER_FOG": "Густий туман",
            "WEATHER_HAZE": "Імла",
            "WEATHER_SMOKE": "Дим",

            "WEATHER_LIGHT_RAIN": "Легкий дощ",
            "WEATHER_MODERATE_RAIN": "Помірний дощ",
            "WEATHER_HEAVY_INTENSITY_RAIN": "Сильний дощ",
            "WEATHER_VERY_HEAVY_RAIN": "Дуже сильний дощ",
            "WEATHER_EXTREME_RAIN": "Злива",
            "WEATHER_FREEZING_RAIN": "Крижаний дощ",
            "WEATHER_SHOWER_RAIN": "Короткочасний дощ",

            "WEATHER_THUNDERSTORM": "Гроза",
            "WEATHER_THUNDERSTORM_WITH_LIGHT_RAIN": "Гроза з легким дощем",
            "WEATHER_THUNDERSTORM_WITH_RAIN": "Гроза з дощем",

            "WEATHER_LIGHT_SNOW": "Легкий сніг",
            "WEATHER_SNOW": "Сніг",
            "WEATHER_HEAVY_SNOW": "Сильний сніг",
            "WEATHER_SLEET": "Мокрий сніг",

            "WEATHER_DUST": "Пил",
            "WEATHER_SAND": "Пісок",
            "WEATHER_ASH": "Попіл",
            "WEATHER_SQUALL": "Шквал",
            "WEATHER_TORNADO": "Торнадо",
        },
        
        "ru": {  # Русский
            # settings/langueges.py
            "DESC_PAGE_LANGUAGE": "Язык приложения",
            "TITLE_CHOOSE_LANGUAGE": "Выберите язык приложения",
            "LABEL_LANGUAGE": "Язык приложения",
            "LANG_UKRAINIAN": "Українська",
            "LANG_RUSSIAN": "Русский",
            "LANG_ENGLISH": "English",
            "LANG_NORWEGIAN": "Norsk",
            "BTN_SAVE": "Сохранить",

            # settings/images.py
            "LISTS": "Списки изображений",
            "LISTS_IMAGES": "Список изображений №1",
            "LISTS_IMAGES2": "Список изображений №2",
            
            # settings/application_size.py
            "DESC_PAGE_SIZE": "Размер приложения",
            "TITLE_CHOOSE_SIZE": "Выберите размер приложения",
            "SIZE_SELECTED": "Выбран размер: {text} ({width}x{height})",
            "SIZE_ERROR": "❌ Ошибка: не удалось получить размер",
            
            # settings/search_sity.py
            "DESC_PAGE_SEARCH": "Поиск города",
            "TITLE_SEARCH_CITY": "Поиск города",
            "LABEL_COUNTRY": "Страна",
            "PLACEHOLDER_COUNTRY": "Поиск страны",
            "LABEL_CITY": "Город",
            "PLACEHOLDER_CITY": "Поиск города",
            "LABEL_COORDINATES": "Координаты",
            "PLACEHOLDER_COORDINATES": "lat, lon",
            "RESULT_COUNTRIES": "Результаты поиска стран",
            "RESULT_CITIES": "Результаты поиска",
            "LABEL_ADDED_CITIES": "Добавленные города",
            "ERROR_CACHE_LOAD": "Ошибка загрузки кэша: {e}",
            
            # settings/settings.py
            "TITLE_SETTINGS": "Параметры",
            "BTN_CLOSE": "✕",
            "NAV_SEARCH_CITY": "Поиск города",
            "NAV_APP_SIZE": "Размер приложения",
            "NAV_LANGUAGE": "Язык приложения",
            "NAV_IMAGE_LISTS": "Списки изображений",
            "PAGE_IMAGE_LISTS": "Списки изображений",
            
            # window/weather_app.py
            "WINDOW_TITLE": "Погода",
            "ERROR_UPDATE_MAP": "Ошибка обновления карты: {e}",
            
            # window/search_panel.py
            "PLACEHOLDER_SEARCH": "Поиск",
            "BTN_ADD_CITY": "⊕ Добавить",
            "RESULT_SEARCH": "Результаты поиска",
            
            # window/settings_panel.py
            "LABEL_SETTINGS": "Параметры",
            
            # card/city_info_frame.py
            "LABEL_CURRENT_POSITION": "Текущее местоположение",
            "LABEL_TODAY": "Сегодня",
            "DAY_MONDAY": "Понедельник",
            "DAY_TUESDAY": "Вторник",
            "DAY_WEDNESDAY": "Среда",
            "DAY_THURSDAY": "Четверг",
            "DAY_FRIDAY": "Пятница",
            "DAY_SATURDAY": "Суббота",
            "DAY_SUNDAY": "Воскресенье",
            
            # card/hourly_forecast_frame.py
            "TEXT_NOW": "Сейчас",
            "TEXT_SUNSET": "Закат",
            "TEXT_SUNRISE": "Восход",
            
            # card/twelve_hour_graph_frame.py
            "TITLE_12H_FORECAST": "Прогноз на 12 часов",
            # weather api
            "WEATHER_CLEAR_SKY": "Ясно",
            "WEATHER_FEW_CLOUDS": "Малооблачно",
            "WEATHER_SCATTERED_CLOUDS": "Переменная облачность",
            "WEATHER_BROKEN_CLOUDS": "Облачно",
            "WEATHER_OVERCAST_CLOUDS": "Пасмурно",

            "WEATHER_MIST": "Туман",
            "WEATHER_FOG": "Густой туман",
            "WEATHER_HAZE": "Дымка",
            "WEATHER_SMOKE": "Дым",

            "WEATHER_LIGHT_RAIN": "Лёгкий дождь",
            "WEATHER_MODERATE_RAIN": "Умеренный дождь",
            "WEATHER_HEAVY_INTENSITY_RAIN": "Сильный дождь",
            "WEATHER_VERY_HEAVY_RAIN": "Очень сильный дождь",
            "WEATHER_EXTREME_RAIN": "Ливень",
            "WEATHER_FREEZING_RAIN": "Ледяной дождь",
            "WEATHER_SHOWER_RAIN": "Кратковременный дождь",

            "WEATHER_THUNDERSTORM": "Гроза",
            "WEATHER_THUNDERSTORM_WITH_LIGHT_RAIN": "Гроза с лёгким дождём",
            "WEATHER_THUNDERSTORM_WITH_RAIN": "Гроза с дождём",

            "WEATHER_LIGHT_SNOW": "Лёгкий снег",
            "WEATHER_SNOW": "Снег",
            "WEATHER_HEAVY_SNOW": "Сильный снег",
            "WEATHER_SLEET": "Мокрый снег",

            "WEATHER_DUST": "Пыль",
            "WEATHER_SAND": "Песок",
            "WEATHER_ASH": "Пепел",
            "WEATHER_SQUALL": "Шквал",
            "WEATHER_TORNADO": "Торнадо",
        },
        
        "en": {  # English
            # settings/langueges.py
            "DESC_PAGE_LANGUAGE": "Application Language",
            "TITLE_CHOOSE_LANGUAGE": "Choose Application Language",
            "LABEL_LANGUAGE": "Application Language",
            "LANG_UKRAINIAN": "Українська",
            "LANG_RUSSIAN": "Русский",
            "LANG_ENGLISH": "English",
            "LANG_NORWEGIAN": "Norsk",
            "BTN_SAVE": "Save",

            # settings/images.py
            "LISTS": "lists picture",
            "LISTS_IMAGES": "List of images №1",
            "LISTS_IMAGES2": "List of images №2",
            
            # settings/application_size.py
            "DESC_PAGE_SIZE": "Application Size",
            "TITLE_CHOOSE_SIZE": "Choose Application Size",
            "SIZE_SELECTED": "Selected size: {text} ({width}x{height})",
            "SIZE_ERROR": "❌ Error: Failed to get size",
            
            # settings/search_sity.py
            "DESC_PAGE_SEARCH": "City Search",
            "TITLE_SEARCH_CITY": "City Search",
            "LABEL_COUNTRY": "Country",
            "PLACEHOLDER_COUNTRY": "Search country",
            "LABEL_CITY": "City",
            "PLACEHOLDER_CITY": "Search city",
            "LABEL_COORDINATES": "Coordinates",
            "PLACEHOLDER_COORDINATES": "lat, lon",
            "RESULT_COUNTRIES": "Country Search Results",
            "RESULT_CITIES": "Search Results",
            "LABEL_ADDED_CITIES": "Added Cities",
            "ERROR_CACHE_LOAD": "Cache loading error: {e}",
            
            # settings/settings.py
            "TITLE_SETTINGS": "Settings",
            "BTN_CLOSE": "✕",
            "NAV_SEARCH_CITY": "City Search",
            "NAV_APP_SIZE": "Application Size",
            "NAV_LANGUAGE": "Application Language",
            "NAV_IMAGE_LISTS": "Image Lists",
            "PAGE_IMAGE_LISTS": "Image Lists",
            
            # window/weather_app.py
            "WINDOW_TITLE": "Weather",
            "ERROR_UPDATE_MAP": "Map update error: {e}",
            
            # window/search_panel.py
            "PLACEHOLDER_SEARCH": "Search",
            "BTN_ADD_CITY": "⊕ Add",
            "RESULT_SEARCH": "Search Results",
            
            # window/settings_panel.py
            "LABEL_SETTINGS": "Settings",
            
            # card/city_info_frame.py
            "LABEL_CURRENT_POSITION": "Current Position",
            "LABEL_TODAY": "Today",
            "DAY_MONDAY": "Monday",
            "DAY_TUESDAY": "Tuesday",
            "DAY_WEDNESDAY": "Wednesday",
            "DAY_THURSDAY": "Thursday",
            "DAY_FRIDAY": "Friday",
            "DAY_SATURDAY": "Saturday",
            "DAY_SUNDAY": "Sunday",
            
            # card/hourly_forecast_frame.py
            "TEXT_NOW": "Now",
            "TEXT_SUNSET": "Sunset",
            "TEXT_SUNRISE": "Sunrise",
            
            # card/twelve_hour_graph_frame.py
            "TITLE_12H_FORECAST": "12 Hour Forecast",
            # weather api
            "WEATHER_CLEAR_SKY": "Clear sky",
            "WEATHER_FEW_CLOUDS": "Few clouds",
            "WEATHER_SCATTERED_CLOUDS": "Scattered clouds",
            "WEATHER_BROKEN_CLOUDS": "Broken clouds",
            "WEATHER_OVERCAST_CLOUDS": "Overcast clouds",

            "WEATHER_MIST": "Mist",
            "WEATHER_FOG": "Fog",
            "WEATHER_HAZE": "Haze",
            "WEATHER_SMOKE": "Smoke",

            "WEATHER_LIGHT_RAIN": "Light rain",
            "WEATHER_MODERATE_RAIN": "Moderate rain",
            "WEATHER_HEAVY_INTENSITY_RAIN": "Heavy rain",
            "WEATHER_VERY_HEAVY_RAIN": "Very heavy rain",
            "WEATHER_EXTREME_RAIN": "Extreme rain",
            "WEATHER_FREEZING_RAIN": "Freezing rain",
            "WEATHER_SHOWER_RAIN": "Shower rain",

            "WEATHER_THUNDERSTORM": "Thunderstorm",
            "WEATHER_THUNDERSTORM_WITH_LIGHT_RAIN": "Thunderstorm with light rain",
            "WEATHER_THUNDERSTORM_WITH_RAIN": "Thunderstorm with rain",

            "WEATHER_LIGHT_SNOW": "Light snow",
            "WEATHER_SNOW": "Snow",
            "WEATHER_HEAVY_SNOW": "Heavy snow",
            "WEATHER_SLEET": "Sleet",

            "WEATHER_DUST": "Dust",
            "WEATHER_SAND": "Sand",
            "WEATHER_ASH": "Ash",
            "WEATHER_SQUALL": "Squall",
            "WEATHER_TORNADO": "Tornado",
        },
        "no": {  # Norsk (Bokmål)
            # settings/langueges.py
            "DESC_PAGE_LANGUAGE": "App-språk",
            "TITLE_CHOOSE_LANGUAGE": "Velg app-språk",
            "LABEL_LANGUAGE": "App-språk",
            
            "LANG_UKRAINIAN": "Ukrainsk",
            "LANG_RUSSIAN": "Russisk",
            "LANG_ENGLISH": "Engelsk",
            "LANG_NORWEGIAN": "Norsk",
            "BTN_SAVE": "Lagre",
            
            # settings/application_size.py
            "DESC_PAGE_SIZE": "App-størrelse",
            "TITLE_CHOOSE_SIZE": "Velg app-størrelse",
            "SIZE_SELECTED": "Valgt størrelse: {text} ({width}x{height})",
            "SIZE_ERROR": "❌ Feil: kunne ikke hente størrelse",

            

            
            # settings/search_sity.py
            "DESC_PAGE_SEARCH": "Søk etter by",
            "TITLE_SEARCH_CITY": "Søk etter by",
            "LABEL_COUNTRY": "Land",
            "PLACEHOLDER_COUNTRY": "Søk etter land",
            "LABEL_CITY": "By",
            "PLACEHOLDER_CITY": "Søk etter by",
            "LABEL_COORDINATES": "Koordinater",
            "PLACEHOLDER_COORDINATES": "lat, lon",
            "RESULT_COUNTRIES": "Søkeresultater for land",
            "RESULT_CITIES": "Søkeresultater",
            "LABEL_ADDED_CITIES": "Lagt til byer",
            "ERROR_CACHE_LOAD": "Feil ved lasting av buffer: {e}",
            
            # settings/settings.py
            "TITLE_SETTINGS": "Innstillinger",
            "BTN_CLOSE": "✕",
            "NAV_SEARCH_CITY": "Søk etter by",
            "NAV_APP_SIZE": "App-størrelse",
            "NAV_LANGUAGE": "App-språk",
            "NAV_IMAGE_LISTS": "Bildelister",
            "PAGE_IMAGE_LISTS": "Bildelister",
            
            # window/weather_app.py
            "WINDOW_TITLE": "Vær",
            "ERROR_UPDATE_MAP": "Feil ved oppdatering av kart: {e}",
            
            # window/search_panel.py
            "PLACEHOLDER_SEARCH": "Søk",
            "BTN_ADD_CITY": "⊕ Legg til",
            "RESULT_SEARCH": "Søkeresultater",
            
            # window/settings_panel.py
            "LABEL_SETTINGS": "Innstillinger",
            
            # card/city_info_frame.py
            "LABEL_CURRENT_POSITION": "Nåværende posisjon",
            "LABEL_TODAY": "I dag",
            "DAY_MONDAY": "Mandag",
            "DAY_TUESDAY": "Tirsdag",
            "DAY_WEDNESDAY": "Onsdag",
            "DAY_THURSDAY": "Torsdag",
            "DAY_FRIDAY": "Fredag",
            "DAY_SATURDAY": "Lørdag",
            "DAY_SUNDAY": "Søndag",
            
            # card/hourly_forecast_frame.py
            "TEXT_NOW": "Nå",
            "TEXT_SUNSET": "Solnedgang",
            "TEXT_SUNRISE": "Soloppgang",
            
            # card/twelve_hour_graph_frame.py
            "TITLE_12H_FORECAST": "12-timers varsel",
            # weather api
            "WEATHER_CLEAR_SKY": "Klart vær",
            "WEATHER_FEW_CLOUDS": "Lettskyet",
            "WEATHER_SCATTERED_CLOUDS": "Spredte skyer",
            "WEATHER_BROKEN_CLOUDS": "Delvis skyet",
            "WEATHER_OVERCAST_CLOUDS": "Overskyet",

            "WEATHER_MIST": "Tåke",
            "WEATHER_FOG": "Tett tåke",
            "WEATHER_HAZE": "Dis",
            "WEATHER_SMOKE": "Røyk",

            "WEATHER_LIGHT_RAIN": "Lett regn",
            "WEATHER_MODERATE_RAIN": "Moderat regn",
            "WEATHER_HEAVY_INTENSITY_RAIN": "Kraftig regn",
            "WEATHER_VERY_HEAVY_RAIN": "Svært kraftig regn",
            "WEATHER_EXTREME_RAIN": "Skybrudd",
            "WEATHER_FREEZING_RAIN": "Underkjølt regn",
            "WEATHER_SHOWER_RAIN": "Regnbyger",

            "WEATHER_THUNDERSTORM": "Tordenvær",
            "WEATHER_THUNDERSTORM_WITH_LIGHT_RAIN": "Tordenvær med lett regn",
            "WEATHER_THUNDERSTORM_WITH_RAIN": "Tordenvær med regn",

            "WEATHER_LIGHT_SNOW": "Lett snø",
            "WEATHER_SNOW": "Snø",
            "WEATHER_HEAVY_SNOW": "Kraftig snø",
            "WEATHER_SLEET": "Sludd",

            "WEATHER_DUST": "Støv",
            "WEATHER_SAND": "Sand",
            "WEATHER_ASH": "Aske",
            "WEATHER_SQUALL": "Vindbøy",
            "WEATHER_TORNADO": "Tornado",
        }
    }
    
    _current_language = "uk"
    _instance = None

    @classmethod
    def set_language(cls, lang_code: str):
        """Устанавливает язык и уведомляет всех подписчиков"""
        if lang_code in cls.TRANSLATIONS and lang_code != cls._current_language:
            cls._current_language = lang_code
            LANGUAGE_SIGNAL.language_changed.emit(lang_code)   # ← Используем глобальный сигнал
            return True
        return False

    @classmethod
    def get_language(cls) -> str:
        return cls._current_language

    @classmethod
    def get_text(cls, key: str, **kwargs) -> str:
        try:
            text = cls.TRANSLATIONS[cls._current_language].get(key, key)
            if kwargs:
                return text.format(**kwargs)
            return text
        except Exception as e:
            print(f"Ошибка локализации: {e}")
            return key


class AppLanguage:
    def __init__(self, parent=None):
        self.DESC_PAGE = LanguageManager.get_text("DESC_PAGE_LANGUAGE")

        LABEL_STYLE = styles.LANGUAGE_LABEL_STYLE
        TITLE_STYLE = styles.LANGUAGE_TITLE_STYLE
        COMBOBOX_STYLE = styles.LANGUAGE_COMBOBOX_STYLE
        BUTTON_STYLE = styles.LANGUAGE_BUTTON_STYLE

        # ===== КОРНЕВОЙ ВИДЖЕТ =====
        self.ROOT = widget.QWidget(parent)
        self.ROOT_LAYOUT = widget.QVBoxLayout(self.ROOT)
        self.ROOT_LAYOUT.setContentsMargins(0, 0, 0, 16)
        self.ROOT_LAYOUT.setSpacing(16)
        self.ROOT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        # ===== ЗАГОЛОВОК =====
        self.PAGE_TITLE = widget.QLabel(LanguageManager.get_text("TITLE_CHOOSE_LANGUAGE"))
        self.PAGE_TITLE.setStyleSheet(TITLE_STYLE)
        self.ROOT_LAYOUT.addWidget(self.PAGE_TITLE)

        # ===== ФОРМА =====
        self.FORM_FRAME = widget.QFrame()
        self.FORM_FRAME.setFixedWidth(SizeManager.get("lang_form_frame_width"))
        self.FORM_LAYOUT = widget.QVBoxLayout(self.FORM_FRAME)
        self.FORM_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.FORM_LAYOUT.setSpacing(6)
        self.FORM_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        lbl_lang = widget.QLabel(LanguageManager.get_text("LABEL_LANGUAGE"))
        lbl_lang.setStyleSheet(LABEL_STYLE)
        self.FORM_LAYOUT.addWidget(lbl_lang)

        self.LANGUAGE = widget.QComboBox()
        lc = SizeManager.get("lang_combo")
        self.LANGUAGE.setFixedSize(lc["width"], lc["height"])
        self.LANGUAGE.setStyleSheet(COMBOBOX_STYLE)
        self.LANGUAGE.addItems([
            LanguageManager.get_text("LANG_UKRAINIAN"),
            LanguageManager.get_text("LANG_RUSSIAN"),
            LanguageManager.get_text("LANG_ENGLISH"),
            LanguageManager.get_text("LANG_NORWEGIAN"),
        ])
        # Устанавливаем текущий язык
        lang_map = {"uk": 0, "ru": 1, "en": 2, "no": 3}
        current_index = lang_map.get(LanguageManager.get_language(), 0)
        self.LANGUAGE.setCurrentIndex(current_index)
        self.FORM_LAYOUT.addWidget(self.LANGUAGE)

        self.FORM_LAYOUT.addSpacing(12)

        self.CONFIRM_BUTTON = widget.QPushButton(LanguageManager.get_text("BTN_SAVE"))
        lcb = SizeManager.get("lang_confirm_button")
        self.CONFIRM_BUTTON.setFixedSize(lcb["width"], lcb["height"])
        self.CONFIRM_BUTTON.setStyleSheet(BUTTON_STYLE)
        self.FORM_LAYOUT.addWidget(self.CONFIRM_BUTTON)

        self.ROOT_LAYOUT.addWidget(self.FORM_FRAME)