import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
from .. import styles


class Application(widget.QWidget):
    sizeSelected = core.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.DESC_PAGE = "Розмір додатку"

        # ===== ЛЕЙАУТ =====
        self.ROOT_LAYOUT = widget.QVBoxLayout(self)
        self.ROOT_LAYOUT.setContentsMargins(0, 0, 0, 16)
        self.ROOT_LAYOUT.setSpacing(16)
        self.ROOT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        # ===== ЗАГОЛОВОК =====
        self.PAGE_TITLE = widget.QLabel("Оберіть розмір додатку")
        self.PAGE_TITLE.setStyleSheet(styles.APPLICATION_TITLE_STYLE)
        self.ROOT_LAYOUT.addWidget(self.PAGE_TITLE)

        # ===== РАДІОГРУПА =====
        self.GROUP = widget.QButtonGroup(self)

        self.SIZES = [
            ("1200x800", 1200, 800),
            ("1440x1024", 1440, 1024),
            ("1512x982", 1512, 982),
            ("1728x1117", 1728, 1117),
            ("1920x1080", 1920, 1080),
            
        ]

        for i, (label, width, height) in enumerate(self.SIZES):
            radio = widget.QRadioButton(label)
            radio.setStyleSheet(styles.APPLICATION_RADIO_STYLE)
            
            # Правильний спосіб для QRadioButton
            radio.setProperty("window_size", (width, height))
            
            if i == 0:
                radio.setChecked(True)
                
            self.GROUP.addButton(radio, i)
            self.ROOT_LAYOUT.addWidget(radio)

        self.ROOT_LAYOUT.addSpacing(4)

        # ===== КНОПКА =====
        self.SAVE_BUTTON = widget.QPushButton("Зберегти")
        self.SAVE_BUTTON.setFixedSize(105, 38)
        self.SAVE_BUTTON.setStyleSheet(styles.APPLICATION_BUTTON_STYLE)
        self.SAVE_BUTTON.clicked.connect(self._ON_SAVE)
        self.ROOT_LAYOUT.addWidget(self.SAVE_BUTTON)

    def _ON_SAVE(self):
        checked_btn = self.GROUP.checkedButton()
        if not checked_btn:
            return None

        size_data = checked_btn.property("window_size")
        
        if isinstance(size_data, tuple) and len(size_data) == 2:
            width, height = size_data
            print(f"Обрано розмір: {checked_btn.text()} ({width}x{height})")
            self.sizeSelected.emit(width, height)
            return (width, height)
        else:
            print("❌ Помилка: не вдалося отримати розмір")
            return None

    def get_widget(self):
        return self