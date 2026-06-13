import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from ..create_path import create_media_path
from ..settings.langueges import LANGUAGE_SIGNAL, LanguageManager
from ..settings.size_config import SizeManager
from .. import styles


class SettingsPanel(widget.QFrame):
    settings_clicked = core.pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        sp = SizeManager.get("settings_panel")
        self.setFixedSize(sp["width"], sp["height"])
        self.setStyleSheet(styles.SETTINGS_FRAME)
        
        self.LAYOUT = widget.QHBoxLayout(self)
        self.LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.LAYOUT.setSpacing(5)
        
        # Кнопка настроек
        self.SETTINGS_BOX = widget.QFrame(self)
        sb = SizeManager.get("settings_box")
        self.SETTINGS_BOX.setFixedSize(sb["width"], sb["height"])
        self.SETTINGS_BOX.setStyleSheet(styles.SETTINGS_BOX)
        
        self.SETTINGS_BTN = widget.QPushButton(self.SETTINGS_BOX)
        sbtn = SizeManager.get("settings_btn")
        self.SETTINGS_BTN.setFixedSize(sbtn["width"], sbtn["height"])
        self.PIXMAP = gui.QPixmap(create_media_path("Vector.png"))
        self.SETTINGS_BTN.setIcon(gui.QIcon(self.PIXMAP))
        sicon = SizeManager.get("settings_btn_icon")
        self.SETTINGS_BTN.setIconSize(core.QSize(sicon["width"], sicon["height"]))
        self.SETTINGS_BTN.setStyleSheet(styles.SETTINGS_BUTTON)
        self.SETTINGS_BTN.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.SETTINGS_BTN.clicked.connect(self.settings_clicked.emit)
        
        # Название настроек
        self.SETTINGS_LABEL = widget.QLabel(LanguageManager.get_text("LABEL_SETTINGS"))
        self.SETTINGS_LABEL.setText(LanguageManager.get_text("LABEL_SETTINGS"))
        self.SETTINGS_LABEL.setStyleSheet(styles.SETTINGS_LABEL)
        self.SETTINGS_LABEL.setAlignment(
            core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignVCenter)
        
        self.LAYOUT.addWidget(self.SETTINGS_BOX,
            alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.LAYOUT.addWidget(self.SETTINGS_LABEL,
            alignment=core.Qt.AlignmentFlag.AlignLeft)
        LANGUAGE_SIGNAL.language_changed.connect(self.retranslate)
    def retranslate(self, lang=None):
        """Обновляет все переводимые строки при смене языка"""
        self.SETTINGS_LABEL.setText(LanguageManager.get_text("LABEL_SETTINGS"))
        self.SETTINGS_BTN.setToolTip(LanguageManager.get_text("TOOLTIP_SETTINGS"))
        self.SETTINGS_BTN.setAccessibleName(LanguageManager.get_text("ACCESSIBLE_SETTINGS_BUTTON"))
