from .weather_app import WeatherApp

# Створюємо глобальний екземпляр (як було раніше)
window = WeatherApp()

# Для зручності
MainWindow = window

__all__ = ["WeatherApp", "window", "MainWindow"]