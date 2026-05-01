import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .create_path import create_media_path


class TitleBar(widget.QFrame):
    def __init__(self, window):
        super().__init__()
        self.WINDOW = window

        self.setFixedHeight(26)

        layout = widget.QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        layout.setSpacing(0)

        layout.addStretch()

        # Кнопки
        self.MIN_BTN = widget.QToolButton()
        self.MAX_BTN = widget.QToolButton()
        self.CLOSE_BTN = widget.QToolButton()

        self.MIN_BTN.clicked.connect(self.WINDOW.showMinimized)
        self.MAX_BTN.clicked.connect(self.toggle_maximize)
        self.CLOSE_BTN.clicked.connect(self.WINDOW.close)

        layout.addWidget(self.MIN_BTN)
        layout.addWidget(self.MAX_BTN)
        layout.addWidget(self.CLOSE_BTN)

        self.DRAG_POSITION = None


        path = create_media_path
        # иконки до наведения
        self.MIN_ICON = gui.QIcon(gui.QPixmap(path("Minimize_Button.svg")))
        self.MAX_ICON = gui.QIcon(gui.QPixmap(path("Maximize_Button.svg")))
        self.CLOSE_ICON = gui.QIcon(gui.QPixmap(path("Close_Button.svg")))
        # иконки при наведении
        self.MIN_HOVER = gui.QIcon(gui.QPixmap(path("Minimize_Button_Hover.svg")))
        self.MAX_HOVER = gui.QIcon(gui.QPixmap(path("Maximize_Button_Hover.svg")))
        self.CLOSE_HOVER = gui.QIcon(gui.QPixmap(path("Close_Button_Hover.svg")))

        # иконки по умолчанию
        self.MIN_BTN.setIcon(self.MIN_ICON)
        self.MAX_BTN.setIcon(self.MAX_ICON)
        self.CLOSE_BTN.setIcon(self.CLOSE_ICON)

    def toggle_maximize(self):
        if self.WINDOW.isMaximized():
            self.WINDOW.showNormal()
        else:
            self.WINDOW.showMaximized()

    def enterEvent(self, event):
        self.MIN_BTN.setIcon(self.MIN_HOVER)
        self.MAX_BTN.setIcon(self.MAX_HOVER)
        self.CLOSE_BTN.setIcon(self.CLOSE_HOVER)

    def leaveEvent(self, event):
        self.MIN_BTN.setIcon(self.MIN_ICON)
        self.MAX_BTN.setIcon(self.MAX_ICON)
        self.CLOSE_BTN.setIcon(self.CLOSE_ICON)

    def mouseMoveEvent(self, event: gui.QMouseEvent):

        mouse_pos = event.position().toPoint() - self.DRAG_POSITION
        self.window().move(
            self.window().x() + mouse_pos.x(),
            self.window().y() + mouse_pos.y()
        )

    def mousePressEvent(self, event: gui.QMouseEvent):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.DRAG_POSITION = event.position().toPoint()