import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from datetime import datetime  
from . import styles
from .create_path import create_media_path

class ClockFaceWidget(widget.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.TICK_LENGTH = 12
        self.TICK_MARGIN = 15
        self.TICK_WIDTH = 4
        self.BG_ALPHA = 45
        self.TICK_ALPHA = 150

    def paintEvent(self, event):
        self.PAINTER = gui.QPainter(self)
        self.PAINTER.setRenderHint(gui.QPainter.RenderHint.Antialiasing)

        self.WIDTH = self.width()
        self.HEIGHT = self.height()
        self.CENTER = core.QPointF(self.WIDTH / 2.0, self.HEIGHT / 2.0)
        self.RADIUS = min(self.WIDTH, self.HEIGHT) / 2.0

        self.PAINTER.setBrush(gui.QColor(0, 0, 0, self.BG_ALPHA))
        self.PAINTER.setPen(core.Qt.PenStyle.NoPen)
        self.PAINTER.drawEllipse(self.CENTER, self.RADIUS, self.RADIUS)

        self.PAINTER.translate(self.CENTER)
        self.PEN = gui.QPen(gui.QColor(255, 255, 255, self.TICK_ALPHA))
        self.PEN.setWidth(self.TICK_WIDTH)
        self.PEN.setCapStyle(core.Qt.PenCapStyle.RoundCap)
        self.PAINTER.setPen(self.PEN)

        for i in range(12):
            self.PAINTER.drawLine(
                core.QPointF(0, -self.RADIUS + self.TICK_MARGIN), 
                core.QPointF(0, -self.RADIUS + self.TICK_MARGIN + self.TICK_LENGTH)
            )
            self.PAINTER.rotate(30.0)
            
        self.PAINTER.end()


class CityInfoFrame(widget.QFrame):
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
# Добавьте эти классы в ваш файл с классами карточек

# ===== ВИДЖЕТ ДЛЯ ОТОБРАЖЕННЯ ПОГОДИ НА НАЙБЛИЖЧІ ГОДИНИ =====
class HourlyForecastFrame(widget.QFrame):
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.setFixedHeight(157)
        self.setStyleSheet("background: rgba(0, 0, 0, 0.2); border-radius: 20px;")

        self.MAIN_LAYOUT = widget.QVBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(15, 12, 15, 12)
        self.MAIN_LAYOUT.setSpacing(0)

        self.TITLE_LBL = widget.QLabel(data.get("desc", "Хмарна погода до кінця дня"))
        self.TITLE_LBL.setStyleSheet("font-size: 14px; color: white; font-weight: 500; background: transparent;")
        self.MAIN_LAYOUT.addWidget(self.TITLE_LBL)

        self.LINE = widget.QFrame()
        self.LINE.setFixedHeight(1)
        self.LINE.setStyleSheet("background: rgba(255,255,255,0.2); margin-top: 8px; margin-bottom: 5px;")
        self.MAIN_LAYOUT.addWidget(self.LINE)

        self.H_CONTAINER = widget.QHBoxLayout()
        self.H_CONTAINER.setSpacing(4)

        # --- Левая стрелка ---
        self.L_ARROW = widget.QPushButton()
        self.L_ARROW.setFixedSize(20, 40)
        self.L_ARROW.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.L_ARROW.setStyleSheet("background: transparent; border: none;")
        l_icon_path = create_media_path("less_vector.png")
        if os.path.exists(l_icon_path):
            self.L_ARROW.setIcon(gui.QIcon(l_icon_path))
            self.L_ARROW.setIconSize(core.QSize(16, 16))
        else:
            self.L_ARROW.setText("<")
            self.L_ARROW.setStyleSheet("color: rgba(255,255,255,150); font-size: 14px; background: transparent; border: none;")

        # Создаём эффекты ОДИН РАЗ и сохраняем
        self.L_EFFECT = widget.QGraphicsOpacityEffect(self.L_ARROW)
        self.L_EFFECT.setOpacity(0.3)
        self.L_ARROW.setGraphicsEffect(self.L_EFFECT)
        self.L_ARROW.setEnabled(False)

        self.H_CONTAINER.addWidget(self.L_ARROW)


        # --- Область прокрутки ---
        self.SCROLL = widget.QScrollArea()
        self.SCROLL.setWidgetResizable(True)
        self.SCROLL.setFrameShape(widget.QFrame.Shape.NoFrame)
        self.SCROLL.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL.setStyleSheet("background: transparent;")

        self.CONTENT = widget.QWidget()
        self.CONTENT.setStyleSheet("background: transparent;")
        self.CONTENT_LAYOUT = widget.QHBoxLayout(self.CONTENT)
        self.CONTENT_LAYOUT.setContentsMargins(5, 0, 5, 0)
        self.CONTENT_LAYOUT.setSpacing(25)

        for item in data.get("today_hours", []):
            hour_widget = widget.QWidget()
            hour_layout = widget.QVBoxLayout(hour_widget)
            hour_layout.setContentsMargins(0, 5, 0, 5)
            hour_layout.setSpacing(8)

            time_str = "Зараз" if item.get("is_current") else item["time"]
            t_lbl = widget.QLabel(time_str)
            t_lbl.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            t_lbl.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent;")

            i_lbl = widget.QLabel()
            icon_name = f"{item['icon']}.png" if not item.get("is_sunset") else "sunset.png"
            icon_path = create_media_path(os.path.join("weather icon", icon_name))
            if os.path.exists(icon_path):
                pix = gui.QPixmap(icon_path).scaled(
                    32, 32,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation
                )
                i_lbl.setPixmap(pix)
            i_lbl.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            i_lbl.setStyleSheet("background: transparent;")

            temp_val = f"{item['temp']}°" if not item.get("is_sunset") else "Захід сонця"
            temp_lbl = widget.QLabel(temp_val)
            temp_lbl.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            temp_lbl.setStyleSheet("color: white; font-size: 14px; font-weight: 500; background: transparent;")

            if item.get("is_sunset"):
                hour_widget.setMinimumWidth(90)

            hour_layout.addWidget(t_lbl)
            hour_layout.addWidget(i_lbl)
            hour_layout.addWidget(temp_lbl)
            self.CONTENT_LAYOUT.addWidget(hour_widget)

        self.SCROLL.setWidget(self.CONTENT)
        self.H_CONTAINER.addWidget(self.SCROLL)

        # --- Правая стрелка ---
        self.R_ARROW = widget.QPushButton()
        self.R_ARROW.setFixedSize(20, 40)
        self.R_ARROW.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.R_ARROW.setStyleSheet("background: transparent; border: none;")
        r_icon_path = create_media_path("more_vector.png")
        if os.path.exists(r_icon_path):
            self.R_ARROW.setIcon(gui.QIcon(r_icon_path))
            self.R_ARROW.setIconSize(core.QSize(16, 16))
        else:
            self.R_ARROW.setText(">")
            self.R_ARROW.setStyleSheet("color: rgba(255,255,255,150); font-size: 14px; background: transparent; border: none;")

        # Эффект правой стрелки — изначально активна
        self.R_EFFECT = widget.QGraphicsOpacityEffect(self.R_ARROW)
        self.R_EFFECT.setOpacity(1.0)
        self.R_ARROW.setGraphicsEffect(self.R_EFFECT)

        self.H_CONTAINER.addWidget(self.R_ARROW)
        self.MAIN_LAYOUT.addLayout(self.H_CONTAINER)

        self.L_ARROW.clicked.connect(self._scroll_left)
        self.R_ARROW.clicked.connect(self._scroll_right)
        self.SCROLL.horizontalScrollBar().valueChanged.connect(self._on_scroll_changed)

    def _set_arrow_opacity(self, effect: widget.QGraphicsOpacityEffect, active: bool):
        effect.setOpacity(1.0 if active else 0.3)

    def _scroll_left(self):
        bar = self.SCROLL.horizontalScrollBar()
        bar.setValue(bar.value() - 150)

    def _scroll_right(self):
        bar = self.SCROLL.horizontalScrollBar()
        bar.setValue(bar.value() + 150)

    def _on_scroll_changed(self, value: int):
        bar     = self.SCROLL.horizontalScrollBar()
        at_start = value <= bar.minimum()
        at_end   = value >= bar.maximum()

        self.L_ARROW.setEnabled(not at_start)
        self._set_arrow_opacity(self.L_EFFECT, not at_start)

        self.R_ARROW.setEnabled(not at_end)
        self._set_arrow_opacity(self.R_EFFECT, not at_end)


# ===== ВІДЖЕТ ДЛЯ ГРАФІКА ПРОГНОЗУ НА 12 ГОДИН =====
class TwelveHourGraphFrame(widget.QFrame):
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)

        self.setFixedHeight(197)

        self.setStyleSheet("""
            TwelveHourGraphFrame {
                background: rgba(0, 0, 0, 0.2);
                border-radius: 20px;
            }
        """)

        original_data = data.get("next_12h", [])

        self.forecast_data = []
        for item in original_data:
            for _ in range(4):
                self.forecast_data.append(item)

        layout = widget.QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 0)

        title = widget.QLabel("Прогноз на 12 годин")
        title.setStyleSheet("font-size: 13px; color: white; font-weight: bold; background: transparent; opacity: 0.8;")
        layout.addWidget(title)

        layout.addStretch()

    # ===== МЕТОД ВІДМАЛЮВАННЯ ГРАФІКА =====
    def paintEvent(self, event):

        painter = gui.QPainter(self)
        painter.setRenderHint(gui.QPainter.RenderHint.Antialiasing)

        # ===== РОЗРАХУНОК РОЗМІРІВ І ГРАНИЦЬ =====
        W, H = self.width(), self.height()  
        pad_l, pad_r = 15, 35  
        pad_top, pad_bot = 55, 30  
        draw_w = W - pad_l - pad_r
        draw_h = H - pad_top - pad_bot

        # ===== 1. МАЛЮЄМО СІТКУ ТЕМПЕРАТУР =====
        scale_values = [25, 20, 15, 10, 5, 0, -5, -10]
        y_min, y_max = -10, 25  # Мінімальна та максимальна температура на графіку
        
       
        font = painter.font()
        font.setPointSize(7)
        painter.setFont(font)
        
        # Малюємо горизонтальні лінії для температури
        for val in scale_values:
            # Розраховуємо координату Y для цієї температури
            y = pad_top + (y_max - val) * (draw_h / (y_max - y_min))
            
            pen = gui.QPen(gui.QColor(255, 255, 255, 30)) 
            pen.setStyle(core.Qt.PenStyle.DotLine)  
            painter.setPen(pen)
            painter.drawLine(pad_l, int(y), W - pad_r, int(y))
            
            # Пишемо значення температури справа від графіка
            painter.setPen(gui.QColor(255, 255, 255, 160))  
            painter.drawText(W - 28, int(y) + 4, f"{val}°")

        
        
        # ===== 2. МАЛЮЄМО КОЛЬОРОВІ СТОВПЦІ ТЕМПЕРАТУРИ =====
        n = len(self.forecast_data)  # Кількість стовпців
        step = draw_w / n  
        bar_w = step * 0.7  

        # Малюємо стовпець
        for i, item in enumerate(self.forecast_data):
            # Отримуємо температуру
            temp = item["temp"]
            # Обмежуємо температуру 
            safe_temp = max(y_min, min(y_max, temp))
            
            # Розраховуємо координату Y 
            y_val = pad_top + (y_max - safe_temp) * (draw_h / (y_max - y_min))
            y_bottom = pad_top + draw_h  # Дно графіка
            
            # Координата X для цього стовпця
            x = pad_l + i * step
            rect = core.QRectF(x, y_val, bar_w, y_bottom - y_val)

            # ===== ГРАДІЄНТ ДЛЯ СТОВПЦЯ =====
            grad = gui.QLinearGradient(rect.topLeft(), rect.bottomLeft())
            grad.setColorAt(0, gui.QColor(255, 255, 150, 200))  # Світло-жовтий верх
            grad.setColorAt(1, gui.QColor(100, 180, 255, 120))  # Голубоватий низ

            # Встановлюємо кисть з градієнтом та малюємо стовпець
            painter.setPen(core.Qt.PenStyle.NoPen)  
            painter.setBrush(gui.QBrush(grad))
            painter.drawRoundedRect(rect, 1, 1)  

            # ===== 3. МАЛЮЄМО ІКОНКИ ПОГОДИ =====
            if i % 4 == 0:
                icon_name = f"{item['icon']}.png"
                icon_path = create_media_path(os.path.join("weather icon", icon_name))
                if os.path.exists(icon_path):
                    pix = gui.QPixmap(icon_path).scaled(21, 21, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation)
                    icon_x = int(x + (step * 4) / 2 - 8)
                    painter.drawPixmap(icon_x, pad_top - 25, pix)

        # Завершуємо малювання
        painter.end()
