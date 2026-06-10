import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from ..create_path import create_media_path
from ..settings.langueges import LanguageManager
from .. import styles


class SettingsPanel(widget.QFrame):
    settings_clicked = core.pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(150, 45)
        self.setStyleSheet(styles.SETTINGS_FRAME)
        
        self.LAYOUT = widget.QHBoxLayout(self)
        self.LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.LAYOUT.setSpacing(5)
        
        # Кнопка настроек
        self.SETTINGS_BOX = widget.QFrame(self)
        self.SETTINGS_BOX.setFixedSize(45, 45)
        self.SETTINGS_BOX.setStyleSheet(styles.SETTINGS_BOX)
        
        self.SETTINGS_BTN = widget.QPushButton(self.SETTINGS_BOX)
        self.SETTINGS_BTN.setFixedSize(45, 45)
        self.PIXMAP = gui.QPixmap(create_media_path("Vector.png"))
        self.SETTINGS_BTN.setIcon(gui.QIcon(self.PIXMAP))
        self.SETTINGS_BTN.setIconSize(core.QSize(20, 20))
        self.SETTINGS_BTN.setStyleSheet(styles.SETTINGS_BUTTON)
        self.SETTINGS_BTN.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.SETTINGS_BTN.clicked.connect(self.settings_clicked.emit)
        
        # Название настроек
        self.SETTINGS_LABEL = widget.QLabel(LanguageManager.get_text("LABEL_SETTINGS"))
        self.SETTINGS_LABEL.setStyleSheet(styles.SETTINGS_LABEL)
        self.SETTINGS_LABEL.setAlignment(
            core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignVCenter)
        
        self.LAYOUT.addWidget(self.SETTINGS_BOX,
            alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.LAYOUT.addWidget(self.SETTINGS_LABEL,
            alignment=core.Qt.AlignmentFlag.AlignLeft)
