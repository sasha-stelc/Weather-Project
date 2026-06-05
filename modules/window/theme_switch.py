import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from ..create_path import create_media_path
from .. import styles


class ImageThemeSwitch(widget.QPushButton):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setCheckable(True)
        self.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(52, 24)
        self.setIconSize(core.QSize(18, 18))
        self.SUN_ICON  = gui.QIcon(create_media_path("Frame_51.png"))
        self.MOON_ICON = gui.QIcon(create_media_path("Frame_52.png"))
        self.toggled.connect(self.UPDATE_IMAGE)
        self.setChecked(False)
        self.UPDATE_IMAGE(False)

    def UPDATE_IMAGE(self, checked: bool):
        self.setStyleSheet(styles.THEME_BUTTON_SUN if checked else styles.THEME_BUTTON_MOON)
        self.setIcon(self.SUN_ICON if checked else self.MOON_ICON)
        if self.app:
            self.app.SET_THEME_LIGHT() if checked else self.app.SET_THEME_DARK()
