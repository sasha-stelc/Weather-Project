import sys

# ЦЕ МАЄ БУТИ НА САМОМУ ВЕРХУ, ДО СТВОРЕННЯ QApplication!
from PyQt6.QtWebEngineWidgets import QWebEngineView

import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
import PyQt6.QtGui as gui
import folium
import io
from threading import Thread

from ..api_request import (
    LOAD_USER_CITIES, SEARCH_CITIES, FORMAT_CITY,
    SEARCH_COUNTRIES, GET_CITIES_BY_COUNTRY,
    _LOAD_COUNTRIES_CITIES_CACHE,
    ADD_USER_CITY, REMOVE_USER_CITY, GET_CITY_EN,
)
from .. import styles
from .langueges import LanguageManager
from .size_config import SizeManager


class SearchCity:
    def __init__(self, parent=None):
        self.DESC_PAGE = LanguageManager.get_text("DESC_PAGE_SEARCH")
        self.SELECTED_COUNTRY = None
        self.SELECTED_CITY = None
        self.COUNTRY_CITIES = []

        # ===== ROOT =====
        self.ROOT = widget.QWidget(parent)
        self.ROOT_LAYOUT = widget.QVBoxLayout(self.ROOT)
        self.ROOT_LAYOUT.setContentsMargins(10, 10, 10, 24)
        self.ROOT_LAYOUT.setSpacing(0)
        self.ROOT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        # ===== TITLE =====
        self.PAGE_TITLE = widget.QLabel(LanguageManager.get_text("TITLE_SEARCH_CITY"))
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
        line_style  = styles.SEARCH_LINEEDIT_STYLE
        btn_style   = styles.SEARCH_BUTTON_STYLE

        # COUNTRY
        lbl_country = widget.QLabel(LanguageManager.get_text("LABEL_COUNTRY"))
        lbl_country.setStyleSheet(label_style)
        self.INPUTS_LAYOUT.addWidget(lbl_country,
            alignment=core.Qt.AlignmentFlag.AlignCenter | core.Qt.AlignmentFlag.AlignLeft)

        self.COUNTRY = widget.QLineEdit()
        self.COUNTRY.setStyleSheet(line_style)
        self.COUNTRY.setPlaceholderText(LanguageManager.get_text("PLACEHOLDER_COUNTRY"))
        self.COUNTRY.textChanged.connect(self.ON_COUNTRY_TEXT_CHANGED)
        self.INPUTS_LAYOUT.addWidget(self.COUNTRY,
            alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        # CITY
        lbl_city = widget.QLabel(LanguageManager.get_text("LABEL_CITY"))
        lbl_city.setStyleSheet(label_style)
        self.INPUTS_LAYOUT.addWidget(lbl_city,
            alignment=core.Qt.AlignmentFlag.AlignCenter | core.Qt.AlignmentFlag.AlignLeft)

        self.CITY_SEARCH = widget.QLineEdit()
        self.CITY_SEARCH.setStyleSheet(line_style)
        self.CITY_SEARCH.setPlaceholderText(LanguageManager.get_text("PLACEHOLDER_CITY"))
        self.CITY_SEARCH.textChanged.connect(self.ON_CITY_SEARCH_TEXT_CHANGED)
        self.INPUTS_LAYOUT.addWidget(self.CITY_SEARCH,
            alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        # COORDS
        lbl_coord = widget.QLabel(LanguageManager.get_text("LABEL_COORDINATES"))
        lbl_coord.setStyleSheet(label_style)
        self.INPUTS_LAYOUT.addWidget(lbl_coord,
            alignment=core.Qt.AlignmentFlag.AlignCenter | core.Qt.AlignmentFlag.AlignLeft)

        self.COORDINATES = widget.QLineEdit()
        self.COORDINATES.setStyleSheet(line_style)
        self.COORDINATES.setPlaceholderText(LanguageManager.get_text("PLACEHOLDER_COORDINATES"))
        self.COORDINATES.setReadOnly(True)   # заповнюється автоматично при виборі міста
        self.INPUTS_LAYOUT.addWidget(self.COORDINATES,
            alignment=core.Qt.AlignmentFlag.AlignCenter | core.Qt.AlignmentFlag.AlignLeft)

        # BUTTON
        self.CONFIRM_BUTTON = widget.QPushButton(LanguageManager.get_text("BTN_SAVE"))
        cbtn = SizeManager.get("confirm_button")
        self.CONFIRM_BUTTON.setFixedSize(cbtn["width"], cbtn["height"])
        self.CONFIRM_BUTTON.setStyleSheet(btn_style)
        self.CONFIRM_BUTTON.setEnabled(False)   # активується тільки після вибору міста
        self.CONFIRM_BUTTON.clicked.connect(self.ON_CONFIRM_CLICKED)
        self.INPUTS_LAYOUT.addWidget(self.CONFIRM_BUTTON,
            alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.INPUTS.setSizePolicy(
            widget.QSizePolicy.Policy.Fixed,
            widget.QSizePolicy.Policy.Expanding,
        )

        # ===== MAP =====
        self.MAP_VIEW = QWebEngineView()
        self.MAP_VIEW.setSizePolicy(
            widget.QSizePolicy.Policy.Expanding,
            widget.QSizePolicy.Policy.Expanding,
        )

        self.TOP_LAYOUT.addWidget(self.INPUTS, 0)
        self.TOP_LAYOUT.addWidget(self.MAP_VIEW, 1)
        self.ROOT_LAYOUT.addWidget(self.TOP_PANEL)

        # ===== COUNTRY DROPDOWN =====
        self.COUNTRY_DROPDOWN = widget.QFrame(self.ROOT)
        self.COUNTRY_DROPDOWN.setStyleSheet(styles.SEARCH_DROPDOWN)
        self.COUNTRY_DROPDOWN_LAYOUT = widget.QVBoxLayout(self.COUNTRY_DROPDOWN)
        self.COUNTRY_DROPDOWN_LAYOUT.setContentsMargins(12, 10, 12, 10)
        self.COUNTRY_DROPDOWN_LAYOUT.setSpacing(2)
        self.COUNTRY_DROPDOWN_TITLE = widget.QLabel(LanguageManager.get_text("RESULT_COUNTRIES"))
        self.COUNTRY_DROPDOWN_TITLE.setStyleSheet(styles.DROPDOWN_TITLE)
        self.COUNTRY_DROPDOWN_LAYOUT.addWidget(self.COUNTRY_DROPDOWN_TITLE)
        self.COUNTRY_LIST = widget.QListWidget()
        self.COUNTRY_LIST.setFrameShape(widget.QFrame.Shape.NoFrame)
        self.COUNTRY_LIST.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.COUNTRY_LIST.setStyleSheet(styles.DROPDOWN_LIST)
        self.COUNTRY_LIST.itemClicked.connect(self.ON_COUNTRY_ITEM_SELECTED)
        self.COUNTRY_DROPDOWN_LAYOUT.addWidget(self.COUNTRY_LIST)
        self.COUNTRY_DROPDOWN.hide()
        self.COUNTRY_DROPDOWN.raise_()

        # ===== CITY DROPDOWN =====
        self.SEARCH_DROPDOWN = widget.QFrame(self.ROOT)
        self.SEARCH_DROPDOWN.setStyleSheet(styles.SEARCH_DROPDOWN)
        self.DROPDOWN_LAYOUT = widget.QVBoxLayout(self.SEARCH_DROPDOWN)
        self.DROPDOWN_LAYOUT.setContentsMargins(12, 10, 12, 10)
        self.DROPDOWN_LAYOUT.setSpacing(2)
        self.DROPDOWN_TITLE = widget.QLabel(LanguageManager.get_text("RESULT_CITIES"))
        self.DROPDOWN_TITLE.setStyleSheet(styles.DROPDOWN_TITLE)
        self.DROPDOWN_LAYOUT.addWidget(self.DROPDOWN_TITLE)
        self.DROPDOWN_LIST = widget.QListWidget()
        self.DROPDOWN_LIST.setFrameShape(widget.QFrame.Shape.NoFrame)
        self.DROPDOWN_LIST.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.DROPDOWN_LIST.setStyleSheet(styles.DROPDOWN_LIST)
        self.DROPDOWN_LIST.itemClicked.connect(self.ON_SEARCH_ITEM_SELECTED)
        self.DROPDOWN_LAYOUT.addWidget(self.DROPDOWN_LIST)
        self.SEARCH_DROPDOWN.hide()
        self.SEARCH_DROPDOWN.raise_()

        # ===== ADDED CITIES =====
        self.ADDED_LABEL = widget.QLabel(LanguageManager.get_text("LABEL_ADDED_CITIES"))
        self.ADDED_LABEL.setStyleSheet(styles.SEARCH_ADDED_LABEL_STYLE)
        self.ROOT_LAYOUT.addWidget(self.ADDED_LABEL)

        self.CITIES_LIST = widget.QFrame()
        self.CITIES_LAYOUT = widget.QVBoxLayout(self.CITIES_LIST)

        self.CITY_FRAME = widget.QFrame()
        cf = SizeManager.get("city_frame")
        self.CITY_FRAME.setFixedSize(cf["width"], cf["height"])
        self.CITY_FRAME.setStyleSheet("background: rgba(0, 0, 0, 0.2)")
        self.CITY_LAYOUT = widget.QVBoxLayout(self.CITY_FRAME)

        for city in LOAD_USER_CITIES():
            self._add_city_row(city)

        self.CITY_LAYOUT.addWidget(self.CITIES_LIST)
        self.ROOT_LAYOUT.addWidget(self.CITY_FRAME,
            alignment=core.Qt.AlignmentFlag.AlignLeft)

        # ===== MAP INIT =====
        self._update_map(50.45, 30.52)

        # ===== PRELOAD CACHE =====
        self._preload_cache()

    # ──────────────────────────────────────────────
    def _preload_cache(self):
        def load_cache():
            try:
                _LOAD_COUNTRIES_CITIES_CACHE()
            except Exception as e:
                msg = LanguageManager.get_text("ERROR_CACHE_LOAD", e=e)
                print(msg)
        Thread(target=load_cache, daemon=True).start()

    # ===== COUNTRY SEARCH =====
    def ON_COUNTRY_TEXT_CHANGED(self, text: str):
        text_stripped = text.strip()
        self.SELECTED_COUNTRY = None
        self._reset_city_selection()

        if not text_stripped:
            self.COUNTRY_DROPDOWN.hide()
            return

        try:
            suggestions = SEARCH_COUNTRIES(text_stripped)
        except Exception:
            suggestions = []

        self.COUNTRY_LIST.clear()
        for country in suggestions:
            item = widget.QListWidgetItem(country.get("name", ""))
            item.setData(core.Qt.ItemDataRole.UserRole, country)
            self.COUNTRY_LIST.addItem(item)

        if self.COUNTRY_LIST.count():
            rows    = min(6, self.COUNTRY_LIST.count())
            total_h = rows * 42 + 40
            self.COUNTRY_DROPDOWN.setFixedSize(self.COUNTRY.width(), total_h)
            self._UPDATE_COUNTRY_DROPDOWN_POS()
            self.COUNTRY_DROPDOWN.show()
            self.COUNTRY_DROPDOWN.raise_()
        else:
            self.COUNTRY_DROPDOWN.hide()

    def ON_COUNTRY_ITEM_SELECTED(self, item: widget.QListWidgetItem):
        country = item.data(core.Qt.ItemDataRole.UserRole)
        if not country:
            return
        country_name = country.get("name", "")
        self.COUNTRY.blockSignals(True)
        self.COUNTRY.setText(country_name)
        self.COUNTRY.blockSignals(False)
        self.SELECTED_COUNTRY = country_name
        self.COUNTRY_DROPDOWN.hide()

        self.COUNTRY_CITIES = GET_CITIES_BY_COUNTRY(country_name)
        self._reset_city_selection()
        self.CITY_SEARCH.clear()
        self.CITY_SEARCH.setFocus()

    # ===== CITY SEARCH =====
    def ON_CITY_SEARCH_TEXT_CHANGED(self, text: str):
        text_stripped = text.strip()
        self._reset_city_selection()

        if not text_stripped:
            self.SEARCH_DROPDOWN.hide()
            return

        q = text_stripped.lower()

        if self.SELECTED_COUNTRY and self.COUNTRY_CITIES:
            suggestions = [
                city for city in self.COUNTRY_CITIES
                if city.get("en", "").lower().startswith(q)
                or (len(q) > 2 and q in city.get("en", "").lower())
            ][:6]
        else:
            try:
                suggestions = SEARCH_CITIES(text_stripped)
            except Exception:
                suggestions = []

        self.DROPDOWN_LIST.clear()
        for city in suggestions:
            item = widget.QListWidgetItem(FORMAT_CITY(city))
            item.setData(core.Qt.ItemDataRole.UserRole, city)
            self.DROPDOWN_LIST.addItem(item)

        if self.DROPDOWN_LIST.count():
            rows    = min(6, self.DROPDOWN_LIST.count())
            total_h = rows * 42 + 40
            self.SEARCH_DROPDOWN.setFixedSize(self.CITY_SEARCH.width(), total_h)
            self._UPDATE_DROPDOWN_POS()
            self.SEARCH_DROPDOWN.show()
            self.SEARCH_DROPDOWN.raise_()
        else:
            self.SEARCH_DROPDOWN.hide()

    def ON_SEARCH_ITEM_SELECTED(self, item: widget.QListWidgetItem):
        city = item.data(core.Qt.ItemDataRole.UserRole)
        if not city:
            return

        # Заповнюємо поле пошуку
        self.CITY_SEARCH.blockSignals(True)
        self.CITY_SEARCH.setText(city.get("display", city.get("en", "")))
        self.CITY_SEARCH.blockSignals(False)

        self.SELECTED_CITY = city
        self.SEARCH_DROPDOWN.hide()

        # Оновлюємо поле координат
        lat = city.get("latitude") or city.get("lat")
        lon = city.get("longitude") or city.get("lon")

        if lat and lon:
            try:
                lat_f = float(lat)
                lon_f = float(lon)
                self.COORDINATES.setText(f"{lat_f:.5f}, {lon_f:.5f}")
                
                # Оновлюємо карту
                self._update_map(lat_f, lon_f, city.get("en", ""))
            except (ValueError, TypeError):
                self.COORDINATES.setText("")
                self._update_map()  # на випадок помилки
        else:
            self.COORDINATES.setText("")
            self._update_map()  # показуємо дефолтну карту

        # Активуємо кнопку "Зберегти"
        self.CONFIRM_BUTTON.setEnabled(True)

    # ===== CONFIRM (ЗБЕРЕГТИ) =====
    def ON_CONFIRM_CLICKED(self):
        if not self.SELECTED_CITY:
            return

        city_en = self.SELECTED_CITY.get("en", "").strip()
        if not city_en:
            return

        # Перевіряємо, чи місто вже є в списку UI
        existing = [
            self.CITIES_LAYOUT.itemAt(i).widget()
            for i in range(self.CITIES_LAYOUT.count())
            if self.CITIES_LAYOUT.itemAt(i) and self.CITIES_LAYOUT.itemAt(i).widget()
        ]
        for row_widget in existing:
            if str(row_widget.property("city_en") or "").lower() == city_en.lower():
                return   # вже є — нічого не робимо

        # Зберігаємо в JSON та додаємо рядок у UI
        ADD_USER_CITY(self.SELECTED_CITY)
        self._add_city_row(self.SELECTED_CITY)

        # Скидаємо форму
        self._reset_city_selection()
        self.CITY_SEARCH.clear()
        self.COUNTRY.clear()
        self.SELECTED_COUNTRY = None
        self.COUNTRY_CITIES   = []
        self.CONFIRM_BUTTON.setEnabled(False)

    # ===== HELPERS =====
    def _reset_city_selection(self):
        self.SELECTED_CITY = None
        self.COORDINATES.setText("")
        self.CONFIRM_BUTTON.setEnabled(False)

    def _UPDATE_COUNTRY_DROPDOWN_POS(self):
        g = self.COUNTRY.mapToGlobal(core.QPoint(0, self.COUNTRY.height() + 4))
        p = self.ROOT.mapFromGlobal(g)
        self.COUNTRY_DROPDOWN.move(p)

    def _UPDATE_DROPDOWN_POS(self):
        g = self.CITY_SEARCH.mapToGlobal(core.QPoint(0, self.CITY_SEARCH.height() + 4))
        p = self.ROOT.mapFromGlobal(g)
        self.SEARCH_DROPDOWN.move(p)

    # ===== MAP =====
    def _update_map(self, lat: float = None, lon: float = None, city_name: str = None):
        """Оновлює карту з маркером"""
        # Если координаты передали явно, используем их
        if lat is not None and lon is not None:
            try:
                lat = float(lat)
                lon = float(lon)
            except (ValueError, TypeError):
                lat, lon = 50.45, 30.52  # Київ за замовчуванням
        else:
            # Якщо координати не передали — беремо з вибраного міста
            if self.SELECTED_CITY and ("lat" in self.SELECTED_CITY or "latitude" in self.SELECTED_CITY):
                try:
                    lat = float(self.SELECTED_CITY.get("lat") or self.SELECTED_CITY.get("latitude"))
                    lon = float(self.SELECTED_CITY.get("lon") or self.SELECTED_CITY.get("longitude"))
                except (ValueError, TypeError, KeyError):
                    lat, lon = 50.45, 30.52  # Київ за замовчуванням
            else:
                lat, lon = 50.45, 30.52  # Київ за замовчуванням

        m = folium.Map(location=[lat, lon], zoom_start=10)
        
        # Додаємо маркер
        tooltip = city_name or (self.SELECTED_CITY.get("en", "Вибране місто") if self.SELECTED_CITY else "Місто")
        folium.Marker(
            [lat, lon],
            popup=tooltip,
            tooltip=tooltip
        ).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        self.MAP_VIEW.setHtml(data.getvalue().decode("utf-8"))
    # ===== CITY ROWS =====
    def _add_city_row(self, city):
        row = widget.QFrame()
        row_layout = widget.QHBoxLayout(row)

        city_en = GET_CITY_EN(city)
        city_name = FORMAT_CITY(city) if isinstance(city, dict) else str(city)
        row.setProperty("city_en", city_en)

        label = widget.QLabel(city_name)
        label.setStyleSheet(styles.SEARCH_CITY_LABEL_STYLE)

        delete_btn = widget.QPushButton("🗑")
        db = SizeManager.get("delete_btn")
        delete_btn.setFixedSize(db["width"], db["height"])
        delete_btn.clicked.connect(
            lambda _, r=row, city=city: self._remove_row(r, city)
        )

        row_layout.addWidget(label)
        row_layout.addStretch()
        row_layout.addWidget(delete_btn)

        self.CITIES_LAYOUT.addWidget(row)

    def _remove_row(self, row: widget.QFrame, city):
        REMOVE_USER_CITY(city)
        self.CITIES_LAYOUT.removeWidget(row)
        row.deleteLater()