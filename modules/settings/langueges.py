import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
from .. import styles


class AppLanguage:
    def __init__(self, parent=None):

        self.DESC_PAGE = "Мова додатку"

        LABEL_STYLE = styles.LANGUAGE_LABEL_STYLE
        TITLE_STYLE = styles.LANGUAGE_TITLE_STYLE
        COMBOBOX_STYLE = styles.LANGUAGE_COMBOBOX_STYLE
        BUTTON_STYLE = styles.LANGUAGE_BUTTON_STYLE

        # ===== КОРНЕВОЙ ВИДЖЕТ =====
        self.ROOT = widget.QWidget(parent)
        self.ROOT_LAYOUT = widget.QVBoxLayout(self.ROOT)
        self.ROOT_LAYOUT.setContentsMargins(0, 0, 0, 16)
        self.ROOT_LAYOUT.setSpacing(16)
        self.ROOT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        # ===== ЗАГОЛОВОК =====
        self.PAGE_TITLE = widget.QLabel("Оберіть мову додатку")
        self.PAGE_TITLE.setStyleSheet(TITLE_STYLE)
        self.ROOT_LAYOUT.addWidget(self.PAGE_TITLE)

        # ===== ФОРМА =====
        self.FORM_FRAME = widget.QFrame()
        self.FORM_FRAME.setFixedWidth(239)
        self.FORM_LAYOUT = widget.QVBoxLayout(self.FORM_FRAME)
        self.FORM_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.FORM_LAYOUT.setSpacing(6)
        self.FORM_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        lbl_lang = widget.QLabel("Мова додатку")
        lbl_lang.setStyleSheet(LABEL_STYLE)
        self.FORM_LAYOUT.addWidget(lbl_lang)

        self.LANGUAGE = widget.QComboBox()
        self.LANGUAGE.setFixedSize(239, 32)
        self.LANGUAGE.setStyleSheet(COMBOBOX_STYLE)
        self.LANGUAGE.addItems([
            "Українська",
            "Русский",
            "English",
        ])
        self.FORM_LAYOUT.addWidget(self.LANGUAGE)

        self.FORM_LAYOUT.addSpacing(12)

        self.CONFIRM_BUTTON = widget.QPushButton("Зберегти")
        self.CONFIRM_BUTTON.setFixedSize(105, 38)
        self.CONFIRM_BUTTON.setStyleSheet(BUTTON_STYLE)
        self.FORM_LAYOUT.addWidget(self.CONFIRM_BUTTON)

        self.ROOT_LAYOUT.addWidget(self.FORM_FRAME)