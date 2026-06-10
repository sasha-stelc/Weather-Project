import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
from .. import styles
import json
import os

# ===== СИСТЕМА ЛОКАЛИЗАЦИИ =====
class LanguageManager:
    """Глобальный менеджер языков для приложения"""
    
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
            "BTN_SAVE": "Зберегти",
            
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
        },
        
        "ru": {  # Русский
            # settings/langueges.py
            "DESC_PAGE_LANGUAGE": "Язык приложения",
            "TITLE_CHOOSE_LANGUAGE": "Выберите язык приложения",
            "LABEL_LANGUAGE": "Язык приложения",
            "LANG_UKRAINIAN": "Українська",
            "LANG_RUSSIAN": "Русский",
            "LANG_ENGLISH": "English",
            "BTN_SAVE": "Сохранить",
            
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
        },
        
        "en": {  # English
            # settings/langueges.py
            "DESC_PAGE_LANGUAGE": "Application Language",
            "TITLE_CHOOSE_LANGUAGE": "Choose Application Language",
            "LABEL_LANGUAGE": "Application Language",
            "LANG_UKRAINIAN": "Українська",
            "LANG_RUSSIAN": "Русский",
            "LANG_ENGLISH": "English",
            "BTN_SAVE": "Save",
            
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
        }
    }
    
    # Текущий активный язык (по умолчанию украинский)
    _current_language = "uk"
    
    @classmethod
    def set_language(cls, lang_code: str):
        """Устанавливает текущий язык"""
        if lang_code in cls.TRANSLATIONS:
            cls._current_language = lang_code
            return True
        return False
    
    @classmethod
    def get_language(cls) -> str:
        """Получает текущий язык"""
        return cls._current_language
    
    @classmethod
    def get_text(cls, key: str, **kwargs) -> str:
        """Получает переведённый текст по ключу
        
        Args:
            key: Ключ текста в словаре переводов
            **kwargs: Параметры для форматирования строки
        
        Returns:
            Переведённый текст или ключ если не найден
        """
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
        self.FORM_FRAME.setFixedWidth(239)
        self.FORM_LAYOUT = widget.QVBoxLayout(self.FORM_FRAME)
        self.FORM_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.FORM_LAYOUT.setSpacing(6)
        self.FORM_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        lbl_lang = widget.QLabel(LanguageManager.get_text("LABEL_LANGUAGE"))
        lbl_lang.setStyleSheet(LABEL_STYLE)
        self.FORM_LAYOUT.addWidget(lbl_lang)

        self.LANGUAGE = widget.QComboBox()
        self.LANGUAGE.setFixedSize(239, 32)
        self.LANGUAGE.setStyleSheet(COMBOBOX_STYLE)
        self.LANGUAGE.addItems([
            LanguageManager.get_text("LANG_UKRAINIAN"),
            LanguageManager.get_text("LANG_RUSSIAN"),
            LanguageManager.get_text("LANG_ENGLISH"),
        ])
        # Устанавливаем текущий язык
        lang_map = {"uk": 0, "ru": 1, "en": 2}
        current_index = lang_map.get(LanguageManager.get_language(), 0)
        self.LANGUAGE.setCurrentIndex(current_index)
        self.FORM_LAYOUT.addWidget(self.LANGUAGE)

        self.FORM_LAYOUT.addSpacing(12)

        self.CONFIRM_BUTTON = widget.QPushButton(LanguageManager.get_text("BTN_SAVE"))
        self.CONFIRM_BUTTON.setFixedSize(105, 38)
        self.CONFIRM_BUTTON.setStyleSheet(BUTTON_STYLE)
        self.FORM_LAYOUT.addWidget(self.CONFIRM_BUTTON)

        self.ROOT_LAYOUT.addWidget(self.FORM_FRAME)