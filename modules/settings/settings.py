import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
from .search_sity import SearchCity
from .application_size import Application
from .langueges import AppLanguage
from .. import styles


class NavButton(widget.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(158, 35)
        self.setCheckable(True)
        self._update_style(False)

    def _update_style(self, checked):
        if checked:
            self.setStyleSheet(styles.NAV_BUTTON_CHECKED)
        else:
            self.setStyleSheet(styles.NAV_BUTTON_UNCHECKED)

    def setChecked(self, checked):
        super().setChecked(checked)
        self._update_style(checked)


class Settings(widget.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(1200, 800)
        self.setAttribute(core.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(styles.SETTINGS_MAIN)

        # ===== MAIN LAYOUT =====
        self.MAIN_LAYOUT = widget.QVBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAIN_LAYOUT.setSpacing(0)

        # ===== TOP BAR =====
        self.TOP_BAR = widget.QFrame(self)
        self.TOP_BAR.setFixedHeight(60)
        self.TOP_BAR.setStyleSheet(styles.SETTINGS_TOP_BAR)

        self.TOP_LAYOUT = widget.QHBoxLayout(self.TOP_BAR)
        self.TOP_LAYOUT.setContentsMargins(24, 10, 24, 10)

        self.TITLE_LABEL = widget.QLabel("Налаштування")
        self.TITLE_LABEL.setStyleSheet(styles.SETTINGS_TITLE)

        self.CLOSE_BUTTON = widget.QPushButton("✕")
        self.CLOSE_BUTTON.setFixedSize(32, 32)
        self.CLOSE_BUTTON.setStyleSheet(styles.SETTINGS_CLOSE_BUTTON)
        self.CLOSE_BUTTON.clicked.connect(self.close)

        self.TOP_LAYOUT.addWidget(self.TITLE_LABEL)
        self.TOP_LAYOUT.addStretch()
        self.TOP_LAYOUT.addWidget(self.CLOSE_BUTTON)

        # ===== CONTENT =====
        self.CONTENT_LAYOUT = widget.QHBoxLayout()
        self.CONTENT_LAYOUT.setContentsMargins(24, 0, 24, 24)
        self.CONTENT_LAYOUT.setSpacing(24)

        # ===== LEFT FRAME =====
        self.LEFT_FRAME = widget.QFrame()
        self.LEFT_FRAME.setFixedWidth(190)
        self.LEFT_FRAME.setStyleSheet(styles.SETTINGS_LEFT_FRAME)

        self.LEFT_LAYOUT = widget.QVBoxLayout(self.LEFT_FRAME)
        self.LEFT_LAYOUT.setContentsMargins(0, 8, 16, 24)
        self.LEFT_LAYOUT.setSpacing(4)
        self.LEFT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        nav_items = [
            "Пошук міста",
            "Розмір додатку",
            "Мова додатку",
            "Списки зображень",
        ]

        self._nav_buttons = []

        for idx, label in enumerate(nav_items):
            btn = NavButton(label)
            btn.clicked.connect(lambda checked, i=idx: self._switch_page(i))
            self.LEFT_LAYOUT.addWidget(btn)
            self._nav_buttons.append(btn)

        self.LEFT_LAYOUT.addStretch()

        # ===== RIGHT FRAME =====
        self.RIGHT_FRAME = widget.QFrame()
        self.RIGHT_FRAME.setStyleSheet(styles.SETTINGS_RIGHT_FRAME)

        self.RIGHT_LAYOUT = widget.QVBoxLayout(self.RIGHT_FRAME)
        self.RIGHT_LAYOUT.setContentsMargins(0, 8, 0, 0)
        self.RIGHT_LAYOUT.setSpacing(0)
        self.RIGHT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        self.PAGE_TITLE = widget.QLabel("")
        self.PAGE_TITLE.setStyleSheet(styles.SETTINGS_PAGE_TITLE)

        self.RIGHT_LAYOUT.addWidget(self.PAGE_TITLE)
        self.RIGHT_LAYOUT.addStretch()

        # ===== СБОРКА =====
        self.CONTENT_LAYOUT.addWidget(self.LEFT_FRAME)
        self.CONTENT_LAYOUT.addWidget(self.RIGHT_FRAME, stretch=1)

        self.MAIN_LAYOUT.addWidget(self.TOP_BAR)
        self.MAIN_LAYOUT.addLayout(self.CONTENT_LAYOUT)

        self._switch_page(0)

    def _switch_page(self, index: int):
        # Очищаем RIGHT_LAYOUT (кроме stretch)
        while self.RIGHT_LAYOUT.count() > 1:
            item = self.RIGHT_LAYOUT.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        if index == 0:
            page = SearchCity()
            self.RIGHT_LAYOUT.insertWidget(0, page.ROOT)
        elif index == 1:
            page = Application()
            self.RIGHT_LAYOUT.insertWidget(0, page.ROOT)
        elif index == 2:
            page = AppLanguage()
            self.RIGHT_LAYOUT.insertWidget(0, page.ROOT)
        else:
            titles = ["", "", "", "Списки зображень"]
            lbl = widget.QLabel(titles[index])
            lbl.setStyleSheet(styles.SETTINGS_PAGE_TITLE)
            self.RIGHT_LAYOUT.insertWidget(0, lbl)

        for i, btn in enumerate(self._nav_buttons):
            btn.setChecked(i == index)
