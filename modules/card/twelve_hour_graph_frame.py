import os
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWidgets as widget

from .. import styles
from .utils import get_weather_icon_path


class TwelveHourGraphFrame(widget.QFrame):
    """Виджет графического отображения 12-часового прогноза погоды.
    
    Строит столбчатую диаграмму (гистограмму) изменения температуры. 
    Отрисовывает горизонтальную координатную сетку с шагом в 5°C, температурные 
    градиентные столбцы, а также накладывает иконки погодных условий над ними.
    """
    
    def __init__(self, data: dict, parent=None):
        """Инициализирует фрейм и подготавливает данные для плотного графика.

        Args:
            data (dict): Словарь с прогнозом погоды. Ожидает ключ "next_12h" 
                         со списком 12-часовых слотов.
            parent (QWidget, optional): Родительский компонент. Defaults to None.
        """
        super().__init__(parent)

        self.minimumHeight()
        self.setStyleSheet(styles.TWELVE_HOUR_FRAME)

        # Извлекаем оригинальный массив из 12 элементов (точек прогноза)
        original_data = data.get("next_12h", [])

        # --- ХАК ДЛЯ ПЛОТНОСТИ ГРАФИКА ---
        # Каждый из 12 оригинальных элементов дублируется 4 раза подряд.
        # Это искусственно увеличивает массив до 48 элементов. 
        # Цель: сделать столбцы на графике более частыми и плотными, чтобы визуально 
        # гистограмма выглядела как непрерывная заполненная диаграмма.
        self.forecast_data = []
        for item in original_data:
            for _ in range(4):
                self.forecast_data.append(item)

        # Настройка базовой разметки (включает только текстовый заголовок)
        layout = widget.QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 8)
        layout.setSpacing(0)

        header = widget.QWidget()
        header_layout = widget.QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 8)
        header_layout.setSpacing(6)

        title = widget.QLabel("Прогноз на 12 годин")
        title.setStyleSheet(styles.TWELVE_HOUR_TITLE)

        header_layout.addWidget(title)

        line = widget.QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet(styles.HOURLY_LINE)

        header_layout.addWidget(line)

        layout.addWidget(header)
        self.GRAPH_CONTAINER = widget.QWidget()
        self.GRAPH_LAYOUT = widget.QVBoxLayout(self.GRAPH_CONTAINER)
        self.GRAPH_LAYOUT.setContentsMargins(0, 8, 0, 0)  
        layout.addWidget(self.GRAPH_CONTAINER, 1)  
  
    def paintEvent(self, event):
        """Выполняет низкоуровневую отрисовку координатной сетки и столбцов графика.
        
        Args:
            event (QPaintEvent): Объект события перерисовки холста.
        """
        painter = gui.QPainter(self)
        painter.setRenderHint(gui.QPainter.RenderHint.Antialiasing)  # Включаем сглаживание геометрии

        # Габариты самого виджета
        W, H = self.width(), self.height()
        
        # --- ГЕОМЕТРИЧЕСКИЕ ОТСТУПЫ (Padding) ---
        pad_l, pad_r = 15, 35      # Отступы слева и справа (справа больше для текста шкалы градусов)
        pad_top, pad_bot = 70, 10  # Отступы сверху (под иконки) и снизу (под границы столбцов)
        
        # Чистые размеры рабочей области, где непосредственно рисуется график
        draw_w = W - pad_l - pad_r
        draw_h = H - pad_top - pad_bot

        # Жестко заданные температурные маркеры для шкалы
        scale_values = [25, 20, 15, 10, 5, 0, -5, -10]
        # Экстремумы шкалы (границы, за которые график не должен выходить)
        y_min, y_max = -10, 25

        # Уменьшаем размер шрифта для подписей градусов на шкале
        font = painter.font()
        font.setPointSize(7)
        painter.setFont(font)

        # --- ШАГ 1: ОТРИСОВКА КООРДИНАТНОЙ СЕТКИ С ПРАВЫМИ ПОДПИСЯМИ ---
        for val in scale_values:
            # Математическая пропорция перевода градусов Цельсия в Y-координату на экране:
            # 1. (y_max - val) — инвертируем значение, так как в Qt координата Y=0 находится СВЕРХУ.
            # 2. Умножаем на коэффициент (высота рабочей области / диапазон температур).
            y = pad_top + (y_max - val) * (draw_h / (y_max - y_min))

            # Рисуем горизонтальную пунктирную линию сетки (очень тонкая, альфа = 30)
            pen = gui.QPen(gui.QColor(255, 255, 255, 30))
            pen.setStyle(core.Qt.PenStyle.DotLine)
            painter.setPen(pen)
            painter.drawLine(pad_l, int(y), W - pad_r, int(y))

            # Справа от пунктира рисуем текст температуры (например, "15°")
            painter.setPen(gui.QColor(255, 255, 255, 160))
            painter.drawText(W - 28, int(y) + 4, f"{val}°")  # Смещение +4 центрирует текст по вертикали

        # --- ШАГ 2: ОТРИСОВКА СТОЛБЦОВ ГРАФИКА И ИКОНОК ---
        n = len(self.forecast_data)  # Всего 48 элементов после размножения
        step = draw_w / n            # Пиксельная ширина одной ячейки (шаг по оси X)
        bar_w = step * 0.7           # Ширина самого столбца (70% от шага, 30% уходит на зазор)

        for i, item in enumerate(self.forecast_data):
            temp = item["temp"]
            
            # Обеспечиваем безопасный диапазон (Clamp), чтобы аномальная температура не вылетела за рамки
            safe_temp = max(y_min, min(y_max, temp))

            # Рассчитываем верхнюю пиксельную координату столбца на основе его температуры
            y_val = pad_top + (y_max - safe_temp) * (draw_h / (y_max - y_min))
            # Нижняя пиксельная координата — это всегда дно рабочей области графика
            y_bottom = pad_top + draw_h

            # Рассчитываем координату X для текущего столбца
            x = pad_l + i * step
            
            # Создаем прямоугольник столбца
            rect = core.QRectF(x, y_val, bar_w, y_bottom - y_val)

            # Настраиваем вертикальный линейный градиент для заливки столбца:
            # Сверху — теплый желтоватый оттенок, снизу — прохладный голубой
            grad = gui.QLinearGradient(rect.topLeft(), rect.bottomLeft())
            grad.setColorAt(0, gui.QColor(255, 255, 150, 200))
            grad.setColorAt(1, gui.QColor(100, 180, 255, 120))

            # Рисуем столбец со скруглением углов в 1 пиксель (без контура, только заливка)
            painter.setPen(core.Qt.PenStyle.NoPen)
            painter.setBrush(gui.QBrush(grad))
            painter.drawRoundedRect(rect, 1, 1)

            # --- ОТРИСОВКА ИКОНОК ПОГОДЫ ---
            # Так как данные были продублированы х4, иконку нужно рисовать только 
            # один раз для каждого оригинального часа. Проверяем остаток от деления на 4.
            if i % 4 == 0:
                icon_path = get_weather_icon_path(item["icon"])
                if os.path.exists(icon_path):
                    # Масштабируем иконку погоды до миниатюрного размера 21x21 пиксель
                    pix = gui.QPixmap(icon_path).scaled(
                        16, 16,
                        core.Qt.AspectRatioMode.KeepAspectRatio,
                        core.Qt.TransformationMode.SmoothTransformation
                    )
                    # Вычисляем координату X так, чтобы иконка стояла по центру группы из 4 дубликатов
                    icon_x = int(x + (step * 4) / 2 - 8)
                    
                    # Отрисовываем иконку в верхней свободной зоне (pad_top - 25)
                    painter.drawPixmap(icon_x, pad_top - 25, pix)

        # Освобождаем системные ресурсы painter
        painter.end()
