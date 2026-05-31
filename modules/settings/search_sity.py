import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
import folium
import io
from ..api_request import LOAD_USER_CITIES
from PyQt6.QtWebEngineWidgets import QWebEngineView
from .. import styles


class SearchCity:
    def __init__(self, parent=None):
        self.DESC_PAGE = "Пошук міста"

        # ===== ROOT =====
        self.ROOT = widget.QWidget(parent)
        self.ROOT_LAYOUT = widget.QVBoxLayout(self.ROOT)
        self.ROOT_LAYOUT.setContentsMargins(10, 10, 10, 24)
        self.ROOT_LAYOUT.setSpacing(0)
        self.ROOT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        # ===== TITLE =====
        self.PAGE_TITLE = widget.QLabel("Пошук міста")
        self.PAGE_TITLE.setStyleSheet(styles.SEARCH_TITLE_STYLE)
        self.ROOT_LAYOUT.addWidget(self.PAGE_TITLE)

        # ===== TOP PANEL =====
        self.TOP_PANEL = widget.QFrame()
        self.TOP_LAYOUT = widget.QHBoxLayout(self.TOP_PANEL)
        self.TOP_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TOP_LAYOUT.setSpacing(0)

        # ===== LEFT INPUTS =====
        self.INPUTS = widget.QFrame()
        self.INPUTS_LAYOUT = widget.QVBoxLayout(self.INPUTS)
        self.INPUTS_LAYOUT.setContentsMargins(10, 16, 16, 16)
        self.INPUTS_LAYOUT.setSpacing(8)

        label_style = styles.SEARCH_LABEL_STYLE
        combo_style = styles.SEARCH_COMBOBOX_STYLE
        line_style = styles.SEARCH_LINEEDIT_STYLE
        btn_style = styles.SEARCH_BUTTON_STYLE

        # COUNTRY
        lbl_country = widget.QLabel("Країна")
        lbl_country.setStyleSheet(label_style)
        self.INPUTS_LAYOUT.addWidget(lbl_country, alignment=core.Qt.AlignmentFlag.AlignCenter | core.Qt.AlignmentFlag.AlignLeft)

        self.COUNTRY = widget.QComboBox()
        self.COUNTRY.setStyleSheet(combo_style)
        self.COUNTRY.addItems(["Виберіть країну", "Україна", "Польща", "Німеччина", "США"])
        self.INPUTS_LAYOUT.addWidget(self.COUNTRY, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        # CITY
        lbl_city = widget.QLabel("Місто")
        lbl_city.setStyleSheet(label_style)
        self.INPUTS_LAYOUT.addWidget(lbl_city, alignment=core.Qt.AlignmentFlag.AlignCenter | core.Qt.AlignmentFlag.AlignLeft)

        self.CITY = widget.QComboBox()
        self.CITY.setStyleSheet(combo_style)
        self.CITY.addItems(["Виберіть місто", "Київ", "Львів", "Одеса", "Харків", "Дніпро"])
        self.INPUTS_LAYOUT.addWidget(self.CITY, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        # COORDS
        lbl_coord = widget.QLabel("Координати")
        lbl_coord.setStyleSheet(label_style)
        self.INPUTS_LAYOUT.addWidget(lbl_coord, alignment=core.Qt.AlignmentFlag.AlignCenter | core.Qt.AlignmentFlag.AlignLeft)

        self.COORDINATES = widget.QLineEdit()
        self.COORDINATES.setStyleSheet(line_style)
        self.COORDINATES.setPlaceholderText("lat, lon")
        self.INPUTS_LAYOUT.addWidget(self.COORDINATES, alignment=core.Qt.AlignmentFlag.AlignCenter | core.Qt.AlignmentFlag.AlignLeft)

        # BUTTON
        self.CONFIRM_BUTTON = widget.QPushButton("Зберегти")
        self.CONFIRM_BUTTON.setFixedSize(105, 38)
        self.CONFIRM_BUTTON.setStyleSheet(btn_style)
        self.INPUTS_LAYOUT.addWidget(self.CONFIRM_BUTTON, alignment= core.Qt.AlignmentFlag.AlignLeft)

        self.INPUTS.setSizePolicy(
            widget.QSizePolicy.Policy.Fixed,
            widget.QSizePolicy.Policy.Expanding
        )

        # ===== MAP =====
        self.MAP_VIEW = QWebEngineView()

        self.MAP_VIEW.setSizePolicy(
            widget.QSizePolicy.Policy.Expanding,
            widget.QSizePolicy.Policy.Expanding
        )

        # layout split
        self.TOP_LAYOUT.addWidget(self.INPUTS, 0)
        self.TOP_LAYOUT.addWidget(self.MAP_VIEW, 1)

        self.ROOT_LAYOUT.addWidget(self.TOP_PANEL)

        # ===== ADDED CITIES =====
        self.ADDED_LABEL = widget.QLabel("Додані міста")
        self.ADDED_LABEL.setStyleSheet(styles.SEARCH_ADDED_LABEL_STYLE)
        self.ROOT_LAYOUT.addWidget(self.ADDED_LABEL)

        self.CITIES_LIST = widget.QFrame()
        self.CITIES_LAYOUT = widget.QVBoxLayout(self.CITIES_LIST)

        self.CITY_FRAME = widget.QFrame()
        self.CITY_FRAME.setFixedSize(544, 160)
        self.CITY_FRAME.setStyleSheet("background: rgba(0, 0, 0, 0.2)")

        self.CITY_LAYOUT = widget.QVBoxLayout(self.CITY_FRAME)

        us_cities = LOAD_USER_CITIES()

        for city in us_cities:
            self._add_city_row(city)

        self.CITY_LAYOUT.addWidget(self.CITIES_LIST)
        self.ROOT_LAYOUT.addWidget(self.CITY_FRAME, alignment=core.Qt.AlignmentFlag.AlignLeft)

        # ===== MAP INIT (FOLIUM) =====
        self._update_map(50.45, 30.52)

    # ===== MAP GENERATION =====
    def _update_map(self, lat: float, lon: float):
        m = folium.Map(location=[lat, lon], zoom_start=6)

        data = io.BytesIO()
        m.save(data, close_file=False)

        html = data.getvalue().decode("utf-8")

        self.MAP_VIEW.setHtml(html)

    # ===== CITY ROW =====
    def _add_city_row(self, name: str):
        row = widget.QFrame()
        row_layout = widget.QHBoxLayout(row)

        label = widget.QLabel(name)
        label.setStyleSheet(styles.SEARCH_CITY_LABEL_STYLE)

        delete_btn = widget.QPushButton("🗑")
        delete_btn.setFixedSize(24, 24)

        delete_btn.clicked.connect(lambda _, r=row: self._remove_row(r))

        row_layout.addWidget(label)
        row_layout.addStretch()
        row_layout.addWidget(delete_btn)

        self.CITIES_LAYOUT.addWidget(row)

    def _remove_row(self, row: widget.QFrame):
        self.CITIES_LAYOUT.removeWidget(row)
        row.deleteLater()