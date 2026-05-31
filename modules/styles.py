"""Модуль конфигурации стилей (QSS) приложения погоды.

Содержит шаблонизированные таблицы стилей (Qt Style Sheets), CSS-свойства для 
текстовых меток, параметры градиентных заливок панелей и специфические отступы 
для реализации аппаратного эффекта переключения дневной/ночной темы оформления.
"""

# =====================================================================
# ==================== СТИЛИ КАРТОЧЕК ПОГОДЫ ==========================
# =====================================================================

# Шаблон QSS для активной карточки текущего местоположения (избранного города)
# Двойные фигурные скобки {{ }} используются для экранирования, чтобы метод .format() 
# не путал их с синтаксисом Python, а подставлял только значение {bg}
CURRENT_CARD = """
    WeatherCard {{
        background-color: {bg};  /* Динамический цвет подложки с альфа-каналом прозрачности */
        border-radius: 15px;      /* Скругление всех углов карточки */
    }}
    /* Каскадный селектор: сбрасывает фон у всех текстовых меток внутри этой карточки,
       чтобы они не перекрывали своими прямоугольными границами подложку карточки */
    QLabel {{ 
        color: white; 
        background: transparent; 
    }}
"""

# Шаблон QSS для стандартных карточек городов в боковом списке
DEFAULT_CARD = """
    WeatherCard {{
        background-color: {bg};        /* Меняется transparent -> rgba при Hover-эффекте */
        border-bottom: 1px solid {border}; /* Тонкая разделительная линия снизу карточки */
        border-radius: {radius}         /* Становится 10px при наведении для красивого эффекта */
    }}
    QLabel {{ 
        color: white; 
        background: transparent; 
        border: none;                  /* Гарантирует отсутствие рамок у текста */
    }}
"""


# =====================================================================
# ==================== ТЕКСТОВЫЕ МЕТКИ (Типографика) ===================
# =====================================================================
# Строки CSS-свойств, передаваемые напрямую в метод setStyleSheet() текстовых лейблов.
# Настройка шрифта: используется гарнитура 'Medium' с явным указанием веса (bold/semi-bold).

CITY_LABEL = "font-family: Medium; font-size: 24px; font-weight: 700"    # Крупный жирный шрифт города
TIME_LABEL = "font-family: Medium; font-size: 12px; font-weight: 500"    # Мелкое аккуратное время
TEMP_LABEL = "font-family: Medium; font-size: 42px; font-weight: 500"    # Огромный индикатор градусов
DESC_LABEL = "font-family: Medium; font-size: 12px; font-weight: 500"    # Текст состояния погоды
MINMAX_LABEL = "font-family: Medium; font-size: 12px; font-weight: 500"  # Текст экстремумов суток


# =====================================================================
# ==================== СТИЛИ ПАНЕЛЕЙ И ФОНОВ =========================
# =====================================================================

# Контейнер поисковой строки (сверху списка городов)
SEARCH_FRAME = """
    QFrame { 
        background: transparent; /* Полностью прозрачный фон для чистого наложения */
    }   
"""

# Главная подложка всего окна приложения с использованием линейного градиента.
# Идентификатор #centralWidget гарантирует, что стиль применится строго к самому 
# окну, не ломая стили дочерних элементов (кнопок, меток), находящихся внутри.
CENTRAL_WIDGET = """
    QWidget#centralWidget {
        border-radius: 15px; /* Скругление углов главного окна (актуально для Frameless-окон) */
        
        /* Двухточечный диагональный линейный градиент (из левого нижнего угла в правый верхний):
           x1:0, y1:1 -> Левый нижний угол
           x2:1, y2:0 -> Правый верхний угол */
        background: qlineargradient(
            x1: 0, y1: 1,
            x2: 1, y2: 0,
            stop: 0 rgba(135, 206, 250, 1),  /* Нежно-голубой цвет (Light Sky Blue) в начале */
            stop: 1 rgba(255, 223, 86, 1)    /* Солнечно-желтый цвет в конце градиента */
        );
    }
"""

# Боковая левая панель (контейнер для списка городов)
LEFT_PANEL = """
    QFrame {
        background: rgba(0, 0, 0, 0.2); /* Единая полупрозрачная затемненная шторка */
        border: none;                   /* Убираем дефолтные рамки QFrame */
    }
"""

# Правая панель (основная область детального прогноза и графиков)
RIGHT_PANEL = """
    QFrame {
        border: none; /* Прозрачный холст, контент рисуется прямо поверх главного градиента */
    }
"""

# Общие вспомогательные стили
TRANSPARENT_BG = "background-color: transparent;"
TRANSPARENT_NO_BORDER = "background: transparent; border: none;"
LIGHT_THEME_CENTRAL = "background: rgba(255, 255, 200, 1);"
LIGHT_THEME_RIGHT_PANEL = "QFrame { background: rgba(255, 223, 86, 0.3); border: none; }"

TITLE_BAR = "background: transparent; border-top-left-radius: 20px; border-top-right-radius: 20px;"
SETTINGS_FRAME = "background-color: rgba(0, 0, 0, 0);"
SETTINGS_BOX = "background-color: rgba(0, 0, 0, 0.50); border-radius: 15px;"
SETTINGS_BUTTON = "background: transparent; border: none;"
SETTINGS_LABEL = "color: white; font-size: 14px; font-weight: 500;"
TITLE_BAR_BUTTONS = "QToolButton { background: transparent; border: none; }"

ADD_CITY_BUTTON = """
    QPushButton {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 500;
        border: none;
        padding: 0 10px;
    }
    QPushButton:hover {
        background: rgba(255, 255, 255, 0.25);
    }
"""

SEARCH_CONTAINER = """
    QFrame {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        border: none;
    }
"""

CITY_SEARCH = """
    QLineEdit {
        background: transparent;
        color: white;
        font-size: 14px;
        border: none;
    }
"""

SEARCH_DROPDOWN = """
    QFrame {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
"""

DROPDOWN_TITLE = "color: rgba(255,255,255,0.5); font-size: 12px; background: transparent; border: none;"
DROPDOWN_LIST = """
    QListWidget {
        background: transparent;
        color: white;
        font-size: 15px;
        border: none;
        outline: none;
    }
    QListWidget::item {
        padding: 10px 4px;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        border-radius: 0px;
    }
    QListWidget::item:last-child {
        border-bottom: none;
    }
    QListWidget::item:hover {
        background: rgba(255, 255, 255, 0.08);
    }
    QListWidget::item:selected {
        background: rgba(255, 255, 255, 0.12);
    }
    QScrollBar:vertical {
        width: 3px;
        background: transparent;
    }
    QScrollBar::handle:vertical {
        background: rgba(255,255,255,0.2);
        border-radius: 1px;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical { height: 0px; }
"""

CITY_INFO_FRAME = "background: transparent;"
CITY_INFO_CARD = "background: rgba(0, 0, 0, 0.2); border-radius: 20px; border: none;"
CITY_INFO_LOCATION_NAME = "font-size: 16px; color: white; background: transparent;"
CITY_INFO_SEPARATOR = "background: rgba(255, 255, 255, 0.25); border: none;"
CITY_INFO_CITY = "font-size: 44px; color: white; font-weight: 500; background: transparent;"
CITY_INFO_DESC = "color: white; font-size: 24px; font-weight: 500; background: transparent;"
CITY_INFO_MINMAX = "color: rgba(255,255,255,180); font-size: 16px; border: none; background: transparent;"
CITY_INFO_TEMP = "font-size: 52px; color: white; font-weight: 500; border: none; background: transparent;"
CITY_INFO_DAY_TITLE = "font-size: 16px; color: white; font-weight: 500; background: transparent;"
CITY_INFO_DAY = "color: white; font-size: 24px; font-weight: 500; background: transparent;"
CITY_INFO_DATE = "color: rgba(255,255,255,0.85); font-size: 24px; font-weight: 500; background: transparent;"
CLOCK_CONTAINER_STYLE = "background: transparent;"
CLOCK_LABEL_STYLE = "background: transparent; font-size: 34px; color: white; font-weight: 500;"

HOURLY_FORECAST_FRAME = "background: rgba(0, 0, 0, 0.2); border-radius: 20px;"
HOURLY_TITLE = "font-size: 14px; color: white; font-weight: 500; background: transparent;"
HOURLY_LINE = "background: rgba(255,255,255,0.2);"
HOURLY_ARROW_BUTTON = "background: transparent; border: none;"
HOURLY_ARROW_TEXT = "color: rgba(255,255,255,150); font-size: 14px; background: transparent; border: none;"
HOURLY_ITEM_TIME = "color: white; font-size: 14px; font-weight: 600; background: transparent;"
HOURLY_ITEM_TEMP = "color: white; font-size: 14px; font-weight: 500; background: transparent;"

TWELVE_HOUR_FRAME = """
    TwelveHourGraphFrame {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 20px;
        
    }
"""
TWELVE_HOUR_TITLE = "font-size: 13px; color: white; font-weight: 500;; background: transparent; opacity: 0.8;"

# Настройки окна
SETTINGS_MAIN = "background: rgba(0, 0, 0, 85%);"
SETTINGS_TOP_BAR = "background: transparent; border: none;"
SETTINGS_TITLE = "color: white; font-size: 18px; font-weight: 600; background: transparent;"
SETTINGS_CLOSE_BUTTON = """
    QPushButton {
        background-color: transparent;
        color: rgba(255, 255, 255, 0.6);
        border: none;
        font-size: 16px;
    }
    QPushButton:hover {
        color: white;
    }
"""
SETTINGS_LEFT_FRAME = """
    QFrame {
        background: transparent;
        border-right: 1px solid rgba(255, 255, 255, 0.12);
    }
"""
SETTINGS_RIGHT_FRAME = "background: transparent; border: none;"
SETTINGS_PAGE_TITLE = "color: white; font-size: 20px; font-weight: 600; background: transparent;"

# =====================================================================
# ==================== СТИЛІ СТОРІНКИ НАЛАШТУВАНЬ ======================
# =====================================================================

LANGUAGE_TITLE_STYLE = """
    QLabel {
        color: #ffffff;
        font-size: 18px;
        font-weight: 500;
        padding-bottom: 4px;
    }
"""

LANGUAGE_LABEL_STYLE = """
    QLabel {
        color: #aaaaaa;
        font-size: 13px;
        background: transparent;
    }
"""

LANGUAGE_COMBOBOX_STYLE = """
    QComboBox {
        background-color: #2b2b2b;
        color: #cccccc;
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 13px;
    }
    QComboBox:hover {
        border: 1px solid #555;
    }
    QComboBox::drop-down {
        border: none;
        width: 24px;
    }
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #888;
        width: 0;
        height: 0;
        margin-right: 8px;
    }
    QComboBox QAbstractItemView {
        background-color: #2b2b2b;
        color: #cccccc;
        border: 1px solid #3a3a3a;
        selection-background-color: #3a3a3a;
        outline: none;
    }
"""

LANGUAGE_BUTTON_STYLE = """
    QPushButton {
        background-color: #3a3a3a;
        color: #aaaaaa;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 500
    }
    QPushButton:hover {
        background-color: #444;
        color: #cccccc;
    }
    QPushButton:pressed {
        background-color: #333;
    }
"""

APPLICATION_TITLE_STYLE = """
    QLabel {
        color: #ffffff;
        font-size: 18px;
        font-weight: 500;
        padding-bottom: 4px;
        background: transparent;
    }
"""

APPLICATION_RADIO_STYLE = """
    QRadioButton {
        color: #cccccc;
        font-size: 14px;
        spacing: 10px;
        background: transparent;
    }
    QRadioButton::indicator {
        width: 16px;
        height: 16px;
        border-radius: 9px;
        border: 2px solid #666666;
        background-color: transparent;
    }
    QRadioButton::indicator:hover {
        border: 2px solid #aaaaaa;
    }
    QRadioButton::indicator:checked {
        background-color: #ffffff;
        border: 4px solid #1a1a1a;
        outline: 2px solid #ffffff;
    }
"""

APPLICATION_BUTTON_STYLE = LANGUAGE_BUTTON_STYLE

SEARCH_TITLE_STYLE = APPLICATION_TITLE_STYLE

SEARCH_LABEL_STYLE = LANGUAGE_LABEL_STYLE

SEARCH_COMBOBOX_STYLE = """
    QComboBox {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 14px;
        font-weight: 500
    }
    QComboBox:hover {
        border: 1px solid #555;
    }
    QComboBox::drop-down {
        border: none;
        width: 24px;
    }
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #888;
        width: 0;
        height: 0;
        margin-right: 8px;
    }
    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #3a3a3a;
        selection-background-color: #eeeeee;
        outline: none;
    }
"""

SEARCH_LINEEDIT_STYLE = """
    QLineEdit {
        background-color: #ffffff;
        color: #222222;
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 14px;
        font-weight: 500
    }
    QLineEdit:hover {
        border: 1px solid #555;
    }
    QLineEdit:focus {
        border: 1px solid #666;
    }
"""

SEARCH_BUTTON_STYLE = LANGUAGE_BUTTON_STYLE

SEARCH_MAP_PLACEHOLDER_STYLE = """
    QLabel {
        background-color: #2a2a2a;
        border-radius: 6px;
        border: 1px solid #3a3a3a;
    }
"""

SEARCH_ADDED_LABEL_STYLE = SEARCH_TITLE_STYLE

SEARCH_CITIES_LIST_STYLE = """
    QFrame {
        background-color: #232323;
        border-radius: 8px;
        border: 1px solid #333;
    }
"""

SEARCH_CITY_ROW_STYLE = """
    QFrame {
        background-color: transparent;
        border: none;
        border-bottom: 1px solid #2e2e2e;
    }
"""

SEARCH_CITY_LABEL_STYLE = """
    QLabel {
        color: #cccccc;
        font-size: 14px;
        background: transparent;
        border: none;
    }
"""

SEARCH_DELETE_BUTTON_STYLE = """
    QPushButton {
        color: #555;
        background: transparent;
        border: none;
        font-size: 15px;
    }
    QPushButton:hover {
        color: #ff5555;
    }
"""

NAV_BUTTON_CHECKED = """
    QPushButton {
        background-color: rgba(255, 255, 255, 0.15);
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 500;
        text-align: left;
        padding-left: 12px;
    }
"""
NAV_BUTTON_UNCHECKED = """
    QPushButton {
        background-color: transparent;
        color: rgba(255, 255, 255, 0.45);
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 400;
        text-align: left;
        padding-left: 12px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 0.07);
        color: rgba(255, 255, 255, 0.75);
    }
"""

# Область прокрутки списка городов
SCROLL_AREA = "background: transparent; border: none;"

# Внутренний контейнер, в который физически укладываются экземпляры WeatherCard
CARDS_CONTAINER = "background: transparent;"


# =====================================================================
# ==================== КНОПКА ПЕРЕКЛЮЧЕНИЯ ТЕМЫ =======================
# =====================================================================
# Интересное архитектурное решение: переключатель сделан в виде ОДНОЙ кнопки QPushButton.
# Имитация движения тумблера (слайдера) влево-вправо достигается за счет резкого 
# изменения внутреннего пространства (padding-left и padding-right).

# Состояние "Дневная тема" (Иконка солнца слева, свободное место справа)
THEME_BUTTON_SUN = """
    QPushButton {
        background-color: rgba(0, 0, 0, 0.2); /* Темная полупрозрачная подложка */
        border-radius: 12px;                  /* Скругление под форму пилюли/капсулы */
        padding-left: 3px;                    /* Прижимает иконку солнца к левому краю */
        padding-right: 31px;                  /* Резервирует пустое место справа */
    }
"""

# Состояние "Ночная тема" (Иконка луны сдвигается вправо, освобождая место слева)
THEME_BUTTON_MOON = """
    QPushButton {
        background-color: rgba(236, 236, 236, 1); /* Контрастный плотный светло-серый фон */
        border-radius: 12px;
        padding-left: 31px;                   /* Выталкивает иконку луны к правому краю */
        padding-right: 3px;                    /* Минимальный зазор от правого края */
    }
"""
