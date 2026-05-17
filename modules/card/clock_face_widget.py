import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui


class ClockFaceWidget(widget.QWidget):
    """Виджет циферблата часов"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.TICK_LENGTH = 12
        self.TICK_MARGIN = 15
        self.TICK_WIDTH = 4
        self.BG_ALPHA = 45
        self.TICK_ALPHA = 150

    def paintEvent(self, event):
        self.PAINTER = gui.QPainter(self)
        self.PAINTER.setRenderHint(gui.QPainter.RenderHint.Antialiasing)

        self.WIDTH = self.width()
        self.HEIGHT = self.height()
        self.CENTER = core.QPointF(self.WIDTH / 2.0, self.HEIGHT / 2.0)
        self.RADIUS = min(self.WIDTH, self.HEIGHT) / 2.0

        self.PAINTER.setBrush(gui.QColor(0, 0, 0, self.BG_ALPHA))
        self.PAINTER.setPen(core.Qt.PenStyle.NoPen)
        self.PAINTER.drawEllipse(self.CENTER, self.RADIUS, self.RADIUS)

        self.PAINTER.translate(self.CENTER)
        self.PEN = gui.QPen(gui.QColor(255, 255, 255, self.TICK_ALPHA))
        self.PEN.setWidth(self.TICK_WIDTH)
        self.PEN.setCapStyle(core.Qt.PenCapStyle.RoundCap)
        self.PAINTER.setPen(self.PEN)

        for i in range(12):
            self.PAINTER.drawLine(
                core.QPointF(0, -self.RADIUS + self.TICK_MARGIN), 
                core.QPointF(0, -self.RADIUS + self.TICK_MARGIN + self.TICK_LENGTH)
            )
            self.PAINTER.rotate(30.0)
            
        self.PAINTER.end()
