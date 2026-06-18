import PyQt6.QtCore as core
import PyQt6.QtWidgets as widget
import PyQt6.QtGui as gui
import os
import re
import shutil

from .langueges import LanguageManager
from .. import styles


SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")

BUILTIN_THEME_LABEL_KEYS = {
    "weather icon": "LISTS_IMAGES",
    "weather icon2": "LISTS_IMAGES2",
}


HIDDEN_THEME_FOLDERS = {"weather icon Bl WI"}


class ClickableFrame(widget.QFrame):
    """QFrame that behaves like a selectable card and emits `clicked` on left click."""

    clicked = core.pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class ClickableLabel(widget.QLabel):
    """QLabel that emits `clicked` on left click, used for the icon thumbnails."""

    clicked = core.pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class Images(widget.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.SETTINGS = core.QSettings("WeatherProject", "WeatherApp")

        self.MEDIA_FOLDER = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "..", "media")
        )
        self.DEFAULT_THEME_FOLDER = os.path.join(self.MEDIA_FOLDER, "weather icon")

        self.SELECTED_THEME = self.SETTINGS.value("selected_theme", "weather icon")
        self.THEME_CARDS = {}

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
        self.PAGE_TITLE.setStyleSheet("font-weight: 400; font-size: 24px; color: white;")
        frame_layout.addWidget(self.PAGE_TITLE)

        self.ADD_BUTTON = widget.QPushButton(LanguageManager.get_text("BTN_ADD_CITY"))
        self.ADD_BUTTON.setFixedSize(140, 36)
        self.ADD_BUTTON.setStyleSheet("background-color: rgba(0,0,0,0.3); color: white;")
        self.ADD_BUTTON.clicked.connect(self.OPEN_ADD_PRESET_MODAL)
        frame_layout.addWidget(self.ADD_BUTTON, alignment=core.Qt.AlignmentFlag.AlignTop)

        self.CARDS_SCROLL = widget.QScrollArea()
        self.CARDS_SCROLL.setWidgetResizable(True)
        self.CARDS_SCROLL.setFrameShape(widget.QFrame.Shape.NoFrame)
        self.CARDS_SCROLL.setStyleSheet("background: transparent;")
        self.CARDS_SCROLL.setFixedHeight(340)

        self.CARDS_CONTAINER = widget.QWidget()
        self.CARDS_CONTAINER.setStyleSheet("background: transparent")
        self.CARDS_LAYOUT = widget.QVBoxLayout(self.CARDS_CONTAINER)
        self.CARDS_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CARDS_LAYOUT.setSpacing(12)
        self.CARDS_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.CARDS_SCROLL.setWidget(self.CARDS_CONTAINER)

        frame_layout.addWidget(self.CARDS_SCROLL)

        self.SAVE_BUTTON = widget.QPushButton(LanguageManager.get_text("BTN_SAVE"))
        self.SAVE_BUTTON.setFixedSize(105, 38)
        self.SAVE_BUTTON.setStyleSheet("background-color: rgba(0,0,0,0.3); color: white;")
        self.SAVE_BUTTON.clicked.connect(self.SAVE_SELECTION)
        frame_layout.addWidget(self.SAVE_BUTTON, alignment=core.Qt.AlignmentFlag.AlignBottom)

        self.REBUILD_THEME_CARDS()



    def TR(self, key, default):
        try:
            text = LanguageManager.get_text(key)
        except Exception:
            return default
        if not text or text == key:
            return default
        return text

    def GET_IMAGE_FILES(self, folder_path):
        if not os.path.isdir(folder_path):
            return []
        return sorted(
            f for f in os.listdir(folder_path)
            if f.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS)
        )



    def REBUILD_THEME_CARDS(self):
        while self.CARDS_LAYOUT.count():
            item = self.CARDS_LAYOUT.takeAt(0)
            card_widget = item.widget()
            if card_widget:
                card_widget.deleteLater()
        self.THEME_CARDS = {}

        if not os.path.isdir(self.MEDIA_FOLDER):
            return

        builtin_order = ["weather icon", "weather icon2"]
        all_folders = [
            name for name in os.listdir(self.MEDIA_FOLDER)
            if os.path.isdir(os.path.join(self.MEDIA_FOLDER, name))
            and name not in HIDDEN_THEME_FOLDERS
        ]
        ordered_folders = [f for f in builtin_order if f in all_folders]
        ordered_folders += sorted(f for f in all_folders if f not in builtin_order)

        for folder_name in ordered_folders:
            self.CARDS_LAYOUT.addWidget(self.BUILD_THEME_CARD(folder_name))

        self.UPDATE_THEME_SELECTION_STYLES()

    def BUILD_THEME_CARD(self, folder_name):
        folder_path = os.path.join(self.MEDIA_FOLDER, folder_name)

        card = ClickableFrame()
        card.setFixedSize(490, 136)
        card.setCursor(core.Qt.CursorShape.PointingHandCursor)
        card.clicked.connect(lambda name=folder_name: self.SELECT_THEME(name))

        card_layout = widget.QVBoxLayout(card)

        label_key = BUILTIN_THEME_LABEL_KEYS.get(folder_name)
        base_title = LanguageManager.get_text(label_key) if label_key else folder_name

        title_label = widget.QLabel(base_title)
        title_label.setStyleSheet("background-color: transparent; color: white;")
        card_layout.addWidget(title_label, alignment=core.Qt.AlignmentFlag.AlignTop)

        icons_layout = widget.QHBoxLayout()
        icons_layout.setSpacing(5)
        icons_layout.setContentsMargins(10, 0, 10, 0)

        for icon_name in self.GET_IMAGE_FILES(folder_path)[:5]:
            img_label = widget.QLabel()
            img_label.setFixedSize(74, 74)
            img_label.setStyleSheet("background-color: transparent")

            pixmap = gui.QPixmap(os.path.join(folder_path, icon_name))
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    74, 74,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation,
                )
                img_label.setPixmap(pixmap)

            icons_layout.addWidget(img_label)

        icons_layout.addStretch()
        card_layout.addLayout(icons_layout)

        self.THEME_CARDS[folder_name] = {
            "frame": card,
            "title_label": title_label,
            "base_title": base_title,
        }
        return card

    def SELECT_THEME(self, folder_name):
        self.SELECTED_THEME = folder_name
        self.UPDATE_THEME_SELECTION_STYLES()

    def UPDATE_THEME_SELECTION_STYLES(self):
        for folder_name, parts in self.THEME_CARDS.items():
            is_selected = folder_name == self.SELECTED_THEME

            parts["frame"].setStyleSheet(
                "background-color: rgba(0, 0, 0, 0.3);"
                "border-radius: 4px;"
                + (
                    "border: 2px solid rgba(255, 255, 255, 0.85);"
                    if is_selected
                    else "border: 2px solid transparent;"
                )
            )

            suffix = "  \u2713" if is_selected else ""
            parts["title_label"].setText(parts["base_title"] + suffix)

    def SAVE_SELECTION(self):
        self.SETTINGS.setValue("selected_theme", self.SELECTED_THEME)

    # ------------------------------------------------------------------
    # Custom preset creation: small "name it" modal -> folder created
    # under media/ -> full-screen icon editor seeded with the defaults
    # ------------------------------------------------------------------

    def OPEN_ADD_PRESET_MODAL(self):
        self.ADD_PRESET_DIALOG = widget.QDialog(self)
        self.ADD_PRESET_DIALOG.setWindowTitle(self.TR("ADD_PRESET_TITLE", "New preset"))
        self.ADD_PRESET_DIALOG.setFixedSize(320, 170)
        self.ADD_PRESET_DIALOG.setStyleSheet("background-color: rgb(40, 40, 40); color: white;")

        dialog_layout = widget.QVBoxLayout(self.ADD_PRESET_DIALOG)
        dialog_layout.setContentsMargins(20, 20, 20, 20)
        dialog_layout.setSpacing(10)

        name_label = widget.QLabel(self.TR("PRESET_NAME_LABEL", "Preset folder name"))
        name_label.setStyleSheet("background: transparent; color: white;")
        dialog_layout.addWidget(name_label)

        self.PRESET_NAME_INPUT = widget.QLineEdit()
        self.PRESET_NAME_INPUT.setPlaceholderText(self.TR("PRESET_NAME_PLACEHOLDER", "e.g. my_theme"))
        self.PRESET_NAME_INPUT.setStyleSheet(
            "background-color: rgba(255,255,255,0.08); color: white;"
            "border: 1px solid rgba(255,255,255,0.3); border-radius: 4px; padding: 4px;"
        )
        dialog_layout.addWidget(self.PRESET_NAME_INPUT)

        self.PRESET_ERROR_LABEL = widget.QLabel("")
        self.PRESET_ERROR_LABEL.setWordWrap(True)
        self.PRESET_ERROR_LABEL.setStyleSheet("background: transparent; color: #ff6b6b; font-size: 11px;")
        dialog_layout.addWidget(self.PRESET_ERROR_LABEL)

        dialog_layout.addStretch()

        buttons_layout = widget.QHBoxLayout()

        # Close is always available, regardless of what (if anything) was typed.
        close_button = widget.QPushButton(self.TR("BTN_CLOSE", "Close"))
        close_button.setStyleSheet("background-color: rgba(0,0,0,0.3); color: white;")
        close_button.clicked.connect(self.ADD_PRESET_DIALOG.reject)
        buttons_layout.addWidget(close_button)

        save_button = widget.QPushButton(LanguageManager.get_text("BTN_SAVE"))
        save_button.setStyleSheet("background-color: rgba(0,0,0,0.3); color: white;")
        save_button.clicked.connect(self.CREATE_PRESET_FOLDER)
        buttons_layout.addWidget(save_button)

        dialog_layout.addLayout(buttons_layout)

        self.ADD_PRESET_DIALOG.exec()
        self.ADD_PRESET_DIALOG.deleteLater()

    def CREATE_PRESET_FOLDER(self):
        raw_name = self.PRESET_NAME_INPUT.text().strip()

        if not raw_name:
            self.PRESET_ERROR_LABEL.setText(self.TR("PRESET_NAME_EMPTY", "Enter a folder name."))
            return

        safe_name = re.sub(r'[\\/:*?"<>|]', "", raw_name).strip().strip(".")

        if not safe_name:
            self.PRESET_ERROR_LABEL.setText(self.TR("PRESET_NAME_INVALID", "That name isn't valid."))
            return

        new_folder_path = os.path.join(self.MEDIA_FOLDER, safe_name)

        if os.path.exists(new_folder_path):
            self.PRESET_ERROR_LABEL.setText(
                self.TR("PRESET_NAME_TAKEN", "A preset with that name already exists.")
            )
            return

        try:
            os.makedirs(new_folder_path)
        except OSError:
            self.PRESET_ERROR_LABEL.setText(self.TR("PRESET_CREATE_FAILED", "Couldn't create the folder."))
            return

        # Seed the new preset with the default icon set so every icon the app
        # needs already exists; the user can then override any of them below.
        for icon_name in self.GET_IMAGE_FILES(self.DEFAULT_THEME_FOLDER):
            try:
                shutil.copy(
                    os.path.join(self.DEFAULT_THEME_FOLDER, icon_name),
                    os.path.join(new_folder_path, icon_name),
                )
            except OSError:
                pass

        self.ADD_PRESET_DIALOG.accept()

        self.REBUILD_THEME_CARDS()
        self.SELECT_THEME(safe_name)

        self.OPEN_ICON_EDITOR_MODAL(new_folder_path, safe_name)

    # ------------------------------------------------------------------
    # Full-screen icon editor for a preset folder
    # ------------------------------------------------------------------

    def OPEN_ICON_EDITOR_MODAL(self, folder_path, folder_name):
        self.ICON_EDITOR_FOLDER = folder_path

        self.ICON_EDITOR_DIALOG = widget.QDialog(self)
        self.ICON_EDITOR_DIALOG.setWindowTitle(folder_name)
        self.ICON_EDITOR_DIALOG.setStyleSheet("background-color: rgb(30, 30, 30); color: white;")

        outer_layout = widget.QVBoxLayout(self.ICON_EDITOR_DIALOG)
        outer_layout.setContentsMargins(30, 30, 30, 30)
        outer_layout.setSpacing(16)

        title_label = widget.QLabel(folder_name)
        title_label.setStyleSheet("background: transparent; font-size: 20px; color: white;")
        outer_layout.addWidget(title_label)

        hint_label = widget.QLabel(
            self.TR("ICON_EDITOR_HINT", "Click an icon to replace it with your own image.")
        )
        hint_label.setStyleSheet("background: transparent; color: rgba(255,255,255,0.6); font-size: 12px;")
        outer_layout.addWidget(hint_label)

        scroll = widget.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(widget.QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        self.ICON_GRID_CONTAINER = widget.QWidget()
        self.ICON_GRID_CONTAINER.setStyleSheet("background: transparent")
        self.ICON_GRID_LAYOUT = widget.QGridLayout(self.ICON_GRID_CONTAINER)
        self.ICON_GRID_LAYOUT.setSpacing(18)

        scroll.setWidget(self.ICON_GRID_CONTAINER)
        outer_layout.addWidget(scroll)

        done_button = widget.QPushButton(LanguageManager.get_text("BTN_SAVE"))
        done_button.setFixedSize(120, 40)
        done_button.setStyleSheet("background-color: rgba(0,0,0,0.3); color: white;")
        done_button.clicked.connect(self.ICON_EDITOR_DIALOG.accept)
        outer_layout.addWidget(done_button, alignment=core.Qt.AlignmentFlag.AlignRight)

        self.RENDER_ICON_GRID()

        self.ICON_EDITOR_DIALOG.showFullScreen()
        self.ICON_EDITOR_DIALOG.exec()
        self.ICON_EDITOR_DIALOG.deleteLater()

        # Pick up any icon changes made while the editor was open.
        self.REBUILD_THEME_CARDS()

    def RENDER_ICON_GRID(self):
        while self.ICON_GRID_LAYOUT.count():
            item = self.ICON_GRID_LAYOUT.takeAt(0)
            cell_widget = item.widget()
            if cell_widget:
                cell_widget.deleteLater()

        image_files = self.GET_IMAGE_FILES(self.ICON_EDITOR_FOLDER)

        if not image_files:
            empty_label = widget.QLabel(self.TR("NO_ICONS_FOUND", "No icons found in this preset yet."))
            empty_label.setStyleSheet("background: transparent; color: rgba(255,255,255,0.7);")
            self.ICON_GRID_LAYOUT.addWidget(empty_label, 0, 0)
            return

        columns = 6

        for index, icon_name in enumerate(image_files):
            cell = widget.QWidget()
            cell.setStyleSheet("background: transparent")

            cell_layout = widget.QVBoxLayout(cell)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.setSpacing(6)
            cell_layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

            icon_label = ClickableLabel()
            icon_label.setFixedSize(90, 90)
            icon_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("background-color: rgba(0,0,0,0.3); border-radius: 6px;")
            icon_label.setCursor(core.Qt.CursorShape.PointingHandCursor)

            pixmap = gui.QPixmap(os.path.join(self.ICON_EDITOR_FOLDER, icon_name))
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    70, 70,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation,
                )
                icon_label.setPixmap(pixmap)

            icon_label.clicked.connect(lambda name=icon_name: self.REPLACE_ICON(name))
            cell_layout.addWidget(icon_label, alignment=core.Qt.AlignmentFlag.AlignCenter)

            name_label = widget.QLabel(icon_name)
            name_label.setStyleSheet("background: transparent; font-size: 11px; color: white;")
            name_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            cell_layout.addWidget(name_label)

            row, col = divmod(index, columns)
            self.ICON_GRID_LAYOUT.addWidget(cell, row, col)

    def REPLACE_ICON(self, icon_name):
        file_path, _ = widget.QFileDialog.getOpenFileName(
            self,
            self.TR("CHOOSE_IMAGE_TITLE", "Choose an image"),
            os.path.expanduser("~"),
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
        )

        if not file_path:
            return

        source_image = gui.QImage(file_path)

        if source_image.isNull():
            widget.QMessageBox.warning(
                self,
                self.TR("ERROR_TITLE", "Error"),
                self.TR("ICON_INVALID_IMAGE", "That file couldn't be read as an image."),
            )
            return

        # Save under the original icon's filename, so it slots into the
        # preset exactly where the icon being replaced used to be.
        destination = os.path.join(self.ICON_EDITOR_FOLDER, icon_name)

        if not source_image.save(destination):
            widget.QMessageBox.warning(
                self,
                self.TR("ERROR_TITLE", "Error"),
                self.TR("ICON_COPY_FAILED", "Couldn't save that image."),
            )
            return

        self.RENDER_ICON_GRID()