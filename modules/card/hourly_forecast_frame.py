import os
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWidgets as widget

from ..create_path import create_media_path
from ..settings.langueges import LanguageManager
from ..settings.size_config import SizeManager
from .. import styles
from .utils import get_weather_icon_path


class HourlyForecastFrame(widget.QFrame):
    """Виджет горизонтального почасового прогноза погоды.

    Предоставляет пользователю адаптивную прокручиваемую панель с карточками 
    прогноза на ближайшие 12 часов. Также автоматически интегрирует в хронологическую 
    линию времени астрономические события (восход и закат солнца). Управление 
    прокруткой осуществляется боковыми кнопками-стрелками, состояние которых 
    (активность и прозрачность) динамически изменяется в зависимости от положения ползунка.
    """
    
    def __init__(self, data: dict, parent=None):
        """Инициализирует контейнеры интерфейса и генерирует почасовые элементы.

        Args:
            data (dict): Словарь с распарсенными данными погоды. Ожидает наличие 
                         ключей "desc" (строка описания) и "today_hours" (список словарей).
            parent (QWidget, optional): Родительский компонент. Defaults to None.
        """
        super().__init__(parent)
        
        # Фиксируем высоту виджета, чтобы он гармонично вписывался в интерфейс,
        # и настраиваем полупрозрачный закругленный фон.
        self.setFixedHeight(SizeManager.get("hourly_forecast_height"))
        self.setStyleSheet(styles.HOURLY_FORECAST_FRAME)

        # Инициализируем главный вертикальный контейнер для виджета
        self.MAIN_LAYOUT = widget.QVBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(15, 12, 15, 12)
        self.MAIN_LAYOUT.setSpacing(0)

        # Текстовый заголовок с общим описанием погоды (например, "Хмарна погода до кінця дня")
        self.TITLE_LBL = widget.QLabel(data.get("desc", "Хмарна погода до кінця дня"))
        self.TITLE_LBL.setStyleSheet(styles.HOURLY_TITLE)
        self.MAIN_LAYOUT.addWidget(self.TITLE_LBL)

        # Декоративная тонкая разделительная линия между заголовком и областью прогноза
        self.LINE = widget.QFrame()
        self.LINE.setFixedHeight(SizeManager.get("hourly_line_height"))
        self.LINE.setStyleSheet(styles.HOURLY_LINE)
        self.MAIN_LAYOUT.addWidget(self.LINE)

        # Горизонтальный контейнер, объединяющий левую стрелку, прокрутку и правую стрелку
        self.H_CONTAINER = widget.QHBoxLayout()
        self.H_CONTAINER.setSpacing(4)

        # --- ЛЕВАЯ СТРЕЛКА НАВИГАЦИИ ---
        self.L_ARROW = widget.QPushButton()
        ha = SizeManager.get("hourly_arrow")
        self.L_ARROW.setFixedSize(ha["width"], ha["height"])
        self.L_ARROW.setCursor(core.Qt.CursorShape.PointingHandCursor)  # Курсор руки при наведении
        self.L_ARROW.setStyleSheet(styles.HOURLY_ARROW_BUTTON)
        l_icon_path = create_media_path("less_vector.png")
        
        if os.path.exists(l_icon_path):
            self.L_ARROW.setIcon(gui.QIcon(l_icon_path))
            hai = SizeManager.get("hourly_arrow_icon")
            self.L_ARROW.setIconSize(core.QSize(hai["width"], hai["height"]))
        else:
            # Текстовый аналог, если файл векторного изображения отсутствует в медиа-папке
            self.L_ARROW.setText("<")
            self.L_ARROW.setStyleSheet(styles.HOURLY_ARROW_TEXT)

        # Наложение эффекта прозрачности. По умолчанию прокрутка находится в крайнем левом положении, 
        # поэтому левая стрелка инициализируется неактивной (opacity 0.3) и выключенной.
        self.L_EFFECT = widget.QGraphicsOpacityEffect(self.L_ARROW)
        self.L_EFFECT.setOpacity(0.3)
        self.L_ARROW.setGraphicsEffect(self.L_EFFECT)
        self.L_ARROW.setEnabled(False)

        self.H_CONTAINER.addWidget(self.L_ARROW)

        # --- СЛУЖЕБНАЯ ОБЛАСТЬ ПРОКРУТКИ (QScrollArea) ---
        self.SCROLL = widget.QScrollArea()
        self.SCROLL.setWidgetResizable(True)  # Разрешает внутреннему контейнеру адаптироваться под размеры
        self.SCROLL.setFrameShape(widget.QFrame.Shape.NoFrame)  # Убираем дефолтную квадратную рамку
        
        # Полностью скрываем встроенные ползунки прокрутки, управление будет идти только через стрелки
        self.SCROLL.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL.setStyleSheet(styles.TRANSPARENT_BG)

        # Внутренний контейнер-виджет, который физически будет содержать в себе все 12 часовых ячеек
        self.CONTENT = widget.QWidget()
        self.CONTENT.setStyleSheet(styles.TRANSPARENT_BG)
        self.CONTENT_LAYOUT = widget.QHBoxLayout(self.CONTENT)
        self.CONTENT_LAYOUT.setContentsMargins(5, 0, 5, 0)
        self.CONTENT_LAYOUT.setSpacing(25)  # Расстояние между почасовыми ячейками

        # --- ДИНАМИЧЕСКАЯ ГЕНЕРАЦИЯ ЧАСОВЫХ ЯЧЕЕК ---
        for item in data.get("today_hours", []):
            hour_widget = widget.QWidget()
            hour_layout = widget.QVBoxLayout(hour_widget)
            hour_layout.setContentsMargins(0, 5, 0, 5)
            hour_layout.setSpacing(8)

            # Определение текста времени: заменяем точное время на слово "Зараз" для текущего часа
            time_str = LanguageManager.get_text("TEXT_NOW") if item.get("is_current") else item["time"]
            t_lbl = widget.QLabel(time_str)
            t_lbl.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            t_lbl.setStyleSheet(styles.HOURLY_ITEM_TIME)

            # Рендеринг иконки погоды/события солнца
            i_lbl = widget.QLabel()
            # Если это точка рассвета или заката, подставляем кастомные строковые коды иконок
            icon_code = "sunset" if item.get("is_sunset") else "sunrise" if item.get("is_sunrise") else item["icon"]
            icon_path = get_weather_icon_path(icon_code)
            
            if os.path.exists(icon_path):
                # Пропорционально сжимаем иконку до размера 32x32 пикселя с использованием качественного сглаживания
                pix = gui.QPixmap(icon_path).scaled(
                    32, 32,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation
                )
                i_lbl.setPixmap(pix)
            i_lbl.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

            # Определение нижнего текстового поля ячейки: температура или текстовый флаг события солнца
            if item.get("is_sunset"):
                temp_val = LanguageManager.get_text("TEXT_SUNSET")
            elif item.get("is_sunrise"):
                temp_val = LanguageManager.get_text("TEXT_SUNRISE")
            else:
                temp_val = f"{item['temp']}°"
            temp_lbl = widget.QLabel(temp_val)
            temp_lbl.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            temp_lbl.setStyleSheet(styles.HOURLY_ITEM_TEMP)

            # Расширяем ячейку для рассвета/заката, так как надписи "Захід сонця" требуют больше пространства, чем "18°"
            if item.get("is_sunset") or item.get("is_sunrise"):
                hour_widget.setMinimumWidth(SizeManager.get("hourly_item_min_width"))

            # Собираем ячейку по вертикали и добавляем ее в общий горизонтальный ряд
            hour_layout.addWidget(t_lbl)
            hour_layout.addWidget(i_lbl)
            hour_layout.addWidget(temp_lbl)
            self.CONTENT_LAYOUT.addWidget(hour_widget)

        # Привязываем заполненный контейнер к области прокрутки
        self.SCROLL.setWidget(self.CONTENT)
        self.H_CONTAINER.addWidget(self.SCROLL)

        # --- ПРАВАЯ СТРЕЛКА НАВИГАЦИИ ---
        self.R_ARROW = widget.QPushButton()
        self.R_ARROW.setFixedSize(ha["width"], ha["height"])
        self.R_ARROW.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.R_ARROW.setStyleSheet(styles.HOURLY_ARROW_BUTTON)
        r_icon_path = create_media_path("more_vector.png")
        
        if os.path.exists(r_icon_path):
            self.R_ARROW.setIcon(gui.QIcon(r_icon_path))
            self.R_ARROW.setIconSize(core.QSize(hai["width"], hai["height"]))
        else:
            self.R_ARROW.setText(">")
            self.R_ARROW.setStyleSheet(styles.HOURLY_ARROW_TEXT)

        # Инициализируем правую стрелку полностью видимой (в начале списка всегда есть куда крутить вправо)
        self.R_EFFECT = widget.QGraphicsOpacityEffect(self.R_ARROW)
        self.R_EFFECT.setOpacity(1.0)
        self.R_ARROW.setGraphicsEffect(self.R_EFFECT)

        self.H_CONTAINER.addWidget(self.R_ARROW)
        self.MAIN_LAYOUT.addLayout(self.H_CONTAINER)

        # --- СИГНАЛЫ И СЛОТЫ (Логика интерактивности) ---
        # Подключение кликов мыши к методам смещения скроллбара
        self.L_ARROW.clicked.connect(self._scroll_left)
        self.R_ARROW.clicked.connect(self._scroll_right)
        
        # Подключение события изменения положения ползунка к валидатору состояния стрелок
        self.SCROLL.horizontalScrollBar().valueChanged.connect(self._on_scroll_changed)

    def _set_arrow_opacity(self, effect: widget.QGraphicsOpacityEffect, active: bool):
        """Вспомогательный метод для изменения прозрачности графического эффекта кнопки.

        Args:
            effect (QGraphicsOpacityEffect): Целевой эффект прозрачности кнопки.
            active (bool): Статус активности кнопки. True — 100% видимость, False — 30% видимость.
        """
        effect.setOpacity(1.0 if active else 0.3)

    def _scroll_left(self):
        """Смещает ползунок горизонтальной прокрутки влево на шаг в 150 пикселей."""
        bar = self.SCROLL.horizontalScrollBar()
        bar.setValue(bar.value() - 150)

    def _scroll_right(self):
        """Смещает ползунок горизонтальной прокрутки вправо на шаг в 150 пикселей."""
        bar = self.SCROLL.horizontalScrollBar()
        bar.setValue(bar.value() + 150)

    def _on_scroll_changed(self, value: int):
        """Реагирует на ручное или программное изменение положения ползунка прокрутки.

        Проверяет, достиг ли ползунок левой границы (минимума) или правой 
        границы (максимума). В зависимости от этого включает или отключает кнопки, 
        а также меняет их прозрачность.

        Args:
            value (int): Текущее пиксельное положение ползунка прокрутки.
        """
        bar      = self.SCROLL.horizontalScrollBar()
        at_start = value <= bar.minimum()  # Находимся ли мы в самом начале списка
        at_end   = value >= bar.maximum()  # Достигли ли мы самого конца списка

        # Управление левой стрелкой
        self.L_ARROW.setEnabled(not at_start)
        self._set_arrow_opacity(self.L_EFFECT, not at_start)

        # Управление правой стрелкой
        self.R_ARROW.setEnabled(not at_end)
        self._set_arrow_opacity(self.R_EFFECT, not at_end)
    def retranslate(self, lang=None):
        """Обновляет все переводимые строки при смене языка"""
        self.TITLE_LBL.setText(LanguageManager.get_text("TEXT_TODAY_HOURS"))
        self._on_scroll_changed(self.SCROLL.horizontalScrollBar().value())  # Обновляем состояние стрелок при смене языка
        self._update_hourly_items_text()  # Обновляем текст внутри часовых ячеек (например, "Зараз", "Захід сонця", "Схід сонця")
        
        # Обновляем день недели сразу
        self.UPDATE_TIME()