import os
from datetime import datetime
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWidgets as widget
from ..settings.langueges import LanguageManager, LANGUAGE_SIGNAL   # ← добавь LANGUAGE_SIGNAL
from .. import styles
from ..create_path import create_media_path
from ..settings.langueges import LanguageManager
from ..settings.size_config import SizeManager
from .clock_face_widget import ClockFaceWidget


class CityInfoFrame(widget.QFrame):
    """Фрейм для визуального отображения информации о погоде и времени в городе."""

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self.setStyleSheet(styles.CITY_INFO_FRAME)

        # Главный горизонтальный контейнер
        self.MAIN_LAYOUT = widget.QHBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)

        # ==================== ЛЕВАЯ КАРТОЧКА ====================
        self.LEFT = widget.QFrame()
        lm = SizeManager.get("city_info_left_max")
        self.LEFT.setMaximumSize(lm["width"], lm["height"])
        self.LEFT.setStyleSheet(styles.CITY_INFO_CARD)

        self.LOCATION_ICON = widget.QToolButton()
        self.LOCATION_ICON.setIcon(gui.QIcon(gui.QPixmap(create_media_path("choice_vector.png"))))
        self.LOCATION_ICON.setStyleSheet(styles.TRANSPARENT_BG)
        li = SizeManager.get("city_info_location_icon")
        self.LOCATION_ICON.setFixedSize(li["width"], li["height"])

        self.LOCATION_NAME = widget.QLabel()
        self.LOCATION_NAME.setStyleSheet(styles.CITY_INFO_LOCATION_NAME)

        self.TOP_LOCATION_ROW = widget.QHBoxLayout()
        self.TOP_LOCATION_ROW.setContentsMargins(16, 16, 16, 0)
        self.TOP_LOCATION_ROW.addWidget(self.LOCATION_ICON)
        self.TOP_LOCATION_ROW.addWidget(self.LOCATION_NAME)
        self.TOP_LOCATION_ROW.addStretch()

        self.SEPARATOR = widget.QFrame()
        self.SEPARATOR.setFixedHeight(SizeManager.get("city_info_separator_height"))
        self.SEPARATOR.setStyleSheet(styles.CITY_INFO_SEPARATOR)

        self.SEPARATOR_LAYOUT = widget.QHBoxLayout()
        self.SEPARATOR_LAYOUT.setContentsMargins(16, 0, 16, 0)
        self.SEPARATOR_LAYOUT.addWidget(self.SEPARATOR)

        self.LEFT_LAYOUT = widget.QVBoxLayout(self.LEFT)
        self.LEFT_LAYOUT.setSpacing(10)
        self.LEFT_LAYOUT.setContentsMargins(20, 0, 0, 20)

        self.CITY_LBL = widget.QLabel(data.get("city_display", data["city"]))
        self.CITY_LBL.setStyleSheet(styles.CITY_INFO_CITY)

        self.DESC_LBL = widget.QLabel(data["desc"])
        self.DESC_LBL.setStyleSheet(styles.CITY_INFO_DESC)

        self.MINMAX_LBL = widget.QLabel(data["minmax"])
        self.MINMAX_LBL.setStyleSheet(styles.CITY_INFO_MINMAX)

        # Иконка погоды
        self.ICON_LBL = widget.QLabel()
        wil = SizeManager.get("city_info_icon_lbl")
        self.ICON_LBL.setFixedSize(wil["width"], wil["height"])
        self.ICON_LBL.setStyleSheet(styles.TRANSPARENT_BG)
        
        icon_name = data.get("icon", "") + ".png"

        # берём выбранную пользователем тему — это имя папки внутри media/,
        # а не готовый абсолютный путь
        selected_theme = core.QSettings("WeatherProject", "WeatherApp").value(
            "selected_theme",
            "weather icon"
        )

        icon_folder = create_media_path(selected_theme)

        icon_path = os.path.join(icon_folder, icon_name)

        if os.path.exists(icon_path):
            self.ICON_LBL.setPixmap(gui.QPixmap(icon_path))
        self.TEMP_LBL = widget.QLabel(f"{data['temp']}°")
        self.TEMP_LBL.setStyleSheet(styles.CITY_INFO_TEMP)

        self.ICON_TEMP_ROW = widget.QHBoxLayout()
        self.ICON_TEMP_ROW.setSpacing(8)
        self.ICON_TEMP_ROW.addWidget(self.ICON_LBL, alignment=core.Qt.AlignmentFlag.AlignRight)
        self.ICON_TEMP_ROW.addWidget(self.TEMP_LBL, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.CITY_ROW = widget.QHBoxLayout()
        self.CITY_ROW.addWidget(self.CITY_LBL, alignment=core.Qt.AlignmentFlag.AlignCenter)

        self.DESC_ROW = widget.QHBoxLayout()
        self.DESC_ROW.addWidget(self.DESC_LBL, alignment=core.Qt.AlignmentFlag.AlignCenter)

        self.MINMAX_ROW = widget.QHBoxLayout()
        self.MINMAX_ROW.setSpacing(20)
        self.MINMAX_ROW.addStretch()
        self.MINMAX_ROW.addWidget(self.MINMAX_LBL)
        self.MINMAX_ROW.addStretch()

        self.LEFT_LAYOUT.addLayout(self.TOP_LOCATION_ROW)
        self.LEFT_LAYOUT.addLayout(self.SEPARATOR_LAYOUT)
        self.LEFT_LAYOUT.addLayout(self.CITY_ROW)
        self.LEFT_LAYOUT.addLayout(self.ICON_TEMP_ROW)
        self.LEFT_LAYOUT.addLayout(self.DESC_ROW)
        self.LEFT_LAYOUT.addStretch()
        self.LEFT_LAYOUT.addLayout(self.MINMAX_ROW)

        # ==================== ПРАВАЯ КАРТОЧКА ====================
        self.RIGHT = widget.QFrame()
        rm = SizeManager.get("city_info_right_max")
        self.RIGHT.setMaximumSize(rm["width"], rm["height"])
        self.RIGHT.setStyleSheet(styles.CITY_INFO_CARD)

        self.TODAY = widget.QLabel()
        self.TODAY.setStyleSheet(styles.CITY_INFO_DAY_TITLE)

        self.DAY_LBL = widget.QLabel()
        self.DAY_LBL.setStyleSheet(styles.CITY_INFO_DAY)

        self.DATE_LBL = widget.QLabel()
        self.DATE_LBL.setStyleSheet(styles.CITY_INFO_DATE)

        self.TODAY_ROW = widget.QHBoxLayout()
        self.TODAY_ROW.setContentsMargins(24, 16, 24, 8)
        self.TODAY_ROW.addWidget(self.TODAY)

        self.RIGHT_SEPARATOR = widget.QFrame()
        self.RIGHT_SEPARATOR.setFixedHeight(SizeManager.get("city_info_right_separator_height"))
        self.RIGHT_SEPARATOR.setStyleSheet(styles.CITY_INFO_SEPARATOR)

        self.RIGHT_SEPARATOR_LAYOUT = widget.QHBoxLayout()
        self.RIGHT_SEPARATOR_LAYOUT.setContentsMargins(24, 0, 24, 0)
        self.RIGHT_SEPARATOR_LAYOUT.addWidget(self.RIGHT_SEPARATOR)

        self.DAY_DATE_ROW = widget.QHBoxLayout()
        self.DAY_DATE_ROW.setContentsMargins(24, 12, 24, 0)
        self.DAY_DATE_ROW.addWidget(self.DAY_LBL)
        self.DAY_DATE_ROW.addStretch()
        self.DAY_DATE_ROW.addWidget(self.DATE_LBL)

        # Часы
        clock = SizeManager.get("clock_widget")
        X = clock["width"]
        Y = clock["height"]
        self.CLOCK_CONTAINER = widget.QWidget()
        self.CLOCK_CONTAINER.setFixedSize(X, Y)
        self.CLOCK_CONTAINER.setStyleSheet(styles.CLOCK_CONTAINER_STYLE)

        self.CLOCK_BG = ClockFaceWidget(self.CLOCK_CONTAINER)
        self.CLOCK_BG.setFixedSize(X, Y)

        self.CLOCK_LBL = widget.QLabel(self.CLOCK_CONTAINER)
        self.CLOCK_LBL.setFixedSize(X, Y)
        self.CLOCK_LBL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.CLOCK_LBL.setStyleSheet(styles.CLOCK_LABEL_STYLE)

        self.RIGHT_LAYOUT = widget.QVBoxLayout(self.RIGHT)
        self.RIGHT_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.RIGHT_LAYOUT.setSpacing(0)
        
        self.RIGHT_LAYOUT.addLayout(self.TODAY_ROW)
        self.RIGHT_LAYOUT.addLayout(self.RIGHT_SEPARATOR_LAYOUT)
        self.RIGHT_LAYOUT.addLayout(self.DAY_DATE_ROW)
        self.RIGHT_LAYOUT.addSpacing(15)
        self.RIGHT_LAYOUT.addWidget(self.CLOCK_CONTAINER, 
                                  alignment=core.Qt.AlignmentFlag.AlignHCenter | core.Qt.AlignmentFlag.AlignTop)
        self.RIGHT_LAYOUT.addStretch()

        self.MAIN_LAYOUT.addWidget(self.LEFT)
        self.MAIN_LAYOUT.addWidget(self.RIGHT)

        # ==================== Таймер и переводы ====================
        self.TZ = data.get("tz")
        self.TIMER = core.QTimer(self)
        self.TIMER.timeout.connect(self.UPDATE_TIME)
        self.TIMER.start(60 * 1000)

        # Подключаем сигнал смены языка
        LANGUAGE_SIGNAL.language_changed.connect(self.retranslate)       
        self.retranslate()
        self.UPDATE_TIME()

    def UPDATE_TIME(self):
        """Обновляет время, дату и день недели"""
        now = datetime.now(self.TZ) if self.TZ else datetime.now()

        days = [
            LanguageManager.get_text("DAY_MONDAY"),
            LanguageManager.get_text("DAY_TUESDAY"),
            LanguageManager.get_text("DAY_WEDNESDAY"),
            LanguageManager.get_text("DAY_THURSDAY"),
            LanguageManager.get_text("DAY_FRIDAY"),
            LanguageManager.get_text("DAY_SATURDAY"),
            LanguageManager.get_text("DAY_SUNDAY"),
        ]

        self.DAY_LBL.setText(days[now.weekday()])
        self.DATE_LBL.setText(now.strftime("%d.%m.%Y"))
        self.CLOCK_LBL.setText(now.strftime("%H:%M"))

    def retranslate(self, lang=None):
        """Обновляет все переводимые строки при смене языка"""
        self.LOCATION_NAME.setText(LanguageManager.get_text("LABEL_CURRENT_POSITION"))
        self.TODAY.setText(LanguageManager.get_text("LABEL_TODAY"))
        
        # Обновляем день недели сразу
        self.UPDATE_TIME()