import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui

from ..create_path import create_media_path
from .utils import get_weather_icon_path


class HourlyForecastFrame(widget.QFrame):
    """Виджет для отображения погоды на ближайшие часы"""
    
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
            icon_code = "sunset" if item.get("is_sunset") else "sunrise" if item.get("is_sunrise") else item["icon"]
            icon_path = get_weather_icon_path(icon_code)
            if os.path.exists(icon_path):
                pix = gui.QPixmap(icon_path).scaled(
                    32, 32,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation
                )
                i_lbl.setPixmap(pix)
            i_lbl.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            i_lbl.setStyleSheet("background: transparent;")

            temp_val = f"{item['temp']}°" if not item.get("is_sunset") and not item.get("is_sunrise") else "Захід сонця" if item.get("is_sunset") else "Схід сонця"
            temp_lbl = widget.QLabel(temp_val)
            temp_lbl.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            temp_lbl.setStyleSheet("color: white; font-size: 14px; font-weight: 500; background: transparent;")

            if item.get("is_sunset") or item.get("is_sunrise"):
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
        bar      = self.SCROLL.horizontalScrollBar()
        at_start = value <= bar.minimum()
        at_end   = value >= bar.maximum()

        self.L_ARROW.setEnabled(not at_start)
        self._set_arrow_opacity(self.L_EFFECT, not at_start)

        self.R_ARROW.setEnabled(not at_end)
        self._set_arrow_opacity(self.R_EFFECT, not at_end)
