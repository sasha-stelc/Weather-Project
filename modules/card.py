import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from . import styles
from .create_path import create_media_path

class Card(widget.QFrame):
    def __init__(self, width: int, height: int, parent=None, right_layout=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.right_layout = right_layout
        self.container_layout = widget.QVBoxLayout(self)
        self.container_layout.setContentsMargins(22, 55, 20, 40)


class WeatherCard(widget.QFrame):
    selected = core.pyqtSignal(object)

    def __init__(self, city: str, time: str, temp: str, desc: str, minmax: str, IS_CURRENT: bool = False):
        super().__init__()
        self.IS_CURRENT = IS_CURRENT
        self.IS_SELECTED = False
        self.setMouseTracking(True)

        self.CHOICE_ICON = widget.QToolButton()
        self.CHOICE_ICON.setIcon(gui.QIcon(gui.QPixmap(create_media_path("choice_vector.png"))))
        self.CHOICE_ICON.setFixedSize(20, 20)
        self.CHOICE_ICON.setIconSize(core.QSize(20, 20))
        self.CHOICE_ICON.setVisible(False)

        self.CITY_LABEL = widget.QLabel(city)
        self.CITY_LABEL.setStyleSheet(styles.CITY_LABEL)

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
        self.TOP_ROW.setContentsMargins(0, 0, 0, 0)
        self.TOP_ROW.setSpacing(6)
        self.TOP_ROW.addWidget(self.CHOICE_ICON)
        self.TOP_ROW.addWidget(self.CITY_LABEL)
        self.TOP_ROW.addStretch()
        self.TOP_ROW.addWidget(self.TEMP_LABEL)

        self.MID_ROW = widget.QHBoxLayout()
        self.MID_ROW.setContentsMargins(0, 0, 0, 0)
        self.MID_ROW.addWidget(self.TIME_LABEL)
        self.MID_ROW.addStretch()

        self.BOT_ROW = widget.QHBoxLayout()
        self.BOT_ROW.setContentsMargins(0, 0, 0, 0)
        self.BOT_ROW.addWidget(self.DESC_LABEL)
        self.BOT_ROW.addStretch()
        self.BOT_ROW.addWidget(self.MINMAX_LABEL)

        self.MAIN_LAYOUT = widget.QVBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(15, 15, 15, 15)
        self.MAIN_LAYOUT.setSpacing(4)
        self.MAIN_LAYOUT.addLayout(self.TOP_ROW)
        self.MAIN_LAYOUT.addLayout(self.MID_ROW)
        self.MAIN_LAYOUT.addStretch()
        self.MAIN_LAYOUT.addLayout(self.BOT_ROW)
        

        self.apply_style(dimmed=False)

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