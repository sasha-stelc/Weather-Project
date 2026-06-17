import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
from .. import styles
from .langueges import LanguageManager
from .size_config import SizeManager, SIZES


class Application(widget.QWidget):
    sizeSelected = core.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.DESC_PAGE = LanguageManager.get_text("DESC_PAGE_SIZE")

        # ===== ЛЕЙАУТ =====
        self.ROOT_LAYOUT = widget.QVBoxLayout(self)
        self.ROOT_LAYOUT.setContentsMargins(0, 0, 0, 16)
        self.ROOT_LAYOUT.setSpacing(16)
        self.ROOT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        # ===== ЗАГОЛОВОК =====
        self.PAGE_TITLE = widget.QLabel(LanguageManager.get_text("TITLE_CHOOSE_SIZE"))
        self.PAGE_TITLE.setStyleSheet(styles.APPLICATION_TITLE_STYLE)
        self.ROOT_LAYOUT.addWidget(self.PAGE_TITLE)

        # ===== РАДІОГРУПА =====
        self.GROUP = widget.QButtonGroup(self)

        # Список пресетів формується з ключів словника SIZES (size_config.py),
        # тож додавання нового пресету достатньо зробити лише там.
        self.SIZES = [
            (key, preset["window"]["width"], preset["window"]["height"])
            for key, preset in SIZES.items()
        ]

        current_key = SizeManager.get_size_key()

        for i, (label, width, height) in enumerate(self.SIZES):
            radio = widget.QRadioButton(label)
            radio.setStyleSheet(styles.APPLICATION_RADIO_STYLE)

            # Правильний спосіб для QRadioButton
            radio.setProperty("window_size", (width, height))
            radio.setProperty("size_key", label)

            if label == current_key:
                radio.setChecked(True)

            self.GROUP.addButton(radio, i)
            self.ROOT_LAYOUT.addWidget(radio)

        self.ROOT_LAYOUT.addSpacing(4)

        # ===== КНОПКА =====
        self.SAVE_BUTTON = widget.QPushButton(LanguageManager.get_text("BTN_SAVE"))
        sb = SizeManager.get("size_save_button")
        self.SAVE_BUTTON.setFixedSize(sb["width"], sb["height"])
        self.SAVE_BUTTON.setStyleSheet(styles.APPLICATION_BUTTON_STYLE)
        self.SAVE_BUTTON.clicked.connect(self._ON_SAVE)
        self.ROOT_LAYOUT.addWidget(self.SAVE_BUTTON)

    def _ON_SAVE(self):
        checked_btn = self.GROUP.checkedButton()
        if not checked_btn:
            return None

        size_data = checked_btn.property("window_size")
        size_key  = checked_btn.property("size_key")

        if isinstance(size_data, tuple) and len(size_data) == 2:
            width, height = size_data

            # Оновлюємо глобальний менеджер розмірів — усі статичні розміри
            # (кнопки, панелі, іконки тощо) перерахуються при наступному
            # створенні/перестворенні віджетів.
            SizeManager.set_size(size_key)

            msg = LanguageManager.get_text("SIZE_SELECTED", text=checked_btn.text(), width=width, height=height)
            print(msg)
            self.sizeSelected.emit(width, height)
            return (width, height)
        else:
            print(LanguageManager.get_text("SIZE_ERROR"))
            return None

    def get_widget(self):
        return self