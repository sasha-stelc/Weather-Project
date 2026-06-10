from datetime import datetime, timezone, timedelta
import json
import os
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    API_KEY = "7fb932921b9597af25d051ceecc43627"

USER_CITIES_PATH    = os.path.join(os.path.dirname(__file__), "user_cities.json")
COUNTRIES_DATA_PATH = os.path.join(os.path.dirname(__file__), "countries+states+cities.json")
CITIES_DATA_PATH    = os.path.join(os.path.dirname(__file__), "cities.json")   # новий плаский файл міст

DEFAULT_CITIES = ["Dnipro"]

# ───────────────────────────── КЕШ ─────────────────────────────
_COUNTRIES_CACHE      = None   # [ { name, iso2, states:[{cities:[]}] } ]
_CITIES_FLAT_CACHE    = None   # [ { en, country, latitude, longitude, timezone } ]
_COUNTRY_SEARCH_INDEX = None   # [ (term_lower, {name, iso2}) ]
_CITY_SEARCH_INDEX    = None   # [ (term_lower, city_entry) ]


# ────────────────────────── ПОБУДОВА ІНДЕКСІВ ──────────────────────────

def _build_country_search_index():
    """Індекс країн: name + native + усі translations."""
    global _COUNTRY_SEARCH_INDEX
    _COUNTRY_SEARCH_INDEX = []
    for country in _COUNTRIES_CACHE:
        name_en = country.get("name", "")
        iso2    = country.get("iso2", "")
        if not name_en:
            continue
        entry   = {"name": name_en, "iso2": iso2}
        added   = set()

        candidates = [name_en, country.get("native", "")]
        candidates += list(country.get("translations", {}).values())

        for term in candidates:
            if not term:
                continue
            key = term.lower().strip()
            if key and key not in added:
                added.add(key)
                _COUNTRY_SEARCH_INDEX.append((key, entry))


def _build_city_search_index():
    """Індекс міст: name + native + усі translations.

    Підтримує обидва формати:
      • Новий плаский  — { name, native, translations, country_name, … }
      • Старий вкладений — вже розгорнутий у _CITIES_FLAT_CACHE як { en, country, … }
    """
    global _CITY_SEARCH_INDEX
    _CITY_SEARCH_INDEX = []

    for city in _CITIES_FLAT_CACHE:
        entry = city   # посилання на той самий словник

        added = set()
        candidates = [
            city.get("en", ""),
            city.get("native", ""),
        ]
        candidates += list(city.get("translations", {}).values())

        for term in candidates:
            if not term:
                continue
            key = term.lower().strip()
            if key and key not in added:
                added.add(key)
                _CITY_SEARCH_INDEX.append((key, entry))


# ────────────────────────── ЗАВАНТАЖЕННЯ КЕШУ ──────────────────────────

def _load_flat_cities():
    """Завантажує новий плаский cities.json у _CITIES_FLAT_CACHE.

    Кожен запис перетворюється у внутрішній формат:
      en, native, translations, country, latitude, longitude, timezone
    """
    global _CITIES_FLAT_CACHE
    with open(CITIES_DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    _CITIES_FLAT_CACHE = []
    for city in raw:
        _CITIES_FLAT_CACHE.append({
            "en":           city.get("name", ""),
            "native":       city.get("native", ""),
            "translations": city.get("translations", {}),
            "country":      city.get("country_name", ""),
            "country_code": city.get("country_code", ""),
            "state":        city.get("state_name", ""),
            "latitude":     city.get("latitude"),
            "longitude":    city.get("longitude"),
            "timezone":     city.get("timezone"),
        })


def _load_nested_cities():
    """Розгортає старий countries+states+cities.json у плаский список."""
    global _CITIES_FLAT_CACHE
    _CITIES_FLAT_CACHE = []
    for country in _COUNTRIES_CACHE:
        country_name = country.get("name", "")
        for state in country.get("states", []):
            for city in state.get("cities", []):
                _CITIES_FLAT_CACHE.append({
                    "en":           city.get("name", ""),
                    "native":       "",
                    "translations": {},
                    "country":      country_name,
                    "country_code": country.get("iso2", ""),
                    "state":        state.get("name", ""),
                    "latitude":     city.get("latitude"),
                    "longitude":    city.get("longitude"),
                    "timezone":     city.get("timezone"),
                })


def _LOAD_COUNTRIES_CITIES_CACHE():
    """Головна функція ініціалізації кешу.

    Пріоритет:
      1. Новий cities.json (плаский, з перекладами) — повна мультимовна підтримка.
      2. Старий countries+states+cities.json — лише англійські назви міст.
    Країни завжди беруться з countries+states+cities.json.
    """
    global _COUNTRIES_CACHE

    if _CITY_SEARCH_INDEX is not None:
        return   # вже ініціалізовано

    # ── Країни ──
    try:
        with open(COUNTRIES_DATA_PATH, "r", encoding="utf-8") as f:
            _COUNTRIES_CACHE = json.load(f)
        _build_country_search_index()
    except Exception as e:
        print(f"Помилка завантаження країн: {e}")
        _COUNTRIES_CACHE = []
        global _COUNTRY_SEARCH_INDEX
        _COUNTRY_SEARCH_INDEX = []

    # ── Міста ──
    if os.path.exists(CITIES_DATA_PATH):
        try:
            _load_flat_cities()
            print(f"[cache] Завантажено {len(_CITIES_FLAT_CACHE)} міст (новий формат)")
        except Exception as e:
            print(f"Помилка завантаження cities.json: {e}")
            _load_nested_cities()
    else:
        print("[cache] cities.json не знайдено, використовується вкладений формат")
        _load_nested_cities()

    _build_city_search_index()
    print(f"[cache] Індекс міст: {len(_CITY_SEARCH_INDEX)} термінів")


# ────────────────────────── ПОШУК КРАЇН ──────────────────────────

def SEARCH_COUNTRIES(query: str) -> list:
    """Шукає країни за префіксом на будь-якій мові (name / native / translations).

    Повертає унікальні результати, не більше 8.
    """
    _LOAD_COUNTRIES_CITIES_CACHE()
    q = query.lower().strip()
    if not q or not _COUNTRY_SEARCH_INDEX:
        return []

    results    = []
    seen_names = set()

    for term_lower, entry in _COUNTRY_SEARCH_INDEX:
        if term_lower.startswith(q) and entry["name"] not in seen_names:
            seen_names.add(entry["name"])
            results.append(entry)
            if len(results) >= 8:
                break

    return results


# ────────────────────────── ПОШУК МІСТ ──────────────────────────

def SEARCH_CITIES(query: str, path=None) -> list:
    """Шукає міста на будь-якій мові через _CITY_SEARCH_INDEX.

    Стратегія:
      1. startswith  — точний збіг початку (вищий пріоритет)
      2. contains    — входження рядка (для запитів > 2 символів)

    Дедублікація по (en, country).
    """
    _LOAD_COUNTRIES_CITIES_CACHE()
    q = query.lower().strip()
    if not q or not _CITY_SEARCH_INDEX:
        return []

    starts   = []
    contains = []
    seen     = set()

    for term_lower, city in _CITY_SEARCH_INDEX:
        dedup = (city["en"].lower(), city["country"].lower())
        if dedup in seen:
            continue

        if term_lower.startswith(q):
            seen.add(dedup)
            starts.append(city)
        elif len(q) > 2 and q in term_lower:
            seen.add(dedup)
            contains.append(city)

        if len(starts) >= 6:
            break

    combined = starts + contains
    return combined[:6]


def GET_CITIES_BY_COUNTRY(country_name: str) -> list:
    """Повертає всі міста країни з плаского кешу."""
    _LOAD_COUNTRIES_CITIES_CACHE()
    if not _CITIES_FLAT_CACHE:
        return []
    target = country_name.lower()
    return [c for c in _CITIES_FLAT_CACHE if c["country"].lower() == target]


def FORMAT_CITY(city: dict) -> str:
    """Форматує місто для відображення: "Kyiv, Ukraine"."""
    name    = city.get("en", "")
    country = city.get("country", "")
    return f"{name}, {country}" if country else name


# ────────────────────────── USER CITIES ──────────────────────────

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


# ────────────────────────── WEATHER ──────────────────────────

def get_weather(city_en: str) -> dict | None:
    try:
        url  = (f"https://api.openweathermap.org/data/2.5/forecast"
                f"?q={city_en}&appid={API_KEY}&units=metric&lang=uk")
        data = requests.get(url, timeout=10).json()

        if data.get("cod") != "200":
            print(f"Помилка API [{city_en}]: {data.get('message')}")
            return None

        tz_offset  = data["city"]["timezone"]
        tz         = timezone(timedelta(seconds=tz_offset))
        server_now = datetime.now(tz)

        current_slot = min(
            data["list"],
            key=lambda x: abs(x["dt"] - server_now.timestamp()),
        )

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
                    "pop":  round(slot.get("pop", 0) * 100),
                    "is_sunset": False, "is_sunrise": False, "is_current": False,
                })

        for evt_dt, evt_time, icon, flag in [
            (sunset_dt,  sunset_time,  "sunset",  "is_sunset"),
            (sunrise_dt, sunrise_time, "sunrise", "is_sunrise"),
        ]:
            inserted = False
            for i in range(len(today_hours) - 1):
                t0 = datetime.strptime(today_hours[i]["time"],   "%H:%M").replace(
                    year=server_now.year, month=server_now.month,
                    day=server_now.day, tzinfo=tz)
                t1 = datetime.strptime(today_hours[i+1]["time"], "%H:%M").replace(
                    year=server_now.year, month=server_now.month,
                    day=server_now.day, tzinfo=tz)
                if t0.hour <= evt_dt.hour < t1.hour:
                    today_hours.insert(i + 1, {
                        "time": evt_time, "icon": icon, "temp": None, "pop": 0,
                        "is_sunset":  flag == "is_sunset",
                        "is_sunrise": flag == "is_sunrise",
                        "is_current": False,
                    })
                    inserted = True
                    break
            if not inserted and evt_dt.date() == server_now.date() and evt_dt >= server_now:
                today_hours.append({
                    "time": evt_time, "icon": icon, "temp": None, "pop": 0,
                    "is_sunset":  flag == "is_sunset",
                    "is_sunrise": flag == "is_sunrise",
                    "is_current": False,
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
                    "pop":  round(slot.get("pop", 0) * 100),
                })

        return {
            "city":        city_en,
            "lat":         data["city"]["coord"]["lat"],   # ← добавить
            "lon":         data["city"]["coord"]["lon"],   # ← добавить
            "time":        server_now.strftime("%H:%M"),
            "temp":        str(round(current_slot["main"]["temp"])),
            "desc":        current_slot["weather"][0]["description"].capitalize(),
            "minmax":      f"Макс.:{temp_max}°, мін.:{temp_min}°",
            "icon":        current_slot["weather"][0]["icon"],
            "is_current":  False,
            "sunset":      sunset_time,
            "sunrise":     sunrise_time,
            "today_hours": today_hours,
            "next_12h":    next_12h,
        }

    except Exception as e:
        print(f"Критична помилка [{city_en}]: {e}")
        return None


# ────────────────────────── LEGACY ──────────────────────────

def LOAD_CITIES_TO_JSON(path="cities_old.json"):
    url  = "https://countriesnow.space/api/v0.1/countries"
    data = requests.get(url).json()
    cities = [city for country in data["data"] for city in country["cities"]]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cities, f, ensure_ascii=False, indent=2)
    return cities


def LOAD_CITIES_FROM_JSON(path="cities_old.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)