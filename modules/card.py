import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from datetime import datetime  
from . import styles
from .create_path import create_media_path


class Card(widget.QFrame):
    def __init__(self, width: int, height: int, parent=None, right_layout=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.right_layout = right_layout
        self.container_layout = widget.QVBoxLayout(self)
        self.container_layout.setContentsMargins(22, 55, 20, 40)


class CityInfoFrame(widget.QFrame):
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.DATA = data
        self.setStyleSheet("background: transparent;")
   

        self.MAIN_LAYOUT = widget.QHBoxLayout(self)
        # self.MAIN_LAYOUT.setSpacing(20)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)

        # ===== ЛЕВАЯ КАРТОЧКА — погода =====
        self.LEFT = widget.QFrame()
        self.LEFT.setFixedSize(390, 303)
        self.LEFT.setStyleSheet("background: rgba(0, 0, 0, 0.2); border-radius: 20px;border: none;")

        self.LOCATION_ICON = widget.QToolButton()
        self.LOCATION_ICON.setIcon(gui.QIcon(gui.QPixmap(create_media_path("choice_vector.png"))))
        self.LOCATION_ICON.setFixedSize(20, 20)

        self.LOCATION_NAME = widget.QLabel("Поточна позиція")
        self.LOCATION_NAME.setStyleSheet("font-size: 16px; color: white")
        
        
        self.LOCATION_ROW = widget.QHBoxLayout()
        self.LOCATION_ROW.setContentsMargins(0, 8, 16, 16)
        self.LOCATION_ROW.addWidget(self.LOCATION_ICON)
        self.LOCATION_ROW.addWidget(self.LOCATION_NAME)

        self.LEFT_LAYOUT = widget.QVBoxLayout(self.LEFT)
        self.LEFT_LAYOUT.setContentsMargins(20, 8, 0, 20)
        self.LEFT_LAYOUT.setSpacing(16)

        self.CITY_LBL = widget.QLabel(data["city"])
        self.CITY_LBL.setStyleSheet("font-size: 44px; color: white; font-weight: 500;")

        self.DESC_LBL = widget.QLabel(data["desc"])
        self.DESC_LBL.setStyleSheet("color: white; font-size: 24px; font-weight: 500;")

        self.MINMAX_LBL = widget.QLabel(data["minmax"])
        self.MINMAX_LBL.setStyleSheet("color: rgba(255,255,255,180); font-size: 16px;border: none; font-weight: 500;")

        self.ICON_LBL = widget.QLabel()
        icon_path = create_media_path(data.get("icon", "") + ".png")
        if os.path.exists(icon_path):
            self.ICON_LBL.setPixmap(gui.QPixmap(icon_path))

        self.TEMP_LBL = widget.QLabel(f"{data['temp']}°")
        self.TEMP_LBL.setStyleSheet("font-size: 52px; color: white; font-weight: 500;border: none;")

        self.ICON_TEMP_ROW = widget.QHBoxLayout()
        self.ICON_TEMP_ROW.setSpacing(10)
        self.ICON_TEMP_ROW.setContentsMargins(0, 0, 0, 0)
        self.ICON_TEMP_ROW.addWidget(self.ICON_LBL)
        self.ICON_TEMP_ROW.addWidget(self.TEMP_LBL)

        self.LEFT_LAYOUT.addLayout(self.LOCATION_ROW)

        self.LEFT_LAYOUT.addWidget(self.CITY_LBL, alignment=core.Qt.AlignmentFlag.AlignCenter)
        self.LEFT_LAYOUT.addLayout(self.ICON_TEMP_ROW)
        self.LEFT_LAYOUT.addWidget(self.DESC_LBL, alignment=core.Qt.AlignmentFlag.AlignCenter)
        self.LEFT_LAYOUT.addWidget(self.MINMAX_LBL, alignment=core.Qt.AlignmentFlag.AlignCenter)
        
        self.LEFT_LAYOUT.addStretch()

        # ===== ПРАВАЯ КАРТОЧКА — часы =====
        self.RIGHT = widget.QFrame()
        self.RIGHT.setFixedSize(390, 303)
        self.RIGHT.setStyleSheet("background: rgba(255,255,255,60); border-radius: 20px;border: none;border: none;")

        self.TODAY = widget.QLabel("Сьогодні")
        self.TODAY.setStyleSheet("font-size: 16px; color: white; font-weight: 500")

        self.RIGHT_LAYOUT = widget.QVBoxLayout(self.RIGHT)
        self.RIGHT_LAYOUT.setContentsMargins(20, 15, 20, 15)
        self.RIGHT_LAYOUT.setSpacing(8)

        self.DAY_LBL = widget.QLabel()
        self.DAY_LBL.setStyleSheet("color: white; font-size: 24px; font-weight: 500;border: none;")

        self.DATE_LBL = widget.QLabel()
        self.DATE_LBL.setStyleSheet("color: rgba(255,255,255,180); font-size: 24px;border: none; font-weight: 500")

        self.DAY_DATE_ROW = widget.QHBoxLayout()
        self.DAY_DATE_ROW.addWidget(self.DAY_LBL)
        self.DAY_DATE_ROW.addStretch()
        self.DAY_DATE_ROW.addWidget(self.DATE_LBL)



        # картинка циферблата с временем поверх
        self.CLOCK_CONTAINER = widget.QWidget()
        self.CLOCK_CONTAINER.setFixedSize(300, 300)
        self.CLOCK_CONTAINER.setStyleSheet("background: transparent;")

        self.CLOCK_BG = widget.QLabel(self.CLOCK_CONTAINER)
        self.CLOCK_BG.setFixedSize(300, 300 )
        clock_bg_path = create_media_path("clock.png")
        if os.path.exists(clock_bg_path):
            self.CLOCK_BG.setPixmap(gui.QPixmap(clock_bg_path).scaled(300, 300, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))

        self.CLOCK_LBL = widget.QLabel(self.CLOCK_CONTAINER)
        self.CLOCK_LBL.setFixedSize(300, 300)
        self.CLOCK_LBL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.CLOCK_LBL.setStyleSheet("background: transparent; font-size: 18px; color: white; font-weight: bold;border: none;")
        
        self.RIGHT_LAYOUT.addWidget(self.TODAY, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.RIGHT_LAYOUT.addLayout(self.DAY_DATE_ROW)
        self.RIGHT_LAYOUT.addStretch()
        self.RIGHT_LAYOUT.addWidget(self.CLOCK_CONTAINER, alignment=core.Qt.AlignmentFlag.AlignCenter)

        self.MAIN_LAYOUT.addWidget(self.LEFT)
        self.MAIN_LAYOUT.addWidget(self.RIGHT)

        # ===== ТАЙМЕР =====
        self.TZ = data.get("timezone")
        self.TIMER = core.QTimer(self)
        self.TIMER.timeout.connect(self.UPDATE_TIME)
        self.TIMER.start(1000)
        self.UPDATE_TIME()

    def UPDATE_TIME(self):
        now = datetime.now(self.TZ) if self.TZ else datetime.now()
        days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]
        self.DAY_LBL.setText(days[now.weekday()])
        self.DATE_LBL.setText(now.strftime("%d.%m.%Y"))
        self.CLOCK_LBL.setText(now.strftime("%H:%M"))


class WeatherCard(widget.QFrame):
    selected = core.pyqtSignal(object)

    def __init__(self, city: str, time: str, temp: str, desc: str, minmax: str, IS_CURRENT: bool = False):
        super().__init__()
        self.IS_CURRENT = IS_CURRENT
        self.IS_SELECTED = False
        self.setMouseTracking(True)
  
        self.setMaximumSize(330, 104)
        self.CHOICE_ICON = widget.QToolButton()
        self.CHOICE_ICON.setIcon(gui.QIcon(gui.QPixmap(create_media_path("choice_vector.png"))))
        self.CHOICE_ICON.setFixedSize(20, 20)
        self.CHOICE_ICON.setIconSize(core.QSize(20, 20))
        self.CHOICE_ICON.setVisible(False)

        self.CITY_LABEL = widget.QLabel(city)
        self.CITY_LABEL.setStyleSheet(styles.CITY_LABEL)
        self.CITY_LABEL.setSizePolicy(widget.QSizePolicy.Policy.Expanding, 
                                      widget.QSizePolicy.Policy.Preferred)
        # self.CITY_LABEL.setMinimumWidth(140)
        # self.CITY_LABEL.setFixedSize(330, 90)

        self.TIME_LABEL = widget.QLabel(time)
        self.TIME_LABEL.setStyleSheet(styles.TIME_LABEL)

        self.TEMP_LABEL = widget.QLabel(f"{temp}°")
        self.TEMP_LABEL.setStyleSheet(styles.TEMP_LABEL)
        self.TEMP_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignTop)

        self.DESC_LABEL = widget.QLabel(desc)
        self.DESC_LABEL.setStyleSheet(styles.DESC_LABEL)

        self.MINMAX_LABEL = widget.QLabel(minmax)
        self.MINMAX_LABEL.setStyleSheet(styles.MINMAX_LABEL)
        self.MINMAX_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignRight)

        self.TOP_ROW = widget.QHBoxLayout()
        self.TOP_ROW.setContentsMargins(0, 0, 0,0)
        self.TOP_ROW.setSpacing(6)
        self.TOP_ROW.addWidget(self.CHOICE_ICON)
        self.TOP_ROW.addWidget(self.CITY_LABEL)
        self.TOP_ROW.addStretch()
        self.TOP_ROW.addWidget(self.TEMP_LABEL)

        self.MID_ROW = widget.QHBoxLayout()
        self.MID_ROW.setContentsMargins(0, 0, 0, 8)
        self.MID_ROW.addWidget(self.TIME_LABEL)
        self.MID_ROW.addStretch()

        self.BOT_ROW = widget.QHBoxLayout()
        self.BOT_ROW.setContentsMargins(0, 0, 0, 8)
        self.BOT_ROW.addWidget(self.DESC_LABEL)
        self.BOT_ROW.addStretch()
        self.BOT_ROW.addWidget(self.MINMAX_LABEL)

        self.MAIN_LAYOUT = widget.QVBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(8, 8, 8, 8)
        self.MAIN_LAYOUT.setSpacing(0)
        self.MAIN_LAYOUT.addLayout(self.TOP_ROW)
        self.MAIN_LAYOUT.addLayout(self.MID_ROW)
        self.MAIN_LAYOUT.addStretch()
        self.MAIN_LAYOUT.addLayout(self.BOT_ROW)
        

        self.apply_style(dimmed=False)

    def update_data(self, data: dict):
        self.weather_data = data
        self.CITY_LABEL.setText(data["city"])
        self.TIME_LABEL.setText(data["time"])
        self.TEMP_LABEL.setText(f"{data['temp']}°")
        self.DESC_LABEL.setText(data["desc"])
        self.MINMAX_LABEL.setText(data["minmax"])

    def apply_style(self, dimmed: bool):
        if self.IS_CURRENT:
            bg = "rgba(0,0,0,110)" if dimmed else "rgba(0,0,0,60)"
            self.setStyleSheet(styles.CURRENT_CARD.format(bg=bg))
        else:
            bg     = "rgba(0,0,0,80)"       if dimmed else "transparent"
            border = "rgba(255,255,255,80)" if dimmed else "rgba(255,255,255,40)"
            radius = "10px"                 if dimmed else "0px"
            self.setStyleSheet(styles.DEFAULT_CARD.format(bg = bg, border = border, radius = radius))

    def set_selected(self, selected: bool):
        self.IS_SELECTED = selected
        self.CHOICE_ICON.setVisible(selected)
        self.apply_style(dimmed=selected)

    def enterEvent(self, event):
        if not self.IS_SELECTED: self.apply_style(dimmed=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.IS_SELECTED: self.apply_style(dimmed=False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == core.Qt.MouseButton.LeftButton: self.selected.emit(self)
        super().mousePressEvent(event)