from datetime import datetime, timezone, timedelta
import json
import os
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    API_KEY = "7fb932921b9597af25d051ceecc43627"

USER_CITIES_PATH = os.path.join(os.path.dirname(__file__), "user_cities.json")
COUNTRIES_DATA_PATH = os.path.join(os.path.dirname(__file__), "countries+states+cities.json")
DEFAULT_CITIES = ["Dnipro"]

# ===== КЕШ =====
_COUNTRIES_CACHE = None       # Сирий список країн з JSON
_CITIES_FLAT_CACHE = None     # Плаский список усіх міст
_COUNTRY_SEARCH_INDEX = None  # Індекс: (term_lower, {name, iso2}) для мультимовного пошуку


def _build_country_search_index():
    """Будує індекс пошуку по країнах з усіх мовних варіантів назви.

    Для кожної країни збирає: англійська name, native та всі значення translations.
    Зберігає список (пошуковий_термін_lower, {name, iso2}) — дубліки одного
    запису відкидаються, але різні мови однієї країни додаються окремо.
    """
    global _COUNTRY_SEARCH_INDEX
    _COUNTRY_SEARCH_INDEX = []
    seen_per_country = {}  # name_en → set of already-added terms

    for country in _COUNTRIES_CACHE:
        name_en = country.get("name", "")
        iso2    = country.get("iso2", "")
        if not name_en:
            continue

        added = seen_per_country.setdefault(name_en, set())
        entry = {"name": name_en, "iso2": iso2}

        candidates = [name_en, country.get("native", "")]
        candidates += list(country.get("translations", {}).values())

        for term in candidates:
            if not term:
                continue
            key = term.lower().strip()
            if key and key not in added:
                added.add(key)
                _COUNTRY_SEARCH_INDEX.append((key, entry))


def _LOAD_COUNTRIES_CITIES_CACHE():
    """Завантажує JSON у пам'ять та будує плаский список міст і пошуковий індекс країн."""
    global _COUNTRIES_CACHE, _CITIES_FLAT_CACHE
    if _COUNTRIES_CACHE is not None:
        return
    try:
        with open(COUNTRIES_DATA_PATH, "r", encoding="utf-8") as f:
            _COUNTRIES_CACHE = json.load(f)

        _CITIES_FLAT_CACHE = []
        for country in _COUNTRIES_CACHE:
            country_name = country.get("name", "")
            for state in country.get("states", []):
                for city in state.get("cities", []):
                    city_name = city.get("name", "")
                    _CITIES_FLAT_CACHE.append({
                        "en":        city_name,
                        "search_key": city_name.lower(),   # JSON містить лише англ. назви міст
                        "country":   country_name,
                        "latitude":  city.get("latitude"),
                        "longitude": city.get("longitude"),
                        "timezone":  city.get("timezone"),
                    })

        _build_country_search_index()

    except Exception as e:
        print(f"Помилка завантаження кешу: {e}")
        _COUNTRIES_CACHE   = []
        _CITIES_FLAT_CACHE = []
        _COUNTRY_SEARCH_INDEX = []


# ===== ПОШУК КРАЇН =====

def SEARCH_COUNTRIES(query: str) -> list:
    """Шукає країни за префіксом на будь-якій мові.

    Перевіряє name (англ.), native та всі ~20 перекладів translations.
    Повертає унікальні результати (по name_en), не більше 8.

    Приклади:
        "ukr"  → Ukraine  (англ.)
        "укра" → Ukraine  (uk-переклад: "Україна")
        "ucrâ" → Ukraine  (pt-BR: "Ucrânia")
        "deut" → Germany  (нім. native: "Deutschland")
    """
    _LOAD_COUNTRIES_CITIES_CACHE()
    q = query.lower().strip()
    if not q or not _COUNTRY_SEARCH_INDEX:
        return []

    results = []
    seen_names = set()

    for term_lower, entry in _COUNTRY_SEARCH_INDEX:
        if term_lower.startswith(q) and entry["name"] not in seen_names:
            seen_names.add(entry["name"])
            results.append(entry)
            if len(results) >= 8:
                break

    return results


# ===== ПОШУК МІСТ =====

def SEARCH_CITIES(query: str, path=None) -> list:
    """Шукає міста за введеним рядком.

    Стратегія (у порядку пріоритету):
      1. Startswith — точний збіг початку назви (Kyiv → "Ky...")
      2. Contains   — рядок де-небудь у назві (for > 2 символів)

    Примітка: JSON містить лише англійські назви міст; мультимовний
    пошук міст неможливий без додаткових даних.

    Args:
        query: Рядок пошуку.
        path:  Не використовується, залишено для сумісності.
    """
    _LOAD_COUNTRIES_CITIES_CACHE()
    q = query.lower().strip()
    if not q or not _CITIES_FLAT_CACHE:
        return []

    starts   = []
    contains = []

    for city in _CITIES_FLAT_CACHE:
        key = city["search_key"]
        if key.startswith(q):
            starts.append(city)
        elif len(q) > 2 and q in key:
            contains.append(city)

    combined = starts + contains
    # Прибираємо дублікати (однакова назва + країна)
    seen = set()
    unique = []
    for c in combined:
        dedup_key = (c["en"].lower(), c["country"].lower())
        if dedup_key not in seen:
            seen.add(dedup_key)
            unique.append(c)
        if len(unique) >= 6:
            break

    return unique


def GET_CITIES_BY_COUNTRY(country_name: str) -> list:
    """Повертає всі міста країни (пошук по англійській назві країни)."""
    _LOAD_COUNTRIES_CITIES_CACHE()
    if not _COUNTRIES_CACHE:
        return []
    target = country_name.lower()
    for country in _COUNTRIES_CACHE:
        if country.get("name", "").lower() == target:
            cities = []
            for state in country.get("states", []):
                for city in state.get("cities", []):
                    cities.append({
                        "en":        city.get("name", ""),
                        "latitude":  city.get("latitude"),
                        "longitude": city.get("longitude"),
                        "timezone":  city.get("timezone"),
                    })
            return cities
    return []


def FORMAT_CITY(city: dict) -> str:
    """Форматує місто для відображення у списку: "Kyiv, Ukraine"."""
    name    = city.get("en", "")
    country = city.get("country", "")
    return f"{name}, {country}" if country else name


# ===== USER CITIES =====

def LOAD_USER_CITIES() -> list[str]:
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
    try:
        with open(USER_CITIES_PATH, "w", encoding="utf-8") as f:
            json.dump(cities, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Помилка збереження міст: {e}")


def ADD_USER_CITY(city_en: str):
    cities = LOAD_USER_CITIES()
    if any(c.lower() == city_en.lower() for c in cities):
        return
    cities.append(city_en)
    SAVE_USER_CITIES(cities)


def REMOVE_USER_CITY(city_en: str):
    cities = LOAD_USER_CITIES()
    cities = [c for c in cities if c.lower() != city_en.lower()]
    SAVE_USER_CITIES(cities)


# ===== WEATHER =====

def get_weather(city_en: str) -> dict | None:
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_en}&appid={API_KEY}&units=metric&lang=uk"
        data = requests.get(url, timeout=10).json()

        if data.get("cod") != "200":
            print(f"Помилка API [{city_en}]: {data.get('message')}")
            return None

        tz_offset = data["city"]["timezone"]
        tz = timezone(timedelta(seconds=tz_offset))
        server_now = datetime.now(tz)

        current_slot = min(data["list"], key=lambda x: abs(x["dt"] - server_now.timestamp()))

        sunset_dt  = datetime.fromtimestamp(data["city"]["sunset"],  tz=tz)
        sunrise_dt = datetime.fromtimestamp(data["city"]["sunrise"], tz=tz)
        sunset_time  = sunset_dt.strftime("%H:%M")
        sunrise_time = sunrise_dt.strftime("%H:%M")

        today_slots = [
            item for item in data["list"]
            if datetime.fromtimestamp(item["dt"], tz).date() == server_now.date()
        ]
        temp_max = max(round(s["main"]["temp"]) for s in today_slots) if today_slots else 0
        temp_min = min(round(s["main"]["temp"]) for s in today_slots) if today_slots else 0

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
            "city_display": data["city"]["name"],
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
            "latitude": data["city"]["coord"]["lat"],
            "longitude": data["city"]["coord"]["lon"],
            "lat": data["city"]["coord"]["lat"],
            "lon": data["city"]["coord"]["lon"],
        }

    except Exception as e:
        print(f"Критична помилка [{city_en}]: {e}")
        return None


# ===== LEGACY =====

def LOAD_CITIES_TO_JSON(path="cities.json"):
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
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)