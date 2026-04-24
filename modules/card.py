import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from . import styles


def create_media_path(name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(current_dir, "..", "media", name))


class Card(widget.QFrame):
    def __init__(self, width: int, height: int, parent=None, right_layout=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.right_layout = right_layout

        self.container_layout = widget.QVBoxLayout(self)
        self.container_layout.setContentsMargins(22, 55, 20, 40)


class WeatherCard(widget.QFrame):
    selected = core.pyqtSignal(object)

    def __init__(self, city: str, time: str, temp: str, desc: str, minmax: str, is_current: bool = False):
        super().__init__()
        self.is_current = is_current
        self.is_selected = False
        self.setMouseTracking(True)

        self.choice_icon = widget.QToolButton()
        self.choice_icon.setIcon(gui.QIcon(gui.QPixmap(create_media_path("choice_vector.png"))))
        self.choice_icon.setFixedSize(20, 20)
        self.choice_icon.setIconSize(core.QSize(20, 20))
        self.choice_icon.setVisible(False)

        self.city_label = widget.QLabel(city)
        self.city_label.setStyleSheet(styles.CITY_LABEL)

        self.time_label = widget.QLabel(time)
        self.time_label.setStyleSheet(styles.TIME_LABEL)

        self.temp_label = widget.QLabel(f"{temp}°")
        self.temp_label.setStyleSheet(styles.TEMP_LABEL)

        self.desc_label = widget.QLabel(desc)
        self.desc_label.setStyleSheet(styles.DESC_LABEL)

        self.minmax_label = widget.QLabel(minmax)
        self.minmax_label.setStyleSheet(styles.MINMAX_LABEL)

        self.city_label.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.temp_label.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignTop)
        self.minmax_label.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignBottom)

        grid = widget.QGridLayout(self)
        grid.setContentsMargins(15, 15, 15, 15)
        grid.addWidget(self.choice_icon, 0, 0)
        grid.addWidget(self.city_label, 0, 1)
        grid.addWidget(self.time_label, 1, 0, 1, 2)
        grid.addWidget(self.temp_label, 0, 2, 2, 1)
        grid.addWidget(self.desc_label, 2, 0, 1, 2)
        grid.addWidget(self.minmax_label, 2, 2)

        self.apply_style(dimmed=False)

    def apply_style(self, dimmed: bool):
        if self.is_current:
            bg = "rgba(0,0,0,110)" if dimmed else "rgba(0,0,0,60)"
            self.setStyleSheet(styles.CURRENT_CARD.format(bg=bg))
        else:
            bg = "rgba(0,0,0,80)" if dimmed else "transparent"
            border = "rgba(255,255,255,80)" if dimmed else "rgba(255,255,255,40)"
            radius = "10px" if dimmed else "0px"
            self.setStyleSheet(styles.DEFAULT_CARD.format(bg=bg, border=border, radius=radius))

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self.choice_icon.setVisible(selected)
        self.apply_style(dimmed=selected)

    def enterEvent(self, event):
        if not self.is_selected:
            self.apply_style(dimmed=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_selected:
            self.apply_style(dimmed=False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.selected.emit(self)
        super().mousePressEvent(event)