import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from ..card import CityInfoFrame, HourlyForecastFrame, TwelveHourGraphFrame
from .. import styles


class RightPanel(widget.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(styles.RIGHT_PANEL)
        
        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setSpacing(15)
        self.LAYOUT.setContentsMargins(20, 10, 20, 10)
        
        # Верхняя панель с поиском
        self.SEARCH_FRAME = None
        
        # Информация о городе
        self.CITY_INFO_FRAME = None
        
        # Почасовой прогноз
        self.WEATHER_PANEL = widget.QFrame()
        self.WEATHER_PANEL.setFixedSize(788, 157)
        self.WEATHER_PANEL.setStyleSheet(styles.TRANSPARENT_BG)
        self.WEATHER_LAYOUT = widget.QVBoxLayout(self.WEATHER_PANEL)
        self.WEATHER_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.WEATHER_LAYOUT.setSpacing(0)
        self.HOURLY_FRAME = None
        
        # График на 12 часов
        self.BOTTOM_PANEL = widget.QFrame()
        self.BOTTOM_PANEL.setFixedSize(788, 197)
        self.BOTTOM_PANEL.setStyleSheet(styles.TRANSPARENT_BG)
        self.BOTTOM_LAYOUT = widget.QVBoxLayout(self.BOTTOM_PANEL)
        self.BOTTOM_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.BOTTOM_LAYOUT.setSpacing(0)
        self.GRAPH_FRAME = None
        
        self.LAYOUT.addStretch()
        self.LAYOUT.addWidget(self.WEATHER_PANEL,
            alignment=core.Qt.AlignmentFlag.AlignBottom)
        self.LAYOUT.addWidget(self.BOTTOM_PANEL,
            alignment=core.Qt.AlignmentFlag.AlignBottom)
    
    def set_search_frame(self, search_frame):
        """Устанавливает фрейм поиска в верхнюю часть."""
        self.SEARCH_FRAME = search_frame
        self.LAYOUT.insertWidget(0, self.SEARCH_FRAME,
            alignment=core.Qt.AlignmentFlag.AlignTop)
    
    def set_city_info(self, weather_data):
        """Отображает информацию о городе."""
        self.clear_weather_ui()
        self.CITY_INFO_FRAME = CityInfoFrame(weather_data)
        self.LAYOUT.insertWidget(1, self.CITY_INFO_FRAME)
    
    def set_hourly_forecast(self, weather_data):
        """Отображает почасовой прогноз."""
        self.HOURLY_FRAME = HourlyForecastFrame(weather_data)
        self.WEATHER_LAYOUT.addWidget(self.HOURLY_FRAME)
    
    def set_twelve_hour_graph(self, weather_data):
        """Отображает график на 12 часов."""
        self.GRAPH_FRAME = TwelveHourGraphFrame(weather_data)
        self.BOTTOM_LAYOUT.addWidget(self.GRAPH_FRAME)
    
    def clear_weather_ui(self):
        """Очищает все компоненты погоды."""
        if self.CITY_INFO_FRAME:
            self.LAYOUT.removeWidget(self.CITY_INFO_FRAME)
            self.CITY_INFO_FRAME.deleteLater()
            self.CITY_INFO_FRAME = None
        if self.HOURLY_FRAME:
            self.WEATHER_LAYOUT.removeWidget(self.HOURLY_FRAME)
            self.HOURLY_FRAME.deleteLater()
            self.HOURLY_FRAME = None
        if self.GRAPH_FRAME:
            self.BOTTOM_LAYOUT.removeWidget(self.GRAPH_FRAME)
            self.GRAPH_FRAME.deleteLater()
            self.GRAPH_FRAME = None
