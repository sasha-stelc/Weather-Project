import os
from datetime import datetime
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWidgets as widget

from .. import styles
from .. import styles
from ..create_path import create_media_path
from .clock_face_widget import ClockFaceWidget
from .utils import get_weather_icon_path


class CityInfoFrame(widget.QFrame):
    """Фрейм для визуального отображения информации о погоде и времени в городе.

    Компонент состоит из двух основных карточек:
    - Левая: отображает название города, текущую температуру, описание погоды и иконку.
    - Правая: отображает текущий день недели, дату и кастомный виджет аналоговых/цифровых часов.
    """

    def __init__(self, data: dict, parent=None):
        """Инициализирует виджет и настраивает графический интерфейс.

        Args:
            data (dict): Словарь с распарсенными данными погоды из API OpenWeather.
            parent (QWidget, optional): Родительский виджет. Defaults to None.
        """
        super().__init__(parent)
        self.data = data
        self.setStyleSheet(styles.CITY_INFO_FRAME)

        # Главный горизонтальный контейнер для левой и правой карточек
        self.MAIN_LAYOUT = widget.QHBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)

        # =====================================================================
        # ===== ЛЕВАЯ КАРТОЧКА (Погода) =======================================
        # =====================================================================
        self.LEFT = widget.QFrame()
        self.LEFT.setMaximumSize(390,303)
        self.LEFT.setStyleSheet(styles.CITY_INFO_CARD)

        # Иконка текущей геопозиции сверху карточки
        self.LOCATION_ICON = widget.QToolButton()
        self.LOCATION_ICON.setIcon(gui.QIcon(gui.QPixmap(create_media_path("choice_vector.png"))))
        self.LOCATION_ICON.setStyleSheet(styles.TRANSPARENT_BG)
        self.LOCATION_ICON.setFixedSize(20, 20)

        # Текстовая метка статуса позиции
        self.LOCATION_NAME = widget.QLabel("Поточна позиція")
        self.LOCATION_NAME.setStyleSheet(styles.CITY_INFO_LOCATION_NAME)
        
        # Сборка верхней строки локации
        self.TOP_LOCATION_ROW = widget.QHBoxLayout()
        self.TOP_LOCATION_ROW.setContentsMargins(16, 16, 16, 0)
        self.TOP_LOCATION_ROW.addWidget(self.LOCATION_ICON)
        self.TOP_LOCATION_ROW.addWidget(self.LOCATION_NAME)
        self.TOP_LOCATION_ROW.addStretch()

        # Разделительная линия под статусом позиции
        self.SEPARATOR = widget.QFrame()
        self.SEPARATOR.setFixedHeight(1)
        self.SEPARATOR.setStyleSheet(styles.CITY_INFO_SEPARATOR)

        self.SEPARATOR_LAYOUT = widget.QHBoxLayout()
        self.SEPARATOR_LAYOUT.setContentsMargins(16, 0, 16, 0)  
        self.SEPARATOR_LAYOUT.addWidget(self.SEPARATOR)

        # Инициализация вертикального контейнера для содержимого левой карточки
        self.LEFT_LAYOUT = widget.QVBoxLayout(self.LEFT)
        self.LEFT_LAYOUT.setSpacing(10)
        self.LEFT_LAYOUT.setContentsMargins(20, 0, 0, 20)

        # Название города
        self.CITY_LBL = widget.QLabel(data["city"])
        self.CITY_LBL.setStyleSheet(styles.CITY_INFO_CITY)

        # Текстовое описание погоды (например, "Хмарно")
        self.DESC_LBL = widget.QLabel(data["desc"])
        self.DESC_LBL.setStyleSheet(styles.CITY_INFO_DESC)

        # Минимальная и максимальная температура на сегодня
        self.MINMAX_LBL = widget.QLabel(data["minmax"])
        self.MINMAX_LBL.setStyleSheet(styles.CITY_INFO_MINMAX)

        # Иконка погоды (PNG файл, соответствующий коду от OpenWeather)
        self.ICON_LBL = widget.QLabel()
        self.ICON_LBL.setFixedSize(150, 70)
        self.ICON_LBL.setStyleSheet(styles.TRANSPARENT_BG)
        
        icon_name = data.get("icon", "") + ".png"
        icon_path = create_media_path(os.path.join("weather icon", icon_name))
        if os.path.exists(icon_path):
            self.ICON_LBL.setPixmap(gui.QPixmap(icon_path))

        # Значение текущей температуры
        self.TEMP_LBL = widget.QLabel(f"{data['temp']}°")
        self.TEMP_LBL.setStyleSheet(styles.CITY_INFO_TEMP)

        # Горизонтальный ряд для размещения иконки и температуры рядом
        self.ICON_TEMP_ROW = widget.QHBoxLayout()
        self.ICON_TEMP_ROW.setSpacing(8)
        self.ICON_TEMP_ROW.setContentsMargins(0, 0, 0, 0)
        self.ICON_TEMP_ROW.addWidget(self.ICON_LBL, alignment=core.Qt.AlignmentFlag.AlignRight)
        self.ICON_TEMP_ROW.addWidget(self.TEMP_LBL, alignment=core.Qt.AlignmentFlag.AlignLeft)

        # Выравнивание текстовых блоков по центру
        self.CITY_ROW = widget.QHBoxLayout()
        self.CITY_ROW.addWidget(self.CITY_LBL, alignment=core.Qt.AlignmentFlag.AlignCenter)

        self.DESC_ROW = widget.QHBoxLayout()
        self.DESC_ROW.addWidget(self.DESC_LBL, alignment=core.Qt.AlignmentFlag.AlignCenter)

        self.MINMAX_ROW = widget.QHBoxLayout()
        self.MINMAX_ROW.setSpacing(20)
        self.MINMAX_ROW.addStretch()
        self.MINMAX_ROW.addWidget(self.MINMAX_LBL)
        self.MINMAX_ROW.addStretch()

        # Компоновка левой карточки
        self.LEFT_LAYOUT.addLayout(self.TOP_LOCATION_ROW)      
        self.LEFT_LAYOUT.addLayout(self.SEPARATOR_LAYOUT)      
        self.LEFT_LAYOUT.addLayout(self.CITY_ROW)
        self.LEFT_LAYOUT.addLayout(self.ICON_TEMP_ROW)
        self.LEFT_LAYOUT.addLayout(self.DESC_ROW)
        self.LEFT_LAYOUT.addStretch()
        self.LEFT_LAYOUT.addLayout(self.MINMAX_ROW)

        # =====================================================================
        # ===== ПРАВАЯ КАРТОЧКА (Время и Дата) ================================
        # =====================================================================
        self.RIGHT = widget.QFrame()
        self.RIGHT.setMaximumSize(390, 303)
        self.RIGHT.setStyleSheet(styles.CITY_INFO_CARD)

        # Заголовок карточки "Сьогодні"
        self.TODAY = widget.QLabel("Сьогодні")
        self.TODAY.setStyleSheet(styles.CITY_INFO_DAY_TITLE)

        # Метка для дня недели
        self.DAY_LBL = widget.QLabel()
        self.DAY_LBL.setStyleSheet(styles.CITY_INFO_DAY)

        # Метка для календарной даты
        self.DATE_LBL = widget.QLabel()
        self.DATE_LBL.setStyleSheet(styles.CITY_INFO_DATE)

        self.TODAY_ROW = widget.QHBoxLayout()
        self.TODAY_ROW.setContentsMargins(24, 16, 24, 8)
        self.TODAY_ROW.addWidget(self.TODAY)

        # Разделительная линия правой карточки
        self.RIGHT_SEPARATOR = widget.QFrame()
        self.RIGHT_SEPARATOR.setFixedHeight(1)
        self.RIGHT_SEPARATOR.setStyleSheet(styles.CITY_INFO_SEPARATOR)

        self.RIGHT_SEPARATOR_LAYOUT = widget.QHBoxLayout()
        self.RIGHT_SEPARATOR_LAYOUT.setContentsMargins(24, 0, 24, 0)
        self.RIGHT_SEPARATOR_LAYOUT.addWidget(self.RIGHT_SEPARATOR)

        # Строка для размещения Дня недели и Даты по краям
        self.DAY_DATE_ROW = widget.QHBoxLayout()
        self.DAY_DATE_ROW.setContentsMargins(24, 12, 24, 0)
        self.DAY_DATE_ROW.addWidget(self.DAY_LBL)
        self.DAY_DATE_ROW.addStretch()
        self.DAY_DATE_ROW.addWidget(self.DATE_LBL)
        
        # === БЛОК ЧАСОВ ===
        X = 160  
        Y = 160

        # Контейнер для наложения цифрового времени поверх графического циферблата
        self.CLOCK_CONTAINER = widget.QWidget()
        self.CLOCK_CONTAINER.setFixedSize(X, Y)
        self.CLOCK_CONTAINER.setStyleSheet(styles.CLOCK_CONTAINER_STYLE)

        # Отрисованный кастомный виджет заднего фона часов
        self.CLOCK_BG = ClockFaceWidget(self.CLOCK_CONTAINER)
        self.CLOCK_BG.setFixedSize(X, Y)

        # Текстовое цифровое время (отображается по центру контейнера поверх циферблата)
        self.CLOCK_LBL = widget.QLabel(self.CLOCK_CONTAINER)
        self.CLOCK_LBL.setFixedSize(X, Y)
        self.CLOCK_LBL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.CLOCK_LBL.setStyleSheet(styles.CLOCK_LABEL_STYLE)

        # Вертикальная компоновка правой карточки
        self.RIGHT_LAYOUT = widget.QVBoxLayout(self.RIGHT)
        self.RIGHT_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.RIGHT_LAYOUT.setSpacing(0)
        
        self.RIGHT_LAYOUT.addLayout(self.TODAY_ROW)
        self.RIGHT_LAYOUT.addLayout(self.RIGHT_SEPARATOR_LAYOUT)
        self.RIGHT_LAYOUT.addLayout(self.DAY_DATE_ROW)
        
        self.RIGHT_LAYOUT.addSpacing(15) 
        self.RIGHT_LAYOUT.addWidget(self.CLOCK_CONTAINER, alignment=core.Qt.AlignmentFlag.AlignHCenter | core.Qt.AlignmentFlag.AlignTop)
        self.RIGHT_LAYOUT.addStretch()

        # Добавление обеих карточек в главный горизонтальный слой фрейма
        self.MAIN_LAYOUT.addWidget(self.LEFT)
        self.MAIN_LAYOUT.addWidget(self.RIGHT)

        # === ТАЙМЕР ОБНОВЛЕНИЯ ВРЕМЕНИ ===
        # Извлекаем объект временной зоны ("tz"), сформированный в get_weather
        self.TZ = data.get("tz")
        self.TIMER = core.QTimer(self)
        self.TIMER.timeout.connect(self.UPDATE_TIME)
        
        # Запуск таймера с интервалом в 60 секунд (1 минута)
        self.TIMER.start(60 * 1000)
        
        # Первичный вызов для мгновенного отображения времени при рендере виджета
        self.UPDATE_TIME()

    def UPDATE_TIME(self):
        """Обновляет текстовые метки дня недели, даты и текущего времени.

        Учитывает индивидуальную часовую зону целевого города (self.TZ).
        Вызывается каждую минуту по сигналу таймера QTimer.
        """
        # Получаем текущее время с учетом таймзоны города или системное время
        now = datetime.now(self.TZ) if self.TZ else datetime.now()
        
        # Массив украинских названий дней недели
        days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]
        
        # Обновление интерфейсных текстовых полей
        self.DAY_LBL.setText(days[now.weekday()])
        self.DATE_LBL.setText(now.strftime("%d.%m.%Y"))
        self.CLOCK_LBL.setText(now.strftime("%H:%M"))
