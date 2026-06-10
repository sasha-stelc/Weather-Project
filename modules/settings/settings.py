import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
from .search_sity import SearchCity
from .application_size import Application
from .langueges import AppLanguage, LanguageManager
from .. import styles


class NavButton(widget.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(35)
        self.setMinimumWidth(140)
        self.setSizePolicy(widget.QSizePolicy.Policy.Expanding, widget.QSizePolicy.Policy.Fixed)
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
    def __init__(self, parent=None, main_app=None):
        super().__init__(parent)
        self.main_app = main_app
        self.search_city_page = None  # Сохраняем ссылку на SearchCity
        self._pending_map_update = None  # Для отложенного обновления карты

        self.resize(790, 688)
        self.setAttribute(core.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(styles.SETTINGS_MAIN)

        # ===== MAIN LAYOUT =====
        self.MAIN_LAYOUT = widget.QVBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAIN_LAYOUT.setSpacing(0)

        # ===== TOP BAR =====
        self.TOP_BAR = widget.QFrame(self)
        self.TOP_BAR.setMinimumHeight(60)
        self.TOP_BAR.setSizePolicy(widget.QSizePolicy.Policy.Expanding, widget.QSizePolicy.Policy.Fixed)
        self.TOP_BAR.setStyleSheet(styles.SETTINGS_TOP_BAR)

        self.TOP_LAYOUT = widget.QHBoxLayout(self.TOP_BAR)
        self.TOP_LAYOUT.setContentsMargins(24, 10, 24, 10)

        self.TITLE_LABEL = widget.QLabel(LanguageManager.get_text("TITLE_SETTINGS"))
        self.TITLE_LABEL.setStyleSheet(styles.SETTINGS_TITLE)

        self.CLOSE_BUTTON = widget.QPushButton(LanguageManager.get_text("BTN_CLOSE"))
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
        self.LEFT_FRAME.setMinimumWidth(190)
        self.LEFT_FRAME.setSizePolicy(widget.QSizePolicy.Policy.Fixed, widget.QSizePolicy.Policy.Expanding)
        self.LEFT_FRAME.setStyleSheet(styles.SETTINGS_LEFT_FRAME)

        self.LEFT_LAYOUT = widget.QVBoxLayout(self.LEFT_FRAME)
        self.LEFT_LAYOUT.setContentsMargins(0, 8, 16, 24)
        self.LEFT_LAYOUT.setSpacing(4)
        self.LEFT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        nav_items = [
            LanguageManager.get_text("NAV_SEARCH_CITY"),
            LanguageManager.get_text("NAV_APP_SIZE"),
            LanguageManager.get_text("NAV_LANGUAGE"),
            LanguageManager.get_text("NAV_IMAGE_LISTS"),
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
        # self.RIGHT_LAYOUT.addStretch()

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
            self.search_city_page = page  # Сохраняем ссылку на SearchCity
            self.RIGHT_LAYOUT.insertWidget(0, page.ROOT)
            # Запускаем отложенное обновление карты, если были переданы координаты
            if hasattr(self, '_pending_map_update') and self._pending_map_update:
                lat, lon, city_name = self._pending_map_update
                core.QTimer.singleShot(300, lambda: self.update_map_for_city(lat, lon, city_name))
                self._pending_map_update = None
        elif index == 1:
            page = Application()
            if self.main_app:
                page.sizeSelected.connect(self.main_app.APPLY_WINDOW_SIZE)
            self.RIGHT_LAYOUT.insertWidget(0, page)
        elif index == 2:
            page = AppLanguage()
            # Подключаем кнопку "Зберегти" для изменения языка
            page.CONFIRM_BUTTON.clicked.connect(self._on_language_changed)
            self.RIGHT_LAYOUT.insertWidget(0, page.ROOT)
        else:
            lbl = widget.QLabel(LanguageManager.get_text("PAGE_IMAGE_LISTS"))
            lbl.setStyleSheet(styles.SETTINGS_PAGE_TITLE)
            self.RIGHT_LAYOUT.insertWidget(0, lbl)

        for i, btn in enumerate(self._nav_buttons):
            btn.setChecked(i == index)
    
    def _on_language_changed(self):
        """Обработчик изменения языка"""
        # Получаем языковую страницу
        from .langueges import AppLanguage as AppLanguageClass
        for i in range(self.RIGHT_LAYOUT.count()):
            widget_item = self.RIGHT_LAYOUT.itemAt(i).widget()
            if isinstance(widget_item, widget.QWidget):
                # Ищем комбобокс в иерархии виджетов
                combo = self._find_combo_in_widget(widget_item)
                if combo:
                    lang_index = combo.currentIndex()
                    lang_map = {0: "uk", 1: "ru", 2: "en"}
                    new_lang = lang_map.get(lang_index, "uk")
                    LanguageManager.set_language(new_lang)
                    
                    # Обновляем все текстовые элементы интерфейса настроек
                    self._update_ui_language()
                    
                    # Сигнализируем главному окну об изменении языка
                    if self.main_app and hasattr(self.main_app, 'on_language_changed'):
                        self.main_app.on_language_changed()
                    break
    
    def _find_combo_in_widget(self, parent_widget):
        """Рекурсивно ищет QComboBox в иерархии виджетов"""
        if isinstance(parent_widget, widget.QComboBox):
            return parent_widget
        
        if hasattr(parent_widget, 'findChild'):
            combo = parent_widget.findChild(widget.QComboBox)
            if combo:
                return combo
        
        return None
    
    def _update_ui_language(self):
        """Обновляет текстовые элементы интерфейса настроек"""
        # Обновляем заголовок
        self.TITLE_LABEL.setText(LanguageManager.get_text("TITLE_SETTINGS"))
        
        # Обновляем кнопки навигации
        nav_texts = [
            LanguageManager.get_text("NAV_SEARCH_CITY"),
            LanguageManager.get_text("NAV_APP_SIZE"),
            LanguageManager.get_text("NAV_LANGUAGE"),
            LanguageManager.get_text("NAV_IMAGE_LISTS"),
        ]
        for btn, text in zip(self._nav_buttons, nav_texts):
            btn.setText(text)
    
    def update_map_for_city(self, lat: float, lon: float, city_name: str = None):
        """Обновляет карту на странице поиска города."""
        if self.search_city_page:
            self.search_city_page._update_map(lat, lon, city_name)
        else:
            # Если страница еще не создана, сохраняем данные для отложенного обновления
            self._pending_map_update = (lat, lon, city_name)
