import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWidgets as widget

from .. import styles
from ..create_path import create_media_path


class WeatherCard(widget.QFrame):
    """Кастомный интерактивный виджет карточки погоды для списка городов.

    Класс представляет собой компактную информационную панель, которая:
    - Отображает основные метеоданные: город, время, температуру, описание и минимумы/максимумы.
    - Реализует паттерн «Hover/Select» для интерактивного отклика на действия пользователя.
    - Переопределяет низкоуровневые события ввода Qt (мышь) для генерации пользовательских сигналов.
    """
    
    # Пользовательский PyQt-сигнал. Эмитится (генерируется) при клике левой кнопкой мыши.
    # Передает в качестве аргумента `object` (ссылку на сам экземпляр self этой карточки),
    # позволяя родительскому контейнеру понять, какая именно карточка была выбрана.
    selected = core.pyqtSignal(object)

    def __init__(self, city: str, time: str, temp: str, desc: str, minmax: str, IS_CURRENT: bool = False):
        """Конструирует карточку, инициализирует внутреннюю разметку и текстовые метки.

        Args:
            city (str): Название населенного пункта.
            time (str): Строка локального времени в формате "ЧЧ:ММ".
            temp (str): Численное значение температуры без знака градуса.
            desc (str): Краткое текстовое описание погодных условий.
            minmax (str): Строка минимальной и максимальной суточной температуры.
            IS_CURRENT (bool, optional): Флаг текущего геоположения. Влияет на базовый стиль. 
                                         Defaults to False.
        """
        super().__init__()
        
        # --- Флаги внутреннего состояния компонента ---
        self.IS_CURRENT = IS_CURRENT  # Определяет, является ли город текущей геопозицией пользователя
        self.IS_SELECTED = False      # Выделена ли карточка в текущий момент кликом
        
        # Включаем постоянное отслеживание перемещений мыши. Без этого события 
        # enterEvent и leaveEvent могли бы срабатывать некорректно при быстрой прокрутке списка.
        self.setMouseTracking(True)
  
        # Ограничиваем максимальные физические габариты элемента в списке
        self.setMaximumSize(330, 104)
        
        # --- ИНИЦИАЛИЗАЦИЯ ЭЛЕМЕНТОВ ИНТЕРФЕЙСА ---
        # Индикатор выбора (маленькая иконка-галочка). По умолчанию скрыта.
        self.CHOICE_ICON = widget.QToolButton()
        self.CHOICE_ICON.setIcon(gui.QIcon(gui.QPixmap(create_media_path("choice_vector.png"))))
        self.CHOICE_ICON.setFixedSize(20, 20)
        self.CHOICE_ICON.setIconSize(core.QSize(20, 20))
        self.CHOICE_ICON.setVisible(False)

        # Текстовая метка названия города
        self.CITY_LABEL = widget.QLabel(city)
        self.CITY_LABEL.setStyleSheet(styles.CITY_LABEL)
        # Политика изменения размеров: expanding заставляет метку занимать все свободное место по горизонтали
        self.CITY_LABEL.setSizePolicy(widget.QSizePolicy.Policy.Expanding, 
                                      widget.QSizePolicy.Policy.Preferred)

        # Текстовая метка локального времени
        self.TIME_LABEL = widget.QLabel(time)
        self.TIME_LABEL.setStyleSheet(styles.TIME_LABEL)

        # Текстовая метка текущей температуры
        self.TEMP_LABEL = widget.QLabel(f"{temp}°")
        self.TEMP_LABEL.setStyleSheet(styles.TEMP_LABEL)
        # Прижимаем температуру к правому верхнему углу выделенной ей области
        self.TEMP_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignTop)

        # Текстовая метка описания погоды (например, "Ясно")
        self.DESC_LABEL = widget.QLabel(desc)
        self.DESC_LABEL.setStyleSheet(styles.DESC_LABEL)

        # Текстовая метка диапазона температур за сутки
        self.MINMAX_LABEL = widget.QLabel(minmax)
        self.MINMAX_LABEL.setStyleSheet(styles.MINMAX_LABEL)
        # Прижимаем диапазон строго к правому краю
        self.MINMAX_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignRight)

        # --- СБОРКА СЕТКИ И ЛЕЙАУТОВ (Макет по строкам) ---
        # 1. Верхняя строка: Иконка галочки + Город --------(Распорка)-------- Текущая температура
        self.TOP_ROW = widget.QHBoxLayout()
        self.TOP_ROW.setContentsMargins(0, 0, 0, 0)
        self.TOP_ROW.setSpacing(6)
        self.TOP_ROW.addWidget(self.CHOICE_ICON)
        self.TOP_ROW.addWidget(self.CITY_LABEL)
        self.TOP_ROW.addStretch()  # Расталкивает элементы по краям строки
        self.TOP_ROW.addWidget(self.TEMP_LABEL)

        # 2. Средняя строка: Локальное время --------(Распорка)
        self.MID_ROW = widget.QHBoxLayout()
        self.MID_ROW.setContentsMargins(0, 0, 0, 8)
        self.MID_ROW.addWidget(self.TIME_LABEL)
        self.MID_ROW.addStretch()

        # 3. Нижняя строка: Описание погоды --------(Распорка)-------- МинМакс температуры
        self.BOT_ROW = widget.QHBoxLayout()
        self.BOT_ROW.setContentsMargins(0, 0, 0, 8)
        self.BOT_ROW.addWidget(self.DESC_LABEL)
        self.BOT_ROW.addStretch()
        self.BOT_ROW.addWidget(self.MINMAX_LABEL)

        # Главный вертикальный контейнер, объединяющий созданные строки
        self.MAIN_LAYOUT = widget.QVBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(8, 8, 8, 8)
        self.MAIN_LAYOUT.setSpacing(0)
        self.MAIN_LAYOUT.addLayout(self.TOP_ROW)
        self.MAIN_LAYOUT.addLayout(self.MID_ROW)
        self.MAIN_LAYOUT.addStretch()  # Создает упругую пустоту, выталкивая нижнюю строку в самый низ
        self.MAIN_LAYOUT.addLayout(self.BOT_ROW)
        
        # Применяем первоначальное визуальное оформление (базовое, незатененное состояние)
        self.apply_style(dimmed=False)

    def update_data(self, data: dict):
        """Динамически обновляет текст во всех внутренних метках виджета.

        Используется при получении свежих данных из фонового потока API погоды,
        исключая необходимость пересоздавать виджет карточки заново.

        Args:
            data (dict): Словарь с ключами "city", "time", "temp", "desc", "minmax".
        """
        self.weather_data = data  # Кэшируем полный объект данных внутри карточки
        self.CITY_LABEL.setText(data["city"])
        self.TIME_LABEL.setText(data["time"])
        self.TEMP_LABEL.setText(f"{data['temp']}°")
        self.DESC_LABEL.setText(data["desc"])
        self.MINMAX_LABEL.setText(data["minmax"])

    def apply_style(self, dimmed: bool):
        """Формирует и накладывает QSS-стиль (таблицу стилей) на основе текущего состояния.

        Использует строки форматирования из общего файла конфигурации стилей проекта
        и налету подставляет туда параметры цвета подложки, границ и закругления.

        Args:
            dimmed (bool): Флаг «затемнения». True активирует стиль для состояния Hover/Selected 
                           (более темный или контрастный фон), False возвращает дефолтный вид.
        """
        if self.IS_CURRENT:
            # Специфическая палитра для основной карточки текущего геоположения
            bg = "rgba(0,0,0,110)" if dimmed else "rgba(0,0,0,60)"
            self.setStyleSheet(styles.CURRENT_CARD.format(bg=bg))
        else:
            # Палитра и геометрия границ для обычных карточек городов из списка
            bg     = "rgba(0,0,0,80)"       if dimmed else "transparent"
            border = "rgba(255,255,255,80)" if dimmed else "rgba(255,255,255,40)"
            radius = "10px"                 if dimmed else "0px"
            self.setStyleSheet(styles.DEFAULT_CARD.format(bg=bg, border=border, radius=radius))

    def set_selected(self, selected: bool):
        """Программно переключает состояние карточки на "Выбрана/Не выбрана".

        Включает или выключает маркер-галочку и фиксирует активный QSS-стиль подсветки.

        Args:
            selected (bool): Статус выбора карточки.
        """
        self.IS_SELECTED = selected
        self.CHOICE_ICON.setVisible(selected)  # Переключаем видимость кнопки-галочки
        self.apply_style(dimmed=selected)      # Фиксируем контрастный стиль подложки

        # --- ОБРАБОТКА НИЗКОУРОВНЕВЫХ СОБЫТИЙ ИНТЕРФЕЙСА (Event Handlers) ---

    def enterEvent(self, event):
        """Переопределенный обработчик: срабатывает, когда курсор мыши входит в границы виджета.

        Реализует визуальный отклик Hover-эффекта: карточка подсвечивается (dimmed=True), 
        если она не зафиксирована кликом.
        """
        if not self.IS_SELECTED: 
            self.apply_style(dimmed=True)
        super().enterEvent(event)  # Передаем управление базовому классу Qt для штатной цепочки обработки

    def leaveEvent(self, event):
        """Переопределенный обработчик: когда курсор мыши покидает границы виджета.

        Убирает Hover-подсветку (dimmed=False) и возвращает карту в исходный вид.
        """
        if not self.IS_SELECTED: 
            self.apply_style(dimmed=False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Переопределенный обработчик: срабатывает в момент нажатия кнопки мыши на виджет.

        Проверяет, была ли нажата именно Левая Кнопка Мыши (LKM). Если да, 
        генерирует сигнал `selected.emit(self)`.

        Args:
            event (QMouseEvent): Контекст события мыши (координаты, нажатая кнопка, модификаторы клавиатуры).
        """
        if event.button() == core.Qt.MouseButton.LeftButton: 
            self.selected.emit(self)  # Извещаем внешние компоненты приложения о выборе
        super().mousePressEvent(event)
