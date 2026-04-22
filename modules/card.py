import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from . import styles


class Card(widget.QFrame):
    def __init__(self, width, height, parent=None, right_layout=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.RIGHT_LAYOUT = right_layout
        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setContentsMargins(22, 55, 20, 40)


class WeatherCard(widget.QFrame):
    selected = core.pyqtSignal(object)

    def __init__(self, city, time, temp, desc, minmax, is_current=False):
        super().__init__()
        self.is_current = is_current
        self.is_selected = False
        self.setMouseTracking(True)

        self.CHOICE_PIXMAP = gui.QPixmap("choice_vector.png")
        self.CHOICE_ICON = widget.QToolButton()
        self.CHOICE_ICON.setIcon(gui.QIcon(self.CHOICE_PIXMAP))
        self.CHOICE_ICON.setFixedSize(20, 20)
        self.CHOICE_ICON.setVisible(False)

        self.CITY_LABEL   = widget.QLabel(city);      self.CITY_LABEL.setStyleSheet(styles.CITY_LABEL)
        self.TIME_LABEL   = widget.QLabel(time);      self.TIME_LABEL.setStyleSheet(styles.TIME_LABEL)
        self.TEMP_LABEL   = widget.QLabel(f"{temp}°"); self.TEMP_LABEL.setStyleSheet(styles.TEMP_LABEL)
        self.DESC_LABEL   = widget.QLabel(desc);      self.DESC_LABEL.setStyleSheet(styles.DESC_LABEL)
        self.MINMAX_LABEL = widget.QLabel(minmax);    self.MINMAX_LABEL.setStyleSheet(styles.MINMAX_LABEL)
        self.CITY_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.TEMP_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignTop)
        self.MINMAX_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignBottom)

        grid = widget.QGridLayout(self)
        grid.setContentsMargins(15, 15, 15, 15)
        grid.addWidget(self.CHOICE_ICON,  0, 0)
        grid.addWidget(self.CITY_LABEL,   0, 0)
        grid.addWidget(self.TIME_LABEL,   1, 0, 1, 2)
        grid.addWidget(self.TEMP_LABEL,   0, 2, 2, 1)
        grid.addWidget(self.DESC_LABEL,   2, 0, 1, 2)
        grid.addWidget(self.MINMAX_LABEL, 2, 2)

        self.apply_style(dimmed=False)

    def apply_style(self, dimmed):
        if self.is_current:
            bg = "rgba(0,0,0,110)" if dimmed else "rgba(0,0,0,60)"
            self.setStyleSheet(styles.CURRENT_CARD.format(bg=bg))
        else:
            bg     = "rgba(0,0,0,80)"       if dimmed else "transparent"
            border = "rgba(255,255,255,80)" if dimmed else "rgba(255,255,255,40)"
            radius = "10px"                 if dimmed else "0px"
            self.setStyleSheet(styles.DEFAULT_CARD.format(bg=bg, border=border, radius=radius))

    def set_selected(self, selected):
        self.is_selected = selected
        self.CHOICE_ICON.setVisible(selected)
        self.apply_style(dimmed=selected)

    def enterEvent(self, event):
        if not self.is_selected: self.apply_style(dimmed=True)
        super().enterEvent(event)

    def leaveEvent(self, e):
        if not self.is_selected: self.apply_style(dimmed=False)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == core.Qt.MouseButton.LeftButton: self.selected.emit(self)
        super().mousePressEvent(e)
