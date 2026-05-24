from datetime import datetime, timezone, timedelta
import json
import os
import requests

# Инициализация API ключа погоды из переменных окружения или значения по умолчанию
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    API_KEY = "7fb932921b9597af25d051ceecc43627"

# Путь к файлу со списком выбранных пользователем городов
USER_CITIES_PATH = os.path.join(os.path.dirname(__file__), "user_cities.json")

# Город по умолчанию при первом запуске приложения
DEFAULT_CITIES = ["Dnipro"]


def LOAD_USER_CITIES() -> list[str]:
    """Загружает список городов пользователя из JSON-файла.
    
    Если файл отсутствует, создает его со значениями по умолчанию.
    Автоматически конвертирует устаревший формат словаря в список.
    """
    if not os.path.exists(USER_CITIES_PATH):
        with open(USER_CITIES_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CITIES, f, ensure_ascii=False, indent=2)
        return DEFAULT_CITIES.copy()
    try:
        with open(USER_CITIES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = list(data.values())
            SAVE_USER_CITIES(data)
        return data
    except Exception:
        return DEFAULT_CITIES.copy()


def SAVE_USER_CITIES(cities: list[str]):
    """Сохраняет текущий список городов пользователя в JSON-файл.
    
    Args:
        cities: Список названий городов на английском языке.
    """
    try:
        with open(USER_CITIES_PATH, "w", encoding="utf-8") as f:
            json.dump(cities, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Помилка збереження міст: {e}")


def ADD_USER_CITY(city_en: str):
    """Добавляет новый город в список пользователя, если его там еще нет.
    
    Регистр букв при проверке дубликатов не учитывается.
    """
    cities = LOAD_USER_CITIES()
    if any(c.lower() == city_en.lower() for c in cities):
        return
    cities.append(city_en)
    SAVE_USER_CITIES(cities)


def REMOVE_USER_CITY(city_en: str):
    """Удаляет указанный город из списка пользователя.
    
    Регистр букв при поиске удаляемого города не учитывается.
    """
    cities = LOAD_USER_CITIES()
    cities = [c for c in cities if c.lower() != city_en.lower()]
    SAVE_USER_CITIES(cities)


def get_weather(city_en: str) -> dict | None:
    """Запрашивает прогноз погоды через OpenWeather API и формирует детальный отчет.
    
    Вычисляет местное время города, находит текущую погоду, минимальную/максимальную
    температуру на сегодня, а также строит почасовой прогноз, интегрируя в него
    время восхода и заката.
    
    Args:
        city_en: Название города на английском языке.
        
    Returns:
        Словарь с отформатированными данными погоды или None в случае ошибки.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_en}&appid={API_KEY}&units=metric&lang=uk"
        data = requests.get(url, timeout=10).json()

        if data.get("cod") != "200":
            print(f"Помилка API [{city_en}]: {data.get('message')}")
            return None

        # Определение часового пояса города для корректного отображения времени
        tz_offset = data["city"]["timezone"]
        tz = timezone(timedelta(seconds=tz_offset))
        server_now = datetime.now(tz)

        # Поиск ближайшего временного слота к текущему моменту
        current_slot = min(data["list"], key=lambda x: abs(x["dt"] - server_now.timestamp()))

        # Парсинг времени восхода и заката
        sunset_dt  = datetime.fromtimestamp(data["city"]["sunset"],  tz=tz)
        sunrise_dt = datetime.fromtimestamp(data["city"]["sunrise"], tz=tz)
        sunset_time  = sunset_dt.strftime("%H:%M")
        sunrise_time = sunrise_dt.strftime("%H:%M")

        # Расчет температурного максимума и минимума на текущие сутки
        today_slots = [
            item for item in data["list"]
            if datetime.fromtimestamp(item["dt"], tz).date() == server_now.date()
        ]
        temp_max = max(round(s["main"]["temp"]) for s in today_slots) if today_slots else 0
        temp_min = min(round(s["main"]["temp"]) for s in today_slots) if today_slots else 0

        # Формирование базового почасового прогноза на ближайшие 12 точек
        today_hours = []
        for slot in data["list"]:
            dt = datetime.fromtimestamp(slot["dt"], tz=tz)
            if dt >= server_now and len(today_hours) < 12:
                today_hours.append({
                    "time": dt.strftime("%H:%M"),
                    "icon": slot["weather"][0]["icon"],
                    "temp": round(slot["main"]["temp"]),
                    "pop": round(slot.get("pop", 0) * 100),
                    "is_sunset": False, "is_sunrise": False, "is_current": False,
                })

        # Вставка событий заката и восхода в хронологическом порядке в почасовой список
        for evt_dt, evt_time, icon, flag in [
            (sunset_dt,  sunset_time,  "sunset",  "is_sunset"),
            (sunrise_dt, sunrise_time, "sunrise", "is_sunrise"),
        ]:
            inserted = False
            for i in range(len(today_hours) - 1):
                t0 = datetime.strptime(today_hours[i]["time"],   "%H:%M").replace(year=server_now.year, month=server_now.month, day=server_now.day, tzinfo=tz)
                t1 = datetime.strptime(today_hours[i+1]["time"], "%H:%M").replace(year=server_now.year, month=server_now.month, day=server_now.day, tzinfo=tz)
                if t0.hour <= evt_dt.hour < t1.hour:
                    today_hours.insert(i + 1, {
                        "time": evt_time, "icon": icon, "temp": None, "pop": 0,
                        "is_sunset": flag == "is_sunset", "is_sunrise": flag == "is_sunrise", "is_current": False,
                    })
                    inserted = True
                    break
            if not inserted and evt_dt.date() == server_now.date() and evt_dt >= server_now:
                today_hours.append({
                    "time": evt_time, "icon": icon, "temp": None, "pop": 0,
                    "is_sunset": flag == "is_sunset", "is_sunrise": flag == "is_sunrise", "is_current": False,
                })

        # Создание чистого 12-часового прогноза без врезок заката/восхода
        next_12h = []
        for slot in data["list"]:
            if len(next_12h) >= 12:
                break
            dt = datetime.fromtimestamp(slot["dt"], tz=tz)
            if dt >= server_now:
                next_12h.append({
                    "time": dt.strftime("%H:%M"),
                    "icon": slot["weather"][0]["icon"],
                    "temp": round(slot["main"]["temp"]),
                    "pop": round(slot.get("pop", 0) * 100),
                })
        return {
            "city": city_en,
            "time": server_now.strftime("%H:%M"),
            "temp": str(round(current_slot["main"]["temp"])),
            "desc": current_slot["weather"][0]["description"].capitalize(),
            "minmax": f"Макс.:{temp_max}°, мін.:{temp_min}°",
            "icon": current_slot["weather"][0]["icon"],
            "is_current": False,
            "sunset":  sunset_time,
            "sunrise": sunrise_time,
            "today_hours": today_hours,
            "next_12h": next_12h,
        }

    except Exception as e:
        print(f"Критична помилка [{city_en}]: {e}")
        return None


def LOAD_CITIES_TO_JSON(path="cities.json"):
    """Скачивает полный список городов мира через стороннее API и сохраняет его в JSON.
    
    Используется для первоначального сбора базы городов для автокомплита.
    """
    url = "https://countriesnow.space/api/v0.1/countries"
    response = requests.get(url)
    data = response.json()

    cities = []
    for country in data["data"]:
        for city in country["cities"]:
            cities.append(city)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(cities, f, ensure_ascii=False, indent=2)

    return cities


def LOAD_CITIES_FROM_JSON(path="cities.json"):
    """Загружает локальный список всех городов из файла cities.json."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def SEARCH_CITIES(query: str, path="cities.json") -> list:
    """Ищет города в локальной базе по начальным буквам (на префикс).
    
    Поддерживает обработку как плоских списков строк, так и списков со словарями.
    Возвращает не более 6 наиболее подходящих результатов.
    
    Args:
        query: Строка поиска, введенная пользователем.
        path: Путь к файлу глобальной базы городов.
    """
    q = query.lower().strip()
    print(f"[DEBUG] SEARCH_CITIES: query={query!r}, normalized={q!r}, path={path}")
    if not q:
        print("[DEBUG] SEARCH_CITIES: empty query after normalization")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            cities = json.load(f)
    except Exception:
        return []

    found = []
    for city in cities:
        if isinstance(city, str):
            if city.lower().startswith(q):
                found.append({"en": city})
        elif isinstance(city, dict):
            en = city.get("en") or city.get("name") or ""
            if en.lower().startswith(q):
                found.append({"en": en})

    return found[:6]


def FORMAT_CITY(city: dict) -> str:
    """Извлекает строковое название города на английском из словаря результатов поиска."""
    return city.get("en", "")
