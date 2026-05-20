import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from datetime import datetime

from .. import styles
from ..create_path import create_media_path
from .clock_face_widget import ClockFaceWidget
from .utils import get_weather_icon_path


class CityInfoFrame(widget.QFrame):
    "Фрейм с информацией о погоде в городе (основная карточка)"
    
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.DATA = data
        self.setStyleSheet("background: transparent;")
   

        self.MAIN_LAYOUT = widget.QHBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)

        # ===== ЛЕВАЯ КАРТОЧКА погода =====
        self.LEFT = widget.QFrame()
        self.LEFT.setFixedSize(390, 303)
        self.LEFT.setStyleSheet("background: rgba(0, 0, 0, 0.2); border-radius: 20px;border: none;")

        self.LOCATION_ICON = widget.QToolButton()
        self.LOCATION_ICON.setIcon(gui.QIcon(gui.QPixmap(create_media_path("choice_vector.png"))))
        self.LOCATION_ICON.setStyleSheet("background: transparent;")
        self.LOCATION_ICON.setFixedSize(20, 20)

        self.LOCATION_NAME = widget.QLabel("Поточна позиція")
        self.LOCATION_NAME.setStyleSheet("font-size: 16px; color: white; background: transparent;")
        
        # Лейаут для Поточна позиція сверху слева
        self.TOP_LOCATION_ROW = widget.QHBoxLayout()
        self.TOP_LOCATION_ROW.setContentsMargins(16, 16, 16, 0)
        self.TOP_LOCATION_ROW.addWidget(self.LOCATION_ICON)
        self.TOP_LOCATION_ROW.addWidget(self.LOCATION_NAME)
        self.TOP_LOCATION_ROW.addStretch()

       
        self.SEPARATOR = widget.QFrame()
        self.SEPARATOR.setFixedHeight(1)
        self.SEPARATOR.setStyleSheet("background: rgba(255, 255, 255, 0.25); border: none;")

        self.SEPARATOR_LAYOUT = widget.QHBoxLayout()
        self.SEPARATOR_LAYOUT.setContentsMargins(16, 0, 16, 0)  
        self.SEPARATOR_LAYOUT.addWidget(self.SEPARATOR)

        self.LEFT_LAYOUT = widget.QVBoxLayout(self.LEFT)
        self.LEFT_LAYOUT.setSpacing(10)
        self.LEFT_LAYOUT.setContentsMargins(20, 0, 0, 20)

        self.CITY_LBL = widget.QLabel(data["city"])
        self.CITY_LBL.setStyleSheet("font-size: 44px; color: white; font-weight: 500; background: transparent;")

        self.DESC_LBL = widget.QLabel(data["desc"])
        self.DESC_LBL.setStyleSheet("color: white; font-size: 24px; font-weight: 500; background: transparent;")

        self.MINMAX_LBL = widget.QLabel(data["minmax"])
        self.MINMAX_LBL.setStyleSheet("color: rgba(255,255,255,180); font-size: 16px; border: none; background: transparent; font-weight: 500;")

        self.ICON_LBL = widget.QLabel()
        self.ICON_LBL.setFixedSize(150, 70)
        self.ICON_LBL.setStyleSheet("background: transparent")
        # Первоначально использовали иконки из "weather icon Bl WI",
        # но здесь явно берем иконки из папки "weather icon" (PNG).
        icon_name = data.get("icon", "") + ".png"
        icon_path = create_media_path(os.path.join("weather icon", icon_name))
        if os.path.exists(icon_path):
            self.ICON_LBL.setPixmap(gui.QPixmap(icon_path))

        self.TEMP_LBL = widget.QLabel(f"{data['temp']}°")
        self.TEMP_LBL.setStyleSheet("font-size: 52px; color: white; font-weight: 500; border: none; background: transparent;")

        self.ICON_TEMP_ROW = widget.QHBoxLayout()
        self.ICON_TEMP_ROW.setSpacing(8)
        self.ICON_TEMP_ROW.setContentsMargins(0, 0, 0, 0)

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

        # ===== ПРАВА КАРТОЧКА =====
        self.RIGHT = widget.QFrame()
        self.RIGHT.setFixedSize(390, 303)
        self.RIGHT.setStyleSheet("background: rgba(0, 0, 0, 0.2); border-radius: 20px; border: none;")

        self.TODAY = widget.QLabel("Сьогодні")
        self.TODAY.setStyleSheet("font-size: 16px; color: white; font-weight: 500; background: transparent;")

        self.DAY_LBL = widget.QLabel()
        self.DAY_LBL.setStyleSheet("color: white; font-size: 24px; font-weight: 500; background: transparent;")

        self.DATE_LBL = widget.QLabel()
        self.DATE_LBL.setStyleSheet("color: rgba(255,255,255,0.85); font-size: 24px; font-weight: 500; background: transparent;")

        self.TODAY_ROW = widget.QHBoxLayout()
        self.TODAY_ROW.setContentsMargins(24, 16, 24, 8)
        self.TODAY_ROW.addWidget(self.TODAY)

        self.RIGHT_SEPARATOR = widget.QFrame()
        self.RIGHT_SEPARATOR.setFixedHeight(1)
        self.RIGHT_SEPARATOR.setStyleSheet("background: rgba(255, 255, 255, 0.25); border: none;")

        self.RIGHT_SEPARATOR_LAYOUT = widget.QHBoxLayout()
        self.RIGHT_SEPARATOR_LAYOUT.setContentsMargins(24, 0, 24, 0)
        self.RIGHT_SEPARATOR_LAYOUT.addWidget(self.RIGHT_SEPARATOR)

        self.DAY_DATE_ROW = widget.QHBoxLayout()
        self.DAY_DATE_ROW.setContentsMargins(24, 12, 24, 0)
        self.DAY_DATE_ROW.addWidget(self.DAY_LBL)
        self.DAY_DATE_ROW.addStretch()
        self.DAY_DATE_ROW.addWidget(self.DATE_LBL)
        
        # === БЛОК ЧАСОВ ===
        X = 160  
        Y = 160

        self.CLOCK_CONTAINER = widget.QWidget()
        self.CLOCK_CONTAINER.setFixedSize(X, Y)
        self.CLOCK_CONTAINER.setStyleSheet("background: transparent;")

        # отрисованный виджет вместо картинки
        self.CLOCK_BG = ClockFaceWidget(self.CLOCK_CONTAINER)
        self.CLOCK_BG.setFixedSize(X, Y)

        # Час поверх 
        self.CLOCK_LBL = widget.QLabel(self.CLOCK_CONTAINER)
        self.CLOCK_LBL.setFixedSize(X, Y)
        self.CLOCK_LBL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.CLOCK_LBL.setStyleSheet("""
            background: transparent; 
            font-size: 34px; 
            color: white; 
            font-weight: 500;
        """)

        self.RIGHT_LAYOUT = widget.QVBoxLayout(self.RIGHT)
        self.RIGHT_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.RIGHT_LAYOUT.setSpacing(0)
        
        self.RIGHT_LAYOUT.addLayout(self.TODAY_ROW)
        self.RIGHT_LAYOUT.addLayout(self.RIGHT_SEPARATOR_LAYOUT)
        self.RIGHT_LAYOUT.addLayout(self.DAY_DATE_ROW)
        
        self.RIGHT_LAYOUT.addSpacing(15) 
        self.RIGHT_LAYOUT.addWidget(self.CLOCK_CONTAINER, alignment=core.Qt.AlignmentFlag.AlignHCenter | core.Qt.AlignmentFlag.AlignTop)
        self.RIGHT_LAYOUT.addStretch()

        # Основний лейаут
        self.MAIN_LAYOUT.addWidget(self.LEFT)
        self.MAIN_LAYOUT.addWidget(self.RIGHT)

        # Таймер
        self.TZ = data.get("timezone")
        self.TIMER = core.QTimer(self)
        self.TIMER.timeout.connect(self.UPDATE_TIME)
        self.TIMER.start(60 * 1000)
        self.UPDATE_TIME()

    def UPDATE_TIME(self):
        now = datetime.now(self.TZ) if self.TZ else datetime.now()
        days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]
        self.DAY_LBL.setText(days[now.weekday()])
        self.DATE_LBL.setText(now.strftime("%d.%m.%Y"))
        self.CLOCK_LBL.setText(now.strftime("%H:%M"))
