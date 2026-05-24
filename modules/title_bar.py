import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWidgets as widget
from .create_path import create_media_path
from . import styles


class TitleBar(widget.QFrame):
    """Кастомный заголовок окна (TitleBar) для кастомизированных безрамочных окон.
    
    Обеспечивает базовый функционал системного заголовка, который операционная система 
    блокирует при использовании флага FramelessWindowHint:
    - Перетаскивание (Drag & Drop) всего окна приложения по экрану.
    - Системные действия: закрытие, сворачивание и разворачивание на весь экран.
    - Кастомная стилизация и интерактивные эффекты наведения (Hover) на кнопки управления.
    """
    
    def __init__(self, window: widget.QWidget):
        """Инициализирует панель заголовка и связывает ее с управляемым окном.

        Args:
            window (QWidget): Ссылка на главное окно приложения, которым управляет данный TitleBar.
        """
        super().__init__()
        self.WINDOW = window

        # Фиксируем высоту панели управления в соответствии с габаритами системных кнопок
        self.setFixedHeight(26)

        # Главный горизонтальный контейнер для выравнивания кнопок по правому краю
        layout = widget.QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        layout.setSpacing(0)

        # Добавляем пружину (Stretch) на первое место, чтобы вытолкнуть все последующие 
        # компоненты (кнопки управления) в крайний правый угол панели
        layout.addStretch()

        # --- ИНИЦИАЛИЗАЦИЯ КНОПОК УПРАВЛЕНИЯ ОКНОМ ---
        # Использование QToolButton вместо QPushButton предпочтительнее для компактных иконок
        self.MIN_BTN = widget.QToolButton()
        self.MAX_BTN = widget.QToolButton()
        self.CLOSE_BTN = widget.QToolButton()

        # Подключение стандартных слотов управления состоянием окна Qt
        self.MIN_BTN.clicked.connect(self.WINDOW.showMinimized)  # Свернуть в панель задач
        self.MAX_BTN.clicked.connect(self.toggle_maximize)       # Развернуть / Восстановить размер
        self.CLOSE_BTN.clicked.connect(self.WINDOW.close)         # Закрыть приложение

        # Интеграция кнопок в компоновщик
        layout.addWidget(self.MIN_BTN, alignment= core.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.MAX_BTN, alignment= core.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.CLOSE_BTN, alignment= core.Qt.AlignmentFlag.AlignLeft)

        # Переменная для хранения стартовой точки клика мыши (нужна для расчета сдвига окна)
        self.DRAG_POSITION = None

        # --- ЗАГРУЗКА И ВЕКТОРНОЕ МАСШТАБИРОВАНИЕ ИКОНОК ---
        path = create_media_path
        
        # Базовые иконки состояния покоя (файлы формата SVG обеспечивают четкость при любом DPI)
        self.MIN_ICON = gui.QIcon(gui.QPixmap(path("Minimize_Button.svg")))
        self.MAX_ICON = gui.QIcon(gui.QPixmap(path("Maximize_Button.svg")))
        self.CLOSE_ICON = gui.QIcon(gui.QPixmap(path("Close_Button.svg")))
        
        # Альтернативные иконки для состояния наведения (Hover)
        self.MIN_HOVER = gui.QIcon(gui.QPixmap(path("Minimize_Button_Hover.svg")))
        self.MAX_HOVER = gui.QIcon(gui.QPixmap(path("Maximize_Button_Hover.svg")))
        self.CLOSE_HOVER = gui.QIcon(gui.QPixmap(path("Close_Button_Hover.svg")))

        # Установка базового визуального состояния при старте
        self.MIN_BTN.setIcon(self.MIN_ICON)
        self.MAX_BTN.setIcon(self.MAX_ICON)
        self.CLOSE_BTN.setIcon(self.CLOSE_ICON)

        # Сброс рамок кнопок для предотвращения дефолтного серого выделения Qt
        self.MIN_BTN.setStyleSheet(styles.TITLE_BAR_BUTTONS)
        self.MAX_BTN.setStyleSheet(styles.TITLE_BAR_BUTTONS)
        self.CLOSE_BTN.setStyleSheet(styles.TITLE_BAR_BUTTONS)

    def toggle_maximize(self):
        """Переключает геометрию окна между развернутым на весь экран и нормальным состоянием."""
        if self.WINDOW.isMaximized():
            self.WINDOW.showNormal()    # Возвращает исходный оконный размер
        else:
            self.WINDOW.showMaximized() # Растягивает окно на всю рабочую область монитора

    # --- ИСПРАВЛЕННАЯ СИСТЕМНАЯ ЛОГИКА HOVER-ЭФФЕКТОВ ---
    # Примечание: Для корректной индивидуальной смены иконок на каждой кнопке при наведении 
    # рекомендуется использовать CSS псевдокласс :hover в setStyleSheet, но если вы делаете это через события:
    def enterEvent(self, event):
        """Срабатывает, когда мышь заходит на территорию панели заголовка."""
        # Включаем превентивную подсветку всех управляющих элементов
        self.MIN_BTN.setIcon(self.MIN_HOVER)
        self.MAX_BTN.setIcon(self.MAX_HOVER)
        self.CLOSE_BTN.setIcon(self.CLOSE_HOVER)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Срабатывает, когда курсор полностью покидает область заголовка."""
        # Возвращаем кнопкам стандартный монохромный вид
        self.MIN_BTN.setIcon(self.MIN_ICON)
        self.MAX_BTN.setIcon(self.MAX_ICON)
        self.CLOSE_BTN.setIcon(self.CLOSE_ICON)
        super().leaveEvent(event)

    # --- МЕХАНИКА ПЕРЕМЕЩЕНИЯ БЕЗРАМОЧНОГО ОКНА (Drag & Drop) ---

    def mousePressEvent(self, event: gui.QMouseEvent):
        """Запоминает локальную координату клика мыши в момент нажатия на заголовок.

        Args:
            event (QMouseEvent): Контекст события нажатия кнопки мыши.
        """
        if event.button() == core.Qt.MouseButton.LeftButton:
            # Преобразуем точные вещественные координаты события в пиксельную точку QPoint.
            # Фиксируем сдвиг курсора относительно верхнего левого угла самого TitleBar.
            self.DRAG_POSITION = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: gui.QMouseEvent):
        """Вычисляет дельту смещения курсора и плавно перемещает окно приложения вслед за ним.

        Срабатывает непрерывно при зажатой левой кнопке мыши и перемещении указателя.

        Args:
            event (QMouseEvent): Контекст перемещения мыши с текущими экранными координатами.
        """
        # Если клик был зафиксирован и мышь движется
        if self.DRAG_POSITION is not None and event.buttons() == core.Qt.MouseButton.LeftButton:
            # Математика вектора движения:
            # 1. event.position().toPoint() — где мышь находится СЕЙЧАС внутри виджета.
            # 2. self.DRAG_POSITION — где мышь БЫЛА в момент клика.
            # Находим разницу (дельту) — вектор относительного сдвига руки пользователя.
            mouse_pos = event.position().toPoint() - self.DRAG_POSITION
            
            # Перемещаем базовое окно (self.window() возвращает глобальный родительский QWidget/QMainWindow),
            # добавляя вычисленное смещение к текущему абсолютному положению окна на глобальном экране ОС.
            self.window().move(
                self.window().x() + mouse_pos.x(),
                self.window().y() + mouse_pos.y()
            )
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: gui.QMouseEvent):
        """Сбрасывает точку зажима мыши при отпускании кнопки, завершая фазу перемещения окна."""
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.DRAG_POSITION = None
        super().mouseReleaseEvent(event)
