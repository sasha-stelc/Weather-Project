import PyQt6.QtCore as core


class _SizeSignalEmitter(core.QObject):
    size_changed = core.pyqtSignal(int, int)


# Глобальный сигнал смены размера (как LANGUAGE_SIGNAL у LanguageManager)
SIZE_SIGNAL = _SizeSignalEmitter()


# ===== СЛОВАРЬ СТАТИЧНИХ РОЗМІРІВ ДЛЯ КОЖНОГО ПРЕСЕТУ =====
#
# Ключ верхнього рівня — "WIDTHxHEIGHT" (як у Application.SIZES).
# Кожен пресет містить усі статичні setFixedSize / setFixedWidth /
# setFixedHeight / setMinimum* / setMaximum* / QSize, які раніше були
# зашиті константами безпосередньо у віджетах.
#
# Базовий пресет — 1200x800 (значення з поточного коду без змін).
# Інші пресети масштабовані пропорційно (коеф. = новий_width / 1200),
# з округленням та розумними мінімумами там, де це важливо для UI.

SIZES = {

    # ───────────────────────── 1200x800 (базовий) ─────────────────────────
    "1200x800": {
        "window": {"width": 1200, "height": 800},

        # window/theme_switch.py
        "theme_switch":        {"width": 52,  "height": 24},
        "theme_switch_icon":   {"width": 18,  "height": 18},

        # window/right_panel.py
        "weather_panel":       {"width": 788, "height": 157},
        "bottom_panel":        {"width": 788, "height": 197},

        # window/settings_panel.py
        "settings_panel":      {"width": 150, "height": 45},
        "settings_box":        {"width": 45,  "height": 45},
        "settings_btn":        {"width": 45,  "height": 45},
        "settings_btn_icon":   {"width": 20,  "height": 20},

        # window/left_panel.py
        "left_panel_width":    370,

        # window/search_panel.py
        "search_panel_height":   45,
        "search_container":      {"width": 261, "height": 36},
        "search_icon_lbl":        {"width": 18,  "height": 18},
        "clear_btn":              {"width": 18,  "height": 18},
        "clear_btn_icon":         {"width": 18,  "height": 18},
        "add_city_btn":           {"width": 100, "height": 34},

        # card/weather_card.py
        "weather_card_max":   {"width": 330, "height": 104},
        "weather_card_choice_icon": {"width": 20, "height": 20},

        # card/hourly_forecast_frame.py
        "hourly_forecast_height": 157,
        "hourly_line_height":     1,
        "hourly_arrow":           {"width": 20, "height": 40},
        "hourly_arrow_icon":      {"width": 16, "height": 16},
        "hourly_item_min_width":  90,

        # card/twelve_hour_graph_frame.py
        "graph_line_height": 1,

        # card/city_info_frame.py
        "city_info_left_max":     {"width": 390, "height": 303},
        "city_info_location_icon": {"width": 20, "height": 20},
        "city_info_separator_height": 1,
        "city_info_icon_lbl":     {"width": 150, "height": 70},
        "city_info_right_max":    {"width": 390, "height": 303},
        "city_info_right_separator_height": 1,
        "clock_widget":           {"width": 160, "height": 160},  # X, Y у city_info_frame.py

        # settings/search_sity.py
        "confirm_button":     {"width": 105, "height": 38},
        "city_frame":         {"width": 544, "height": 160},
        "delete_btn":         {"width": 24,  "height": 24},

        # settings/application_size.py
        "size_save_button":   {"width": 105, "height": 38},

        # settings/settings.py
        "settings_window":        {"width": 790, "height": 688},
        "settings_min_height":    35,
        "settings_min_width":     140,
        "settings_top_bar_min_h": 60,
        "settings_close_btn":     {"width": 32, "height": 32},
        "settings_left_frame_min_w": 190,

        # settings/langueges.py
        "lang_form_frame_width": 239,
        "lang_combo":            {"width": 239, "height": 32},
        "lang_confirm_button":   {"width": 105, "height": 38},

        # title_bar.py
        "title_bar_height": 26,
    },

    # ───────────────────────── 1440x1024 ─────────────────────────
    "1440x1024": {
        "window": {"width": 1440, "height": 1024},

        "theme_switch":        {"width": 62,  "height": 29},
        "theme_switch_icon":   {"width": 22,  "height": 22},

        "weather_panel":       {"width": 946, "height": 188},
        "bottom_panel":        {"width": 946, "height": 236},

        "settings_panel":      {"width": 180, "height": 54},
        "settings_box":        {"width": 54,  "height": 54},
        "settings_btn":        {"width": 54,  "height": 54},
        "settings_btn_icon":   {"width": 24,  "height": 24},

        "left_panel_width":    444,

        "search_panel_height":   54,
        "search_container":      {"width": 313, "height": 43},
        "search_icon_lbl":        {"width": 22,  "height": 22},
        "clear_btn":              {"width": 22,  "height": 22},
        "clear_btn_icon":         {"width": 22,  "height": 22},
        "add_city_btn":           {"width": 120, "height": 41},

        "weather_card_max":   {"width": 396, "height": 125},
        "weather_card_choice_icon": {"width": 24, "height": 24},

        "hourly_forecast_height": 188,
        "hourly_line_height":     1,
        "hourly_arrow":           {"width": 24, "height": 48},
        "hourly_arrow_icon":      {"width": 19, "height": 19},
        "hourly_item_min_width":  108,

        "graph_line_height": 1,

        "city_info_left_max":     {"width": 468, "height": 364},
        "city_info_location_icon": {"width": 24, "height": 24},
        "city_info_separator_height": 1,
        "city_info_icon_lbl":     {"width": 180, "height": 84},
        "city_info_right_max":    {"width": 468, "height": 364},
        "city_info_right_separator_height": 1,
        "clock_widget":           {"width": 192, "height": 192},

        "confirm_button":     {"width": 126, "height": 46},
        "city_frame":         {"width": 653, "height": 192},
        "delete_btn":         {"width": 29,  "height": 29},

        "size_save_button":   {"width": 126, "height": 46},

        "settings_window":        {"width": 948, "height": 880},
        "settings_min_height":    42,
        "settings_min_width":     168,
        "settings_top_bar_min_h": 72,
        "settings_close_btn":     {"width": 38, "height": 38},
        "settings_left_frame_min_w": 228,

        "lang_form_frame_width": 287,
        "lang_combo":            {"width": 287, "height": 38},
        "lang_confirm_button":   {"width": 126, "height": 46},

        "title_bar_height": 31,
    },

    # ───────────────────────── 1512x982 ─────────────────────────
    "1512x982": {
        "window": {"width": 1512, "height": 982},

        "theme_switch":        {"width": 66,  "height": 30},
        "theme_switch_icon":   {"width": 23,  "height": 23},

        "weather_panel":       {"width": 993, "height": 193},
        "bottom_panel":        {"width": 993, "height": 242},

        "settings_panel":      {"width": 189, "height": 57},
        "settings_box":        {"width": 57,  "height": 57},
        "settings_btn":        {"width": 57,  "height": 57},
        "settings_btn_icon":   {"width": 25,  "height": 25},

        "left_panel_width":    466,

        "search_panel_height":   57,
        "search_container":      {"width": 329, "height": 45},
        "search_icon_lbl":        {"width": 23,  "height": 23},
        "clear_btn":              {"width": 23,  "height": 23},
        "clear_btn_icon":         {"width": 23,  "height": 23},
        "add_city_btn":           {"width": 126, "height": 43},

        "weather_card_max":   {"width": 416, "height": 128},
        "weather_card_choice_icon": {"width": 25, "height": 25},

        "hourly_forecast_height": 193,
        "hourly_line_height":     1,
        "hourly_arrow":           {"width": 25, "height": 49},
        "hourly_arrow_icon":      {"width": 20, "height": 20},
        "hourly_item_min_width":  113,

        "graph_line_height": 1,

        "city_info_left_max":     {"width": 491, "height": 372},
        "city_info_location_icon": {"width": 25, "height": 25},
        "city_info_separator_height": 1,
        "city_info_icon_lbl":     {"width": 189, "height": 86},
        "city_info_right_max":    {"width": 491, "height": 372},
        "city_info_right_separator_height": 1,
        "clock_widget":           {"width": 202, "height": 202},

        "confirm_button":     {"width": 132, "height": 47},
        "city_frame":         {"width": 685, "height": 196},
        "delete_btn":         {"width": 30,  "height": 30},

        "size_save_button":   {"width": 132, "height": 47},

        "settings_window":        {"width": 995, "height": 844},
        "settings_min_height":    44,
        "settings_min_width":     176,
        "settings_top_bar_min_h": 74,
        "settings_close_btn":     {"width": 40, "height": 40},
        "settings_left_frame_min_w": 239,

        "lang_form_frame_width": 301,
        "lang_combo":            {"width": 301, "height": 39},
        "lang_confirm_button":   {"width": 132, "height": 47},

        "title_bar_height": 32,
    },

    # ───────────────────────── 1728x1117 ─────────────────────────
    "1728x1117": {
        "window": {"width": 1728, "height": 1117},

        "theme_switch":        {"width": 75,  "height": 35},
        "theme_switch_icon":   {"width": 26,  "height": 26},

        "weather_panel":       {"width": 1135, "height": 219},
        "bottom_panel":        {"width": 1135, "height": 275},

        "settings_panel":      {"width": 216, "height": 65},
        "settings_box":        {"width": 65,  "height": 65},
        "settings_btn":        {"width": 65,  "height": 65},
        "settings_btn_icon":   {"width": 29,  "height": 29},

        "left_panel_width":    533,

        "search_panel_height":   65,
        "search_container":      {"width": 376, "height": 52},
        "search_icon_lbl":        {"width": 26,  "height": 26},
        "clear_btn":              {"width": 26,  "height": 26},
        "clear_btn_icon":         {"width": 26,  "height": 26},
        "add_city_btn":           {"width": 144, "height": 49},

        "weather_card_max":   {"width": 475, "height": 145},
        "weather_card_choice_icon": {"width": 29, "height": 29},

        "hourly_forecast_height": 219,
        "hourly_line_height":     1,
        "hourly_arrow":           {"width": 29, "height": 56},
        "hourly_arrow_icon":      {"width": 23, "height": 23},
        "hourly_item_min_width":  129,

        "graph_line_height": 1,

        "city_info_left_max":     {"width": 561, "height": 423},
        "city_info_location_icon": {"width": 29, "height": 29},
        "city_info_separator_height": 1,
        "city_info_icon_lbl":     {"width": 216, "height": 98},
        "city_info_right_max":    {"width": 561, "height": 423},
        "city_info_right_separator_height": 1,
        "clock_widget":           {"width": 230, "height": 230},

        "confirm_button":     {"width": 151, "height": 55},
        "city_frame":         {"width": 783, "height": 223},
        "delete_btn":         {"width": 35,  "height": 35},

        "size_save_button":   {"width": 151, "height": 55},

        "settings_window":        {"width": 1137, "height": 960},
        "settings_min_height":    50,
        "settings_min_width":     201,
        "settings_top_bar_min_h": 84,
        "settings_close_btn":     {"width": 46, "height": 46},
        "settings_left_frame_min_w": 273,

        "lang_form_frame_width": 344,
        "lang_combo":            {"width": 344, "height": 46},
        "lang_confirm_button":   {"width": 151, "height": 55},

        "title_bar_height": 36,
    },

    # ───────────────────────── 1920x1080 ─────────────────────────
    "1920x1080": {
        "window": {"width": 1920, "height": 1080},

        "theme_switch":        {"width": 83,  "height": 38},
        "theme_switch_icon":   {"width": 29,  "height": 29},

        "weather_panel":       {"width": 1261, "height": 212},
        "bottom_panel":        {"width": 1261, "height": 266},

        "settings_panel":      {"width": 240, "height": 72},
        "settings_box":        {"width": 72,  "height": 72},
        "settings_btn":        {"width": 72,  "height": 72},
        "settings_btn_icon":   {"width": 32,  "height": 32},

        "left_panel_width":    592,

        "search_panel_height":   72,
        "search_container":      {"width": 418, "height": 58},
        "search_icon_lbl":        {"width": 29,  "height": 29},
        "clear_btn":              {"width": 29,  "height": 29},
        "clear_btn_icon":         {"width": 29,  "height": 29},
        "add_city_btn":           {"width": 160, "height": 54},

        "weather_card_max":   {"width": 528, "height": 140},
        "weather_card_choice_icon": {"width": 32, "height": 32},

        "hourly_forecast_height": 212,
        "hourly_line_height":     1,
        "hourly_arrow":           {"width": 32, "height": 54},
        "hourly_arrow_icon":      {"width": 26, "height": 26},
        "hourly_item_min_width":  144,

        "graph_line_height": 1,

        "city_info_left_max":     {"width": 624, "height": 409},
        "city_info_location_icon": {"width": 32, "height": 32},
        "city_info_separator_height": 1,
        "city_info_icon_lbl":     {"width": 240, "height": 95},
        "city_info_right_max":    {"width": 624, "height": 409},
        "city_info_right_separator_height": 1,
        "clock_widget":           {"width": 256, "height": 256},

        "confirm_button":     {"width": 168, "height": 51},
        "city_frame":         {"width": 870, "height": 216},
        "delete_btn":         {"width": 38,  "height": 38},

        "size_save_button":   {"width": 168, "height": 51},

        "settings_window":        {"width": 1264, "height": 929},
        "settings_min_height":    47,
        "settings_min_width":     224,
        "settings_top_bar_min_h": 81,
        "settings_close_btn":     {"width": 51, "height": 51},
        "settings_left_frame_min_w": 304,

        "lang_form_frame_width": 382,
        "lang_combo":            {"width": 382, "height": 43},
        "lang_confirm_button":   {"width": 168, "height": 51},

        "title_bar_height": 35,
    },
}


class SizeManager:
    """Глобальний менеджер розмірів додатку (за зразком LanguageManager)."""

    _current_size_key = "1200x800"

    @classmethod
    def set_size(cls, size_key: str):
        """Встановлює активний пресет розміру та надсилає сигнал зміни."""
        if size_key in SIZES and size_key != cls._current_size_key:
            cls._current_size_key = size_key
            window = SIZES[size_key]["window"]
            SIZE_SIGNAL.size_changed.emit(window["width"], window["height"])

    @classmethod
    def get_size_key(cls) -> str:
        return cls._current_size_key

    @classmethod
    def get(cls, name: str, key: str = None):
        """Повертає значення розміру за іменем для поточного пресету.

        Якщо key вказано — повертає values["width"|"height"|...],
        інакше повертає весь словник/число цілком.

        Приклад:
            SizeManager.get("weather_panel")            -> {"width":788,"height":157}
            SizeManager.get("weather_panel", "width")   -> 788
            SizeManager.get("left_panel_width")         -> 370
        """
        preset = SIZES.get(cls._current_size_key, SIZES["1200x800"])
        value = preset.get(name, SIZES["1200x800"].get(name))
        if key is not None and isinstance(value, dict):
            return value.get(key)
        return value

    @classmethod
    def get_window_size(cls) -> tuple[int, int]:
        window = SIZES[cls._current_size_key]["window"]
        return window["width"], window["height"]
