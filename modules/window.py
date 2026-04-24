import os
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .card import WeatherCard
from . import styles


def create_media_path(name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(current_dir, "..", "media", name))


class ImageThemeSwitch(widget.QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCheckable(True)
        self.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(52, 24)
        self.setIconSize(core.QSize(18, 18))

        self.sun_icon = gui.QIcon(create_media_path("Frame_51.png"))
        self.moon_icon = gui.QIcon(create_media_path("Frame_52.png"))

        self.toggled.connect(self.update_image)

        self.setChecked(False)
        self.update_image(self.isChecked())

    def update_image(self, checked: bool):

        self.setStyleSheet(styles.THEME_BUTTON_SUN if checked else styles.THEME_BUTTON_MOON)
        self.setIcon(self.sun_icon if checked else self.moon_icon)


class WeatherApp(widget.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Погода")
        self.resize(1200, 800)

        central_widget = widget.QWidget()
        central_widget.setStyleSheet(styles.CENTRAL_WIDGET)
        self.setCentralWidget(central_widget)

        self.main_layout = widget.QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        left_panel = widget.QFrame()
        left_panel.setFixedWidth(370)
        left_panel.setStyleSheet(styles.LEFT_PANEL)

        left_layout = widget.QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 0)
        left_layout.setSpacing(10)

        top_bar_frame = widget.QFrame(left_panel)
        top_bar_frame.setFixedSize(core.QSize(330, 44))

        top_bar_layout = widget.QHBoxLayout(top_bar_frame)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)

        theme_button = ImageThemeSwitch()
        top_bar_layout.addWidget(theme_button, alignment=core.Qt.AlignmentFlag.AlignRight)

        left_layout.addWidget(top_bar_frame)

        scroll_area = widget.QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(widget.QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet(styles.SCROLL_AREA)

        cards_container = widget.QWidget()
        cards_container.setStyleSheet(styles.CARDS_CONTAINER)

        cards_layout = widget.QVBoxLayout(cards_container)
        cards_layout.setContentsMargins(10, 10, 10, 20)
        cards_layout.setSpacing(10)

        self.weather_data = [
            {"city": "Дніпро", "time": "15:24", "temp": "11", "desc": "Переважно хмарно", "minmax": "Макс.:11°, мін.:0°", "is_current": False},
            {"city": "Київ", "time": "15:24", "temp": "14", "desc": "Сонячно", "minmax": "Макс.:15°, мін.:0°", "is_current": False},
            {"city": "Братіслава", "time": "14:24", "temp": "9", "desc": "Подекуди хмарно", "minmax": "Макс.:10°, мін.:1°", "is_current": False},
            {"city": "Варшава", "time": "14:24", "temp": "15", "desc": "Хмарно", "minmax": "Макс.:18°, мін.:7°", "is_current": False},
            {"city": "Рим", "time": "14:24", "temp": "24", "desc": "Сонячно", "minmax": "Макс.:25°, мін.:16°", "is_current": False},
        ]

        self.weather_cards = []
        self.selected_card = None

        for data in self.weather_data:

            card = WeatherCard(data["city"], data["time"], data["temp"], data["desc"], data["minmax"], data["is_current"])

            card.selected.connect(self.on_card_selected)

            self.weather_cards.append(card)
            cards_layout.addWidget(card)

        cards_layout.addStretch()

        scroll_area.setWidget(cards_container)
        left_layout.addWidget(scroll_area)

        right_panel = widget.QFrame()
        right_panel.setStyleSheet(styles.RIGHT_PANEL)

        self.main_layout.addWidget(left_panel)
        self.main_layout.addWidget(right_panel)

    def on_card_selected(self, card: WeatherCard):

        if self.selected_card and self.selected_card != card:
            self.selected_card.set_selected(False)

        card.set_selected(not card.is_selected)

        self.selected_card = card if card.is_selected else None


window = WeatherApp()