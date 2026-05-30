import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
from .. import styles


class SearchCity:
    def __init__(self, parent=None):

        self.DESC_PAGE = "Пошук міста"

        # ===== КОРНЕВОЙ ВИДЖЕТ =====
        self.ROOT = widget.QWidget(parent)
        self.ROOT_LAYOUT = widget.QVBoxLayout(self.ROOT)
        self.ROOT_LAYOUT.setContentsMargins(0, 0, 0, 16)
        self.ROOT_LAYOUT.setSpacing(16)
        self.ROOT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        # ===== ЗАГОЛОВОК =====
        self.PAGE_TITLE = widget.QLabel("Пошук міста")
        self.PAGE_TITLE.setStyleSheet(styles.SEARCH_TITLE_STYLE)
        self.ROOT_LAYOUT.addWidget(self.PAGE_TITLE)

        # ===== TOP PANEL (inputs + map) =====
        self.TOP_PANEL = widget.QFrame()
        self.TOP_PAN_LAYOUT = widget.QHBoxLayout(self.TOP_PANEL)
        self.TOP_PAN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TOP_PAN_LAYOUT.setSpacing(16)
        self.TOP_PAN_LAYOUT.setAlignment(
            core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft
        )

        # ===== INPUTS (левая колонка) =====
        self.SERCH_INPUTS = widget.QFrame()
        self.SERCH_INPUTS.setFixedWidth(239)
        self.SERCH_INPUTS_LAYOUT = widget.QVBoxLayout(self.SERCH_INPUTS)
        self.SERCH_INPUTS_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.SERCH_INPUTS_LAYOUT.setSpacing(6)
        self.SERCH_INPUTS_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        LABEL_STYLE = styles.SEARCH_LABEL_STYLE
        COMBOBOX_STYLE = styles.SEARCH_COMBOBOX_STYLE
        LINEEDIT_STYLE = styles.SEARCH_LINEEDIT_STYLE
        BUTTON_STYLE = styles.SEARCH_BUTTON_STYLE

        # Країна
        lbl_country = widget.QLabel("Країна")
        lbl_country.setStyleSheet(LABEL_STYLE)
        self.SERCH_INPUTS_LAYOUT.addWidget(lbl_country)

        self.COUNTRY = widget.QComboBox()
        self.COUNTRY.setFixedSize(239, 32)
        self.COUNTRY.setStyleSheet(COMBOBOX_STYLE)
        self.COUNTRY.addItems(["Виберіть країну", "Україна", "Польща", "Німеччина", "США"])
        self.SERCH_INPUTS_LAYOUT.addWidget(self.COUNTRY)
        self.SERCH_INPUTS_LAYOUT.addSpacing(4)

        # Місто
        lbl_city = widget.QLabel("Місто")
        lbl_city.setStyleSheet(LABEL_STYLE)
        self.SERCH_INPUTS_LAYOUT.addWidget(lbl_city)

        self.CITY = widget.QComboBox()
        self.CITY.setFixedSize(239, 32)
        self.CITY.setStyleSheet(COMBOBOX_STYLE)
        self.CITY.addItems(["Виберіть місто", "Київ", "Львів", "Одеса", "Харків", "Дніпро"])
        self.SERCH_INPUTS_LAYOUT.addWidget(self.CITY)
        self.SERCH_INPUTS_LAYOUT.addSpacing(4)

        # Координати
        lbl_coord = widget.QLabel("Координати")
        lbl_coord.setStyleSheet(LABEL_STYLE)
        self.SERCH_INPUTS_LAYOUT.addWidget(lbl_coord)

        self.COORDINATES = widget.QLineEdit()
        self.COORDINATES.setFixedSize(239, 32)
        self.COORDINATES.setStyleSheet(LINEEDIT_STYLE)
        self.COORDINATES.setPlaceholderText("(WGS 84,UTM,MGRS)")
        self.SERCH_INPUTS_LAYOUT.addWidget(self.COORDINATES)
        self.SERCH_INPUTS_LAYOUT.addSpacing(12)

        # Кнопка
        self.CONFIRM_BUTTON = widget.QPushButton("Зберегти")
        self.CONFIRM_BUTTON.setFixedSize(105, 38)
        self.CONFIRM_BUTTON.setStyleSheet(BUTTON_STYLE)
        self.SERCH_INPUTS_LAYOUT.addWidget(self.CONFIRM_BUTTON)

        # ===== MAP (правая колонка) =====
        self.MAP_PLACEHOLDER = widget.QLabel()
        self.MAP_PLACEHOLDER.setFixedSize(400, 240)
        self.MAP_PLACEHOLDER.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.MAP_PLACEHOLDER.setStyleSheet(styles.SEARCH_MAP_PLACEHOLDER_STYLE)

        self.TOP_PAN_LAYOUT.addWidget(self.SERCH_INPUTS, 0, core.Qt.AlignmentFlag.AlignTop)
        self.TOP_PAN_LAYOUT.addWidget(self.MAP_PLACEHOLDER, 1, core.Qt.AlignmentFlag.AlignTop)

        # ===== ДОДАНІ МІСТА =====
        self.ADDED_LABEL = widget.QLabel("Додані міста")
        self.ADDED_LABEL.setStyleSheet(styles.SEARCH_ADDED_LABEL_STYLE)

        self.CITIES_LIST = widget.QFrame()
        self.CITIES_LIST.setStyleSheet(styles.SEARCH_CITIES_LIST_STYLE)
        self.CITIES_LIST_LAYOUT = widget.QVBoxLayout(self.CITIES_LIST)
        self.CITIES_LIST_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CITIES_LIST_LAYOUT.setSpacing(0)

        for city in ["Київ", "Братіслава", "Варшава", "Рим"]:
            self._add_city_row(city)

        # ===== ЗБІРКА =====
        self.ROOT_LAYOUT.addWidget(self.TOP_PANEL)
        self.ROOT_LAYOUT.addWidget(self.ADDED_LABEL)
        self.ROOT_LAYOUT.addWidget(self.CITIES_LIST)

    def _add_city_row(self, name: str):
        row = widget.QFrame()
        row.setStyleSheet(styles.SEARCH_CITY_ROW_STYLE)
        row_layout = widget.QHBoxLayout(row)
        row_layout.setContentsMargins(12, 10, 12, 10)

        label = widget.QLabel(name)
        label.setStyleSheet(styles.SEARCH_CITY_LABEL_STYLE)

        delete_btn = widget.QPushButton("🗑")
        delete_btn.setFixedSize(24, 24)
        delete_btn.setFlat(True)
        delete_btn.setStyleSheet(styles.SEARCH_DELETE_BUTTON_STYLE)
        delete_btn.clicked.connect(lambda checked, r=row: self._remove_row(r))

        row_layout.addWidget(label)
        row_layout.addStretch()
        row_layout.addWidget(delete_btn)
        self.CITIES_LIST_LAYOUT.addWidget(row)

    def _remove_row(self, row: widget.QFrame):
        self.CITIES_LIST_LAYOUT.removeWidget(row)
        row.deleteLater()