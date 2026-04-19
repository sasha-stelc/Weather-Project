import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core


class Card(widget.QFrame):
    def __init__(self, width: int, height: int, parent=None, right_layout=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setParent(parent)
        self.setFixedSize(width, height)
        
        self.RIGHT_LAYOUT = right_layout
        
        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setContentsMargins(22, 55, 20, 40)
        
class WeatherCard(widget.QFrame):
    def __init__(self, city, time, temp, desc, minmax, is_current=False):
        super().__init__()
        
        self.GRID_LAYOUT = widget.QGridLayout(self)
        self.GRID_LAYOUT.setContentsMargins(15, 15, 15, 15)
        self.GRID_LAYOUT.setHorizontalSpacing(10)
        
        self.CITY_LABEL = widget.QLabel(city)
        self.CITY_LABEL.setStyleSheet("font-size: 28px; font-weight: bold;")
        
        self.TIME_LABEL = widget.QLabel(time)
        self.TIME_LABEL.setStyleSheet("font-size: 14px; opacity: 0.8;")
        
        self.TEMP_LABEL = widget.QLabel(f"{temp}°")
        self.TEMP_LABEL.setStyleSheet("font-size: 48px;")
        self.TEMP_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignTop)
        
        self.DESC_LABEL = widget.QLabel(desc)
        self.DESC_LABEL.setStyleSheet("font-size: 14px;")
        
        self.MINMAX_LABEL = widget.QLabel(minmax)
        self.MINMAX_LABEL.setStyleSheet("font-size: 14px;")
        self.MINMAX_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignBottom)

        self.GRID_LAYOUT.addWidget(self.CITY_LABEL, 0, 0)
        self.GRID_LAYOUT.addWidget(self.TIME_LABEL, 1, 0)
        self.GRID_LAYOUT.addWidget(self.TEMP_LABEL, 0, 1, 2, 1)
        self.GRID_LAYOUT.addWidget(self.DESC_LABEL, 2, 0)
        self.GRID_LAYOUT.addWidget(self.MINMAX_LABEL, 2, 1)

        self.IS_CURRENT = is_current

        if self.IS_CURRENT:
            self.setStyleSheet("""
                WeatherCard {
                    background-color: rgba(0, 0, 0, 60); 
                    border-radius: 15px;
                }
                QLabel { color: white; background: transparent; }
            """)
        else:
            self.setStyleSheet("""
                WeatherCard {
                    background-color: transparent;
                    border-bottom: 1px solid rgba(255, 255, 255, 40); 
                    border-radius: 0px;
                }
                QLabel { color: white; background: transparent; border: none; }
            """)