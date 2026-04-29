import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .create_path import create_media_path


class TitleBar(widget.QFrame):
    def __init__(self, window):
        super().__init__()
        self.WINDOW = window

        self.setFixedHeight(36)
        
        layout = widget.QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        layout.setSpacing(0)

        
        layout.addStretch()

        self.min_btn = widget.QToolButton()
        self.max_btn = widget.QToolButton()
        self.close_btn = widget.QToolButton()

        self.min_btn.clicked.connect(self.WINDOW.showMinimized)
        self.max_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(self.WINDOW.close)

        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

       
        self._drag_position = None

        path = create_media_path

        self.min_icon = gui.QIcon(gui.QPixmap(path("Minimize_Button.svg")))
        self.max_icon = gui.QIcon(gui.QPixmap(path("Maximize_Button.svg")))
        self.close_icon = gui.QIcon(gui.QPixmap(path("Close_Button.svg")))

        self.min_hover = gui.QIcon(gui.QPixmap(path("Minimize_Button_Hover.svg")))
        self.max_hover = gui.QIcon(gui.QPixmap(path("Maximize_Button_Hover.svg")))
        self.close_hover = gui.QIcon(gui.QPixmap(path("Close_Button_Hover.svg")))

        
        self.min_btn.setIcon(self.min_icon)
        self.max_btn.setIcon(self.max_icon)
        self.close_btn.setIcon(self.close_icon)

    def toggle_maximize(self):
        if self.WINDOW.isMaximized():
            self.WINDOW.showNormal()
        else:
            self.WINDOW.showMaximized()

    def enterEvent(self, event):

        self.min_btn.setIcon(self.min_hover)
        self.max_btn.setIcon(self.max_hover)
        self.close_btn.setIcon(self.close_hover)

    def leaveEvent(self, event):
        self.min_btn.setIcon(self.min_icon)
        self.max_btn.setIcon(self.max_icon)
        self.close_btn.setIcon(self.close_icon)

    def mouseMoveEvent(self, event:gui.QMouseEvent):
        mouse_pos = event.position().toPoint() - self.POSITION
        print(mouse_pos, self.window().x(), self.window().y())
        self.window().move(
            self.window().x() + mouse_pos.x() ,
            self.window().y() + mouse_pos.y()
        )
        
    def mousePressEvent(self, event:gui.QMouseEvent):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.POSITION = event.position().toPoint()