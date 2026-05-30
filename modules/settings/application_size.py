import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
from .. import styles


class Application:
    def __init__(self, parent=None):

        self.DESC_PAGE = "Розмір додатку"

        TITLE_STYLE = styles.APPLICATION_TITLE_STYLE
        RADIO_STYLE = styles.APPLICATION_RADIO_STYLE
        BUTTON_STYLE = styles.APPLICATION_BUTTON_STYLE

        # ===== КОРНЕВОЙ ВИДЖЕТ =====
        self.ROOT = widget.QWidget(parent)
        self.ROOT_LAYOUT = widget.QVBoxLayout(self.ROOT)
        self.ROOT_LAYOUT.setContentsMargins(0, 0, 0, 16)
        self.ROOT_LAYOUT.setSpacing(16)
        self.ROOT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        # ===== ЗАГОЛОВОК =====
        self.PAGE_TITLE = widget.QLabel("Оберіть розмір додатку")
        self.PAGE_TITLE.setStyleSheet(TITLE_STYLE)
        self.ROOT_LAYOUT.addWidget(self.PAGE_TITLE)

        # ===== РАДИОКНОПКИ =====
        self.GROUP = widget.QButtonGroup(self.ROOT)

        sizes = ["1200x800", "1440x1024", "1512x982", "1728x1117"]

        for i, size in enumerate(sizes):
            radio = widget.QRadioButton(size)
            radio.setStyleSheet(RADIO_STYLE)
            if i == 0:
                radio.setChecked(True)
            self.GROUP.addButton(radio, i)
            self.ROOT_LAYOUT.addWidget(radio)

        self.ROOT_LAYOUT.addSpacing(4)

        # ===== КНОПКА =====
        self.SAVE_BUTTON = widget.QPushButton("Зберегти")
        self.SAVE_BUTTON.setFixedSize(105, 38)
        self.SAVE_BUTTON.setStyleSheet(BUTTON_STYLE)
        self.SAVE_BUTTON.clicked.connect(self._on_save)
        self.ROOT_LAYOUT.addWidget(self.SAVE_BUTTON)

    def _on_save(self):
        btn = self.GROUP.checkedButton()
        if btn:
            print(f"Обрано розмір: {btn.text()}")
            return btn.text()
        return None