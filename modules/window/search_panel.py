import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from ..create_path import create_media_path
from ..api_request import SEARCH_CITIES, FORMAT_CITY, ADD_USER_CITY
from ..settings.langueges import LanguageManager
from .. import styles


class SearchPanel(widget.QFrame):
    city_selected = core.pyqtSignal(dict)  # Сигнал при выборе города
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(45)
        self.setStyleSheet(styles.SEARCH_FRAME)
        
        self.LAYOUT = widget.QHBoxLayout(self)
        self.LAYOUT.setContentsMargins(8, 0, 8, 0)
        self.LAYOUT.setSpacing(8)
        
        self._SELECTED_CITY = None
        
        # ===== КОНТЕЙНЕР ПОИСКА =====
        self.SEARCH_CONTAINER = widget.QFrame()
        self.SEARCH_CONTAINER.setFixedSize(261, 36)
        self.SEARCH_CONTAINER.setStyleSheet(styles.SEARCH_CONTAINER)
        self.SEARCH_CONTAINER_LAYOUT = widget.QHBoxLayout(self.SEARCH_CONTAINER)
        self.SEARCH_CONTAINER_LAYOUT.setContentsMargins(10, 0, 8, 0)
        self.SEARCH_CONTAINER_LAYOUT.setSpacing(6)
        
        # Иконка поиска
        self.SEARCH_ICON_LBL = widget.QLabel()
        self.SEARCH_ICON_LBL.setFixedSize(18, 18)
        self.SEARCH_ICON_LBL.setStyleSheet(styles.TRANSPARENT_NO_BORDER)
        search_icon_path = create_media_path("search.png")
        if os.path.exists(search_icon_path):
            self.SEARCH_ICON_LBL.setPixmap(
                gui.QPixmap(search_icon_path).scaled(
                    18, 18,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation,
                )
            )
        
        # Поле ввода
        self.CITY_SEARCH = widget.QLineEdit()
        self.CITY_SEARCH.setStyleSheet(styles.CITY_SEARCH)
        self.CITY_SEARCH.setPlaceholderText(LanguageManager.get_text("PLACEHOLDER_SEARCH"))
        self.CITY_SEARCH.textChanged.connect(self._on_search_text_changed)
        
        # Кнопка очистки
        self.CLEAR_BTN = widget.QPushButton()
        self.CLEAR_BTN.setFixedSize(18, 18)
        self.CLEAR_BTN.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.CLEAR_BTN.setStyleSheet(styles.TRANSPARENT_NO_BORDER)
        remove_icon_path = create_media_path("remove.png")
        if os.path.exists(remove_icon_path):
            self.CLEAR_BTN.setIcon(gui.QIcon(remove_icon_path))
            self.CLEAR_BTN.setIconSize(core.QSize(18, 18))
        self.CLEAR_BTN.hide()
        self.CLEAR_BTN.clicked.connect(self._clear_search)
        
        self.SEARCH_CONTAINER_LAYOUT.addWidget(self.SEARCH_ICON_LBL)
        self.SEARCH_CONTAINER_LAYOUT.addWidget(self.CITY_SEARCH)
        self.SEARCH_CONTAINER_LAYOUT.addWidget(self.CLEAR_BTN)
        
        # Кнопка добавления города
        self.ADD_CITY_BTN = widget.QPushButton(LanguageManager.get_text("BTN_ADD_CITY"))
        self.ADD_CITY_BTN.setFixedSize(100, 34)
        self.ADD_CITY_BTN.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.ADD_CITY_BTN.setStyleSheet(styles.ADD_CITY_BUTTON)
        self.ADD_CITY_BTN.hide()
        self.ADD_CITY_BTN.clicked.connect(self._on_add_city_clicked)
        
        self.LAYOUT.addStretch()
        self.LAYOUT.addWidget(self.ADD_CITY_BTN,
            alignment=core.Qt.AlignmentFlag.AlignVCenter)
        self.LAYOUT.addWidget(self.SEARCH_CONTAINER,
            alignment=core.Qt.AlignmentFlag.AlignVCenter)
        
        # ===== DROPDOWN =====
        self.SEARCH_DROPDOWN = widget.QFrame(parent)
        self.SEARCH_DROPDOWN.setStyleSheet(styles.SEARCH_DROPDOWN)
        self.DROPDOWN_LAYOUT = widget.QVBoxLayout(self.SEARCH_DROPDOWN)
        self.DROPDOWN_LAYOUT.setContentsMargins(12, 10, 12, 10)
        self.DROPDOWN_LAYOUT.setSpacing(2)
        
        self.DROPDOWN_TITLE = widget.QLabel(LanguageManager.get_text("RESULT_SEARCH"))
        self.DROPDOWN_TITLE.setStyleSheet(styles.DROPDOWN_TITLE)
        self.DROPDOWN_LAYOUT.addWidget(self.DROPDOWN_TITLE)
        
        self.DROPDOWN_LIST = widget.QListWidget()
        self.DROPDOWN_LIST.setFrameShape(widget.QFrame.Shape.NoFrame)
        self.DROPDOWN_LIST.setVerticalScrollBarPolicy(
            core.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.DROPDOWN_LIST.setStyleSheet(styles.DROPDOWN_LIST)
        self.DROPDOWN_LIST.itemClicked.connect(self._on_search_item_selected)
        self.DROPDOWN_LAYOUT.addWidget(self.DROPDOWN_LIST)
        self.SEARCH_DROPDOWN.hide()
        self.SEARCH_DROPDOWN.raise_()
    
    def _on_search_text_changed(self, text: str):
        """Обработчик изменения текста в поиске."""
        text_stripped = text.strip()
        self.CLEAR_BTN.setVisible(bool(text_stripped))
        self._SELECTED_CITY = None
        self.ADD_CITY_BTN.hide()
        if not text_stripped:
            self.SEARCH_DROPDOWN.hide()
            return
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
            self.SEARCH_DROPDOWN.setFixedSize(self.SEARCH_CONTAINER.width(), total_h)
            self._update_dropdown_pos()
            self.SEARCH_DROPDOWN.show()
            self.SEARCH_DROPDOWN.raise_()
        else:
            self.SEARCH_DROPDOWN.hide()
    
    def _on_search_item_selected(self, item: widget.QListWidgetItem):
        """Обработчик выбора элемента из дропдауна."""
        city = item.data(core.Qt.ItemDataRole.UserRole)
        if not city:
            return
        self.CITY_SEARCH.blockSignals(True)
        self.CITY_SEARCH.setText(city.get("en", ""))
        self.CITY_SEARCH.blockSignals(False)
        self._SELECTED_CITY = city
        self.SEARCH_DROPDOWN.hide()
        self.ADD_CITY_BTN.show()
    
    def _update_dropdown_pos(self):
        """Обновляет позицию дропдауна."""
        g = self.SEARCH_CONTAINER.mapToGlobal(
            core.QPoint(0, self.SEARCH_CONTAINER.height() + 4))
        parent = self.SEARCH_DROPDOWN.parent()
        if parent:
            p = parent.mapFromGlobal(g)
            self.SEARCH_DROPDOWN.move(p)
    
    def _clear_search(self):
        """Очищает поиск."""
        self.CITY_SEARCH.clear()
        self.SEARCH_DROPDOWN.hide()
        self.ADD_CITY_BTN.hide()
        self._SELECTED_CITY = None
    
    def _on_add_city_clicked(self):
        """Обработчик добавления города."""
        if not self._SELECTED_CITY:
            return
        city_en = self._SELECTED_CITY.get("en", "")
        if not city_en:
            return
        
        # Сохраняем город перед очисткой
        selected_city = self._SELECTED_CITY
        
        # Сохраняем город и очищаем поиск
        ADD_USER_CITY(city_en)
        self._clear_search()
        
        # Испускаем сигнал с сохраненным городом
        self.city_selected.emit(selected_city)
    
    def get_selected_city(self):
        """Возвращает выбранный город."""
        return self._SELECTED_CITY
    
    def get_search_text(self):
        """Возвращает текст поиска."""
        return self.CITY_SEARCH.text()
