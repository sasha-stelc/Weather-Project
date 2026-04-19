import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from PyQt6.QtWidgets import QCheckBox
from .card import WeatherCard
from .app import app


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
        self.LEFT_LAYOUT.setContentsMargins(0, 15, 0, 0) 

        self.TOP_BAR_LAYOUT = widget.QHBoxLayout()
        self.TOP_BAR_LAYOUT.setContentsMargins(15, 0, 15, 10)
        
        self.TOP_BAR_LAYOUT.addStretch() 
        self.LEFT_LAYOUT.addLayout(self.TOP_BAR_LAYOUT)

        self.SCROLL_AREA = widget.QScrollArea()
        self.SCROLL_AREA.setWidgetResizable(True)
        self.SCROLL_AREA.setFrameShape(widget.QFrame.Shape.NoFrame)
        self.SCROLL_AREA.setStyleSheet("background: transparent; border: none;")
        
        self.CARDS_CONTAINER = widget.QWidget()
        self.CARDS_CONTAINER.setStyleSheet("background: transparent;")
        
        self.CARDS_LAYOUT = widget.QVBoxLayout(self.CARDS_CONTAINER)
        self.CARDS_LAYOUT.setContentsMargins(15, 5, 15, 20)
        self.CARDS_LAYOUT.setSpacing(10)
        
        self.WEATHER_DATA = [
            {"city": "Дніпро", "time": "15:24", "temp": "11", "desc": "Переважно хмарно", "minmax": "Макс.:11°, мін.:0°", "is_current": True},
            {"city": "Київ", "time": "15:24", "temp": "14", "desc": "Сонячно", "minmax": "Макс.:15°, мін.:0°", "is_current": False},
            {"city": "Братіслава", "time": "14:24", "temp": "9", "desc": "Подекуди хмарно", "minmax": "Макс.:10°, мін.:1°", "is_current": False},
            {"city": "Варшава", "time": "14:24", "temp": "15", "desc": "Хмарно", "minmax": "Макс.:18°, мін.:7°", "is_current": False},
            {"city": "Рим", "time": "14:24", "temp": "24", "desc": "Сонячно", "minmax": "Макс.:25°, мін.:16°", "is_current": False},
        ]
        
        self.WEATHER_CARDS = []
        
        self.CENTRAL_FRAME.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0, 
                    stop: 0 #87CEFA,
                    stop: 1 #FFDF56
                );
                border-radius: 10px;
            }
        """)
        
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
        self.MAIN_LAYOUT.addWidget(self.LEFT_PANEL)
        self.MAIN_LAYOUT.addWidget(self.RIGHT_PANEL)


window = WeatherApp()