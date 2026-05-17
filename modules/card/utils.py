import os
from ..create_path import create_media_path


def get_weather_icon_path(icon_code: str) -> str:
    """Получить путь до иконки погоды из папки weather icon Bl WI"""
    SPECIAL = {"sunrise", "sunset", "sun2"}

    if icon_code in SPECIAL:
        filename = f"{icon_code}.png"
    else:
        # Ожидаемый формат файлов: '001.d.png', '002.n.png' и т.д.
        # OpenWeather возвращает коды вида '01d' или '01n'.
        try:
            code = (icon_code or "").strip()
            if len(code) >= 3:
                num = int(code[:2])
                suffix = code[2]
                filename = f"{num:03d}.{suffix}.png"
            else:
                # fallback — просто положим как есть с префиксом 0
                filename = f"0{code}.png"
        except Exception:
            filename = f"0{icon_code}.png"

    return create_media_path(os.path.join("weather icon Bl WI", filename))
