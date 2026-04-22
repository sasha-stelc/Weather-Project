import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtWidgets import QCheckBox
from .card import WeatherCard
from .app import app

def create_path(name: str):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "..", "media", name)
        return os.path.normpath(path)
    except Exception as error:
        print(f"Ошибка загрузки пути: {error}")
        return ""

class ImageThemeSwitch(widget.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(core.Qt.CursorShape.PointingHandCursor)
        
        self.setFixedSize(52, 24) 
        self.setIconSize(core.QSize(18, 18))
        
        self.sun_icon_path = create_path("Frame_51.png")
        self.moon_icon_path = create_path("Frame_52.png")

        self.toggled.connect(self.update_image)
        
        self.setChecked(False)
        self.update_image(self.isChecked())

    def update_image(self, checked):
        if checked:
            self.setStyleSheet("""
                QPushButton {
                    background-color: white; 
                    border-radius: 12px;
                    padding-left: 3px;
                    padding-right: 31px;
                }
            """)
            self.setIcon(gui.QIcon(self.sun_icon_path))
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: white; 
                    border-radius: 12px;
                    padding-left: 31px;
                    padding-right: 3px;
                }
            """)
            self.setIcon(gui.QIcon(self.moon_icon_path))

class WeatherApp(widget.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Погода")
        self.resize(1200, 800)
        
        self.CENTRAL_FRAME = widget.QWidget()
        self.CENTRAL_FRAME.setStyleSheet("background-color: #2E2E2E;") 
        self.setCentralWidget(self.CENTRAL_FRAME)
        
        self.MAIN_LAYOUT = widget.QHBoxLayout(self.CENTRAL_FRAME)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAIN_LAYOUT.setSpacing(0)

        self.LEFT_PANEL = widget.QFrame()
        self.LEFT_PANEL.setFixedWidth(370) 
        self.LEFT_PANEL.setStyleSheet("""
            QFrame {
                background-color: #6C8281; 
                border-right: 1px solid #1A1A1A; 
            }
        """)
        
        self.LEFT_LAYOUT = widget.QVBoxLayout(self.LEFT_PANEL)
        self.LEFT_LAYOUT.setContentsMargins(20, 20, 20, 0)
        self.LEFT_LAYOUT.setSpacing(10)
         
        self.TOP_BAR_FRAME = widget.QFrame(self.LEFT_PANEL)
        self.TOP_BAR_FRAME.setFixedSize(core.QSize(330, 44))
        
        self.TOP_BAR_LAYOUT = widget.QHBoxLayout(self.TOP_BAR_FRAME)
        self.TOP_BAR_LAYOUT.setContentsMargins(0, 0, 0, 0)
        
        self.THEME_BUTTON = ImageThemeSwitch()

        self.TOP_BAR_LAYOUT.addWidget(self.THEME_BUTTON, alignment = core.Qt.AlignmentFlag.AlignRight)
        
        self.LEFT_LAYOUT.addWidget(self.TOP_BAR_FRAME) 

        self.SCROLL_AREA = widget.QScrollArea()
        self.SCROLL_AREA.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL_AREA.setWidgetResizable(True)
        self.SCROLL_AREA.setFrameShape(widget.QFrame.Shape.NoFrame)
        self.SCROLL_AREA.setStyleSheet("background: transparent; border: none;")
        
        self.CARDS_CONTAINER = widget.QWidget()
        self.CARDS_CONTAINER.setStyleSheet("background: transparent;")
        
        self.CARDS_LAYOUT = widget.QVBoxLayout(self.CARDS_CONTAINER)
        self.CARDS_LAYOUT.setContentsMargins(10, 10, 10, 20)
        self.CARDS_LAYOUT.setSpacing(10)
        
        self.WEATHER_DATA = [
            {"city": "Дніпро", "time": "15:24", "temp": "11", "desc": "Переважно хмарно", "minmax": "Макс.:11°, мін.:0°", "is_current": False},
            {"city": "Київ", "time": "15:24", "temp": "14", "desc": "Сонячно", "minmax": "Макс.:15°, мін.:0°", "is_current": False},
            {"city": "Братіслава", "time": "14:24", "temp": "9", "desc": "Подекуди хмарно", "minmax": "Макс.:10°, мін.:1°", "is_current": False},
            {"city": "Варшава", "time": "14:24", "temp": "15", "desc": "Хмарно", "minmax": "Макс.:18°, мін.:7°", "is_current": False},
            {"city": "Рим", "time": "14:24", "temp": "24", "desc": "Сонячно", "minmax": "Макс.:25°, мін.:16°", "is_current": False},
        ]
        
        self.WEATHER_CARDS = []
        
        for data in self.WEATHER_DATA:
            card = WeatherCard(
                data["city"], data["time"], data["temp"], 
                data["desc"], data["minmax"], data["is_current"]
            )
            self.WEATHER_CARDS.append(card)
            self.CARDS_LAYOUT.addWidget(card)
            
        self.CARDS_LAYOUT.addStretch()
        self.SCROLL_AREA.setWidget(self.CARDS_CONTAINER)
        self.LEFT_LAYOUT.addWidget(self.SCROLL_AREA)

        self.RIGHT_PANEL = widget.QFrame()        
        self.RIGHT_LAYOUT = widget.QVBoxLayout(self.RIGHT_PANEL)
        
        self.RIGHT_PANEL.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0, 
                    stop: 0 #87CEFA,
                    stop: 1 #FFDF56
                );
                border-radius: 10px;
            }
        """)

        self.MAIN_LAYOUT.addWidget(self.LEFT_PANEL)
        self.MAIN_LAYOUT.addWidget(self.RIGHT_PANEL)



window = WeatherApp()