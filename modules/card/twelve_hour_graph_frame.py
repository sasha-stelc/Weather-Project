import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui

from .utils import get_weather_icon_path


class TwelveHourGraphFrame(widget.QFrame):
    """Виджет для графика прогноза на 12 часов"""
    
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)

        self.setFixedHeight(197)
        self.setStyleSheet("""
            TwelveHourGraphFrame {
                background: rgba(0, 0, 0, 0.2);
                border-radius: 20px;
            }
        """)

        original_data = data.get("next_12h", [])

        self.forecast_data = []
        for item in original_data:
            for _ in range(4):
                self.forecast_data.append(item)

        layout = widget.QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 0)

        title = widget.QLabel("Прогноз на 12 годин")
        title.setStyleSheet("font-size: 13px; color: white; font-weight: bold; background: transparent; opacity: 0.8;")
        layout.addWidget(title)

        layout.addStretch()

    def paintEvent(self, event):
        painter = gui.QPainter(self)
        painter.setRenderHint(gui.QPainter.RenderHint.Antialiasing)

        W, H = self.width(), self.height()
        pad_l, pad_r = 15, 35
        pad_top, pad_bot = 55, 30
        draw_w = W - pad_l - pad_r
        draw_h = H - pad_top - pad_bot

        scale_values = [25, 20, 15, 10, 5, 0, -5, -10]
        y_min, y_max = -10, 25

        font = painter.font()
        font.setPointSize(7)
        painter.setFont(font)

        for val in scale_values:
            y = pad_top + (y_max - val) * (draw_h / (y_max - y_min))

            pen = gui.QPen(gui.QColor(255, 255, 255, 30))
            pen.setStyle(core.Qt.PenStyle.DotLine)
            painter.setPen(pen)
            painter.drawLine(pad_l, int(y), W - pad_r, int(y))

            painter.setPen(gui.QColor(255, 255, 255, 160))
            painter.drawText(W - 28, int(y) + 4, f"{val}°")

        n = len(self.forecast_data)
        step = draw_w / n
        bar_w = step * 0.7

        for i, item in enumerate(self.forecast_data):
            temp = item["temp"]
            safe_temp = max(y_min, min(y_max, temp))

            y_val = pad_top + (y_max - safe_temp) * (draw_h / (y_max - y_min))
            y_bottom = pad_top + draw_h

            x = pad_l + i * step
            rect = core.QRectF(x, y_val, bar_w, y_bottom - y_val)

            grad = gui.QLinearGradient(rect.topLeft(), rect.bottomLeft())
            grad.setColorAt(0, gui.QColor(255, 255, 150, 200))
            grad.setColorAt(1, gui.QColor(100, 180, 255, 120))

            painter.setPen(core.Qt.PenStyle.NoPen)
            painter.setBrush(gui.QBrush(grad))
            painter.drawRoundedRect(rect, 1, 1)

            if i % 4 == 0:
                icon_path = get_weather_icon_path(item["icon"])
                if os.path.exists(icon_path):
                    pix = gui.QPixmap(icon_path).scaled(
                        21, 21,
                        core.Qt.AspectRatioMode.KeepAspectRatio,
                        core.Qt.TransformationMode.SmoothTransformation
                    )
                    icon_x = int(x + (step * 4) / 2 - 8)
                    painter.drawPixmap(icon_x, pad_top - 25, pix)

        painter.end()
