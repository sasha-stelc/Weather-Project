import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
import PyQt6.QtGui as gui
import os
from .langueges import LanguageManager
from .. import styles

class Images(widget.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.MAIN_LAYOUT = widget.QVBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        
        self.MAIN_FRAME = widget.QFrame()
        self.MAIN_FRAME.setFixedSize(544, 578)
        self.MAIN_LAYOUT.addWidget(self.MAIN_FRAME)

        frame_layout = widget.QVBoxLayout(self.MAIN_FRAME)
        frame_layout.setContentsMargins(0, 0, 0, 16)
        frame_layout.setSpacing(16)
        frame_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        self.PAGE_TITLE = widget.QLabel(LanguageManager.get_text("LISTS"))
        self.PAGE_TITLE.setStyleSheet("font-weight: 400; font-size: 24px;")
        frame_layout.addWidget(self.PAGE_TITLE)



        self.ADD_BUTTON = widget.QPushButton(LanguageManager.get_text("BTN_ADD_CITY"))
        self.ADD_BUTTON.setFixedSize(97, 36)
        self.ADD_BUTTON.setStyleSheet("background-color: rgba(0, 0, 0, 0.3)")
        frame_layout.addWidget(self.ADD_BUTTON, alignment=core.Qt.AlignmentFlag.AlignTop)




        self.NEW_IMAGES_FRAME = widget.QWidget()
        self.NEW_IMAGES_FRAME.setFixedSize(490, 136)
        self.NEW_IMAGES_FRAME.setStyleSheet("background-color: rgba(0, 0, 0, 0.3)")
        
        new_frame_layout = widget.QVBoxLayout(self.NEW_IMAGES_FRAME)
        new_frame_label = widget.QLabel(LanguageManager.get_text("LISTS_IMAGES"))
        new_frame_label.setStyleSheet("background-color: transparent")
        new_frame_layout.addWidget(new_frame_label, alignment=core.Qt.AlignmentFlag.AlignTop)
        
        # Горизонтальный лейаут для картинок
        new_images_h_layout = widget.QHBoxLayout()
        new_images_h_layout.setSpacing(5)
        new_images_h_layout.setContentsMargins(10, 0, 10, 0)
        
        # Добавляем 5 картинок в NEW_IMAGES_FRAME (01d, 02d, 03d, 04d, 05d)
        icon_names = ["01d.png", "02d.png", "03d.png", "03n.png", "02n.png"]
        
        for icon_name in icon_names:
            img_label = widget.QLabel()
            img_label.setFixedSize(74, 74)
            img_label.setStyleSheet("background-color: transparent")
            media_path = os.path.join(os.path.dirname(__file__), "..", "..", "media", "weather icon", icon_name)
            pixmap = gui.QPixmap(media_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(74, 74, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation)
                img_label.setPixmap(pixmap)
            new_images_h_layout.addWidget(img_label)
        
        new_frame_layout.addLayout(new_images_h_layout)
        
        frame_layout.addWidget(self.NEW_IMAGES_FRAME, alignment=core.Qt.AlignmentFlag.AlignBottom | core.Qt.AlignmentFlag.AlignLeft)

        self.PIXEL_IMAGES_FRAME = widget.QFrame()
        self.PIXEL_IMAGES_FRAME.setFixedSize(490, 136)
        self.PIXEL_IMAGES_FRAME.setStyleSheet("background-color: rgba(0, 0, 0, 0.3)")
        
        pixel_frame_layout = widget.QVBoxLayout(self.PIXEL_IMAGES_FRAME)
        pixel_frame_label = widget.QLabel(LanguageManager.get_text("LISTS_IMAGES2"))
        pixel_frame_label.setStyleSheet("background-color: transparent")
        pixel_frame_layout.addWidget(pixel_frame_label, alignment=core.Qt.AlignmentFlag.AlignTop)
        
        # Горизонтальный лейаут для картинок
        pixel_images_h_layout = widget.QHBoxLayout()
        pixel_images_h_layout.setSpacing(5)
        pixel_images_h_layout.setContentsMargins(10, 0, 10, 0)
        
        # Добавляем 5 картинок в PIXEL_IMAGES_FRAME (01d, 02d, 03d, 04d, 05d)
        pixel_icon_names = ["01d.png", "02d.png", "03d.png", "01n.png", "02n.png"]
        
        for icon_name in pixel_icon_names:
            img_label = widget.QLabel()
            img_label.setFixedSize(74, 74)
            img_label.setStyleSheet("background-color: transparent")
            media_path = os.path.join(os.path.dirname(__file__), "..", "..", "media", "weather icon2", icon_name)
            pixmap = gui.QPixmap(media_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(74, 74, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation)
                img_label.setPixmap(pixmap)
            pixel_images_h_layout.addWidget(img_label)
        
        pixel_frame_layout.addLayout(pixel_images_h_layout)

        frame_layout.addWidget(self.PIXEL_IMAGES_FRAME, alignment=core.Qt.AlignmentFlag.AlignCenter | core.Qt.AlignmentFlag.AlignLeft)
        
        # Кнопка Зберегти
        self.SAVE_BUTTON = widget.QPushButton(LanguageManager.get_text("BTN_SAVE"))
        self.SAVE_BUTTON.setFixedSize(105, 38)
        self.SAVE_BUTTON.setStyleSheet("background-color: rgba(0, 0, 0, 0.3)")
        frame_layout.addWidget(self.SAVE_BUTTON, alignment=core.Qt.AlignmentFlag.AlignBottom)

