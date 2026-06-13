from datetime import datetime, timezone, timedelta
import json
import os
import requests

from modules.settings.langueges import LanguageManager

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    API_KEY = "7fb932921b9597af25d051ceecc43627"

USER_CITIES_PATH    = os.path.join(os.path.dirname(__file__), "user_cities.json")
COUNTRIES_DATA_PATH = os.path.join(os.path.dirname(__file__), "countries+states+cities.json")
CITIES_DATA_PATH    = os.path.join(os.path.dirname(__file__), "cities.json")
WEATHER_CACHE_PATH  = os.path.join(os.path.dirname(__file__), "weather_cache.json")

# Формат user_cities.json:
# [{"en": "Dnipro", "display": "Дніпро", "country": "Ukraine"}, ...]
DEFAULT_CITIES = [{"en": "Dnipro", "display": "Dnipro", "country": "Ukraine"}]

ALL_LANGUAGES      = ["uk", "ru", "en", "no"]
CACHE_TTL_SECONDS  = 5 * 60  # 5 хвилин

# ───────────────────────────── КЕШ ГЕОДАНИХ ─────────────────────────────
_COUNTRIES_CACHE      = None
_CITIES_FLAT_CACHE    = None
_COUNTRY_SEARCH_INDEX = None   # [(term_lower, {name, iso2, display_name})]
_CITY_SEARCH_INDEX    = None   # [(term_lower, matched_display, city_entry)]

# ───────────────────────────── КЕШ ПОГОДИ ─────────────────────────────
_weather_cache: dict = {}      # дзеркало JSON-файлу в пам'яті

# Відповідність англійських описів OpenWeather → ключі локалізації
_WEATHER_DESC_TO_KEY: dict[str, str] = {
    "clear sky":                     "WEATHER_CLEAR_SKY",
    "few clouds":                    "WEATHER_FEW_CLOUDS",
    "scattered clouds":              "WEATHER_SCATTERED_CLOUDS",
    "broken clouds":                 "WEATHER_BROKEN_CLOUDS",
    "overcast clouds":               "WEATHER_OVERCAST_CLOUDS",
    "mist":                          "WEATHER_MIST",
    "fog":                           "WEATHER_FOG",
    "haze":                          "WEATHER_HAZE",
    "smoke":                         "WEATHER_SMOKE",
    "light rain":                    "WEATHER_LIGHT_RAIN",
    "moderate rain":                 "WEATHER_MODERATE_RAIN",
    "heavy intensity rain":          "WEATHER_HEAVY_INTENSITY_RAIN",
    "very heavy rain":               "WEATHER_VERY_HEAVY_RAIN",
    "extreme rain":                  "WEATHER_EXTREME_RAIN",
    "freezing rain":                 "WEATHER_FREEZING_RAIN",
    "shower rain":                   "WEATHER_SHOWER_RAIN",
    "light shower rain":             "WEATHER_SHOWER_RAIN",
    "heavy intensity shower rain":   "WEATHER_SHOWER_RAIN",
    "ragged shower rain":            "WEATHER_SHOWER_RAIN",
    "thunderstorm":                  "WEATHER_THUNDERSTORM",
    "thunderstorm with light rain":  "WEATHER_THUNDERSTORM_WITH_LIGHT_RAIN",
    "thunderstorm with rain":        "WEATHER_THUNDERSTORM_WITH_RAIN",
    "thunderstorm with heavy rain":  "WEATHER_THUNDERSTORM_WITH_RAIN",
    "light snow":                    "WEATHER_LIGHT_SNOW",
    "snow":                          "WEATHER_SNOW",
    "heavy snow":                    "WEATHER_HEAVY_SNOW",
    "sleet":                         "WEATHER_SLEET",
    "light shower sleet":            "WEATHER_SLEET",
    "shower sleet":                  "WEATHER_SLEET",
    "dust":                          "WEATHER_DUST",
    "sand":                          "WEATHER_SAND",
    "ash":                           "WEATHER_ASH",
    "squall":                        "WEATHER_SQUALL",
    "tornado":                       "WEATHER_TORNADO",
}

# Шаблони рядка min/max для кожної мови
_MINMAX_TEMPLATES: dict[str, str] = {
    "uk": "Макс.:{max}°, мін.:{min}°",
    "ru": "Макс.:{max}°, мин.:{min}°",
    "en": "Max: {max}°, min: {min}°",
    "no": "Maks: {max}°, min: {min}°",
}


# ────────────────────────── ПОБУДОВА ІНДЕКСІВ ──────────────────────────

def _build_country_search_index():
    global _COUNTRY_SEARCH_INDEX
    _COUNTRY_SEARCH_INDEX = []
    for country in _COUNTRIES_CACHE:
        name_en = country.get("name", "")
        iso2    = country.get("iso2", "")
        if not name_en:
            continue
        added = set()

        candidates = [(name_en, name_en)]
        native = country.get("native", "")
        if native:
            candidates.append((native, native))
        for translation in country.get("translations", {}).values():
            if translation:
                candidates.append((translation, translation))

        for term, display in candidates:
            key = term.lower().strip()
            if key and key not in added:
                added.add(key)
                _COUNTRY_SEARCH_INDEX.append((key, {
                    "name":         name_en,
                    "iso2":         iso2,
                    "display_name": display,
                }))


def _build_city_search_index():
    global _CITY_SEARCH_INDEX
    _CITY_SEARCH_INDEX = []

    for city in _CITIES_FLAT_CACHE:
        added = set()
        candidates = []
        en = city.get("en", "")
        if en:
            candidates.append((en, en))
        native = city.get("native", "")
        if native:
            candidates.append((native, native))
        for translation in city.get("translations", {}).values():
            if translation:
                candidates.append((translation, translation))

        for term, display in candidates:
            key = term.lower().strip()
            if key and key not in added:
                added.add(key)
                _CITY_SEARCH_INDEX.append((key, display, city))


# ────────────────────────── ЗАВАНТАЖЕННЯ КЕШу ГЕОДАНИХ ──────────────────────────

def _load_flat_cities():
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


def _normalize_city_record(city, display: str = "", country: str = "") -> dict | None:
    if isinstance(city, dict):
        city_en = city.get("en", "") or city.get("name", "")
        if not city_en:
            return None
        return {
            "en":      city_en.strip(),
            "display": (city.get("display") or city_en).strip(),
            "country": (city.get("country") or country or "").strip(),
        }

    if isinstance(city, str):
        city_en = city.strip()
        if not city_en:
            return None
        return {
            "en":      city_en,
            "display": (display or city_en).strip(),
            "country": country.strip(),
        }

    return None


def _LOAD_COUNTRIES_CITIES_CACHE():
    global _COUNTRIES_CACHE

    if _CITY_SEARCH_INDEX is not None:
        return

    try:
        with open(COUNTRIES_DATA_PATH, "r", encoding="utf-8") as f:
            _COUNTRIES_CACHE = json.load(f)
        _build_country_search_index()
    except Exception as e:
        print(f"Помилка завантаження країн: {e}")
        _COUNTRIES_CACHE = []
        global _COUNTRY_SEARCH_INDEX
        _COUNTRY_SEARCH_INDEX = []

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

def _get_country_display_map(q: str) -> dict:
    result = {}
    if not _COUNTRY_SEARCH_INDEX:
        return result
    for term_lower, c_entry in _COUNTRY_SEARCH_INDEX:
        if term_lower.startswith(q):
            key = c_entry["name"].lower()
            if key not in result:
                result[key] = c_entry["display_name"]
    return result


def SEARCH_CITIES(query: str, path=None) -> list:
    _LOAD_COUNTRIES_CITIES_CACHE()
    q = query.lower().strip()
    if not q or not _CITY_SEARCH_INDEX:
        return []

    country_display_map = _get_country_display_map(q)

    starts   = []
    contains = []
    seen     = set()

    for term_lower, matched_display, city in _CITY_SEARCH_INDEX:
        dedup = (city["en"].lower(), city["country"].lower())
        if dedup in seen:
            continue

        if term_lower.startswith(q):
            seen.add(dedup)
            starts.append(_enrich(city, matched_display, country_display_map))
        elif len(q) > 2 and q in term_lower:
            seen.add(dedup)
            contains.append(_enrich(city, matched_display, country_display_map))

        if len(starts) >= 6:
            break

    combined = starts + contains
    return combined[:6]


def _enrich(city: dict, matched_display: str, country_display_map: dict) -> dict:
    result = dict(city)
    result["display"] = matched_display
    country_key = city["country"].lower()
    result["display_country"] = country_display_map.get(country_key, city["country"])
    return result


def GET_CITIES_BY_COUNTRY(country_name: str) -> list:
    _LOAD_COUNTRIES_CITIES_CACHE()
    if not _CITIES_FLAT_CACHE:
        return []
    target = country_name.lower()
    return [c for c in _CITIES_FLAT_CACHE if c["country"].lower() == target]


def FORMAT_CITY(city: dict) -> str:
    name    = city.get("display") or city.get("en", "")
    country = city.get("display_country") or city.get("country", "")
    return f"{name}, {country}" if country else name


# ────────────────────────── USER CITIES ──────────────────────────

def _migrate_legacy(data) -> list:
    if not data:
        return []
    if isinstance(data, list) and data and isinstance(data[0], str):
        return [n for n in (_normalize_city_record(name) for name in data) if n]
    if isinstance(data, list) and data and isinstance(data[0], dict):
        return [n for n in (_normalize_city_record(city) for city in data) if n]
    if isinstance(data, dict):
        return [n for n in (_normalize_city_record(name) for name in data.values()) if n]
    return data


def LOAD_USER_CITIES() -> list[dict]:
    if not os.path.exists(USER_CITIES_PATH):
        SAVE_USER_CITIES(DEFAULT_CITIES)
        return DEFAULT_CITIES.copy()
    try:
        with open(USER_CITIES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        data = _migrate_legacy(data)
        return [city for city in data if isinstance(city, dict) and city.get("en")]
    except Exception:
        return DEFAULT_CITIES.copy()


def SAVE_USER_CITIES(cities: list[dict]):
    try:
        normalized = []
        for city in cities:
            normalized_city = _normalize_city_record(city)
            if normalized_city:
                normalized.append(normalized_city)
        with open(USER_CITIES_PATH, "w", encoding="utf-8") as f:
            json.dump(normalized, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Помилка збереження міст: {e}")


def ADD_USER_CITY(city, display: str = "", country: str = ""):
    cities = LOAD_USER_CITIES()
    normalized_city = _normalize_city_record(city, display=display, country=country)
    if not normalized_city:
        return
    if any(c.get("en", "").lower() == normalized_city["en"].lower() for c in cities):
        return
    cities.append(normalized_city)
    SAVE_USER_CITIES(cities)


def REMOVE_USER_CITY(city):
    cities = LOAD_USER_CITIES()
    city_en = GET_CITY_EN(city).strip().lower()
    if not city_en:
        return
    cities = [c for c in cities if c.get("en", "").lower() != city_en]
    SAVE_USER_CITIES(cities)


def GET_CITY_EN(city: "dict | str") -> str:
    if isinstance(city, dict):
        return city.get("en", "")
    return city


# ────────────────────────── КЕШ ПОГОДИ — допоміжні функції ──────────────────────────

def _load_weather_cache() -> dict:
    """Завантажує кеш погоди з файлу в пам'ять (один раз)."""
    global _weather_cache
    if _weather_cache:
        return _weather_cache
    if os.path.exists(WEATHER_CACHE_PATH):
        try:
            with open(WEATHER_CACHE_PATH, "r", encoding="utf-8") as f:
                _weather_cache = json.load(f)
            print(f"[weather_cache] Завантажено {len(_weather_cache)} міст")
        except Exception as e:
            print(f"[weather_cache] Помилка читання: {e}")
            _weather_cache = {}
    return _weather_cache


def _save_weather_cache():
    """Записує поточний стан кешу погоди на диск."""
    try:
        with open(WEATHER_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(_weather_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[weather_cache] Помилка запису: {e}")


def _get_city_names_all_langs(city_en: str) -> dict[str, str]:
    """Повертає назви міста на всіх 4 мовах зі словника перекладів.

    Формат результату: {"uk": "Дніпро", "ru": "Днепр", "en": "Dnipro", "no": "Dnipro"}
    Якщо переклад не знайдено — fallback на city_en.
    """
    _LOAD_COUNTRIES_CITIES_CACHE()
    names = {lang: city_en for lang in ALL_LANGUAGES}

    city_en_lower = city_en.lower()
    for _, _, city in _CITY_SEARCH_INDEX:
        if city.get("en", "").lower() != city_en_lower:
            continue

        names["en"] = city.get("en", city_en)
        translations = city.get("translations", {})

        for lang, codes in [
            ("uk", ["uk", "ukr"]),
            ("ru", ["ru", "rus"]),
            ("no", ["no", "nor", "nb"]),
        ]:
            for code in codes:
                val = translations.get(code, "").strip()
                if val:
                    names[lang] = val
                    break

        # Якщо native є і потрібної мови нема — не перезаписуємо, залишаємо city_en
        break

    return names


def _desc_to_translations(desc_en_raw: str) -> dict[str, str]:
    """Перекладає сирий опис OpenWeather API на всі 4 мови через ключ локалізації."""
    key = _WEATHER_DESC_TO_KEY.get(desc_en_raw.lower().strip(), "")
    result: dict[str, str] = {}
    for lang in ALL_LANGUAGES:
        if key:
            translated = LanguageManager.TRANSLATIONS.get(lang, {}).get(key, "")
            result[lang] = translated if translated else desc_en_raw.capitalize()
        else:
            result[lang] = desc_en_raw.capitalize()
    return result


def _format_minmax_all_langs(temp_max: int, temp_min: int) -> dict[str, str]:
    """Формує рядок min/max температури одразу для всіх 4 мов."""
    return {
        lang: _MINMAX_TEMPLATES[lang].format(max=temp_max, min=temp_min)
        for lang in ALL_LANGUAGES
    }


def _is_cache_fresh(entry: dict) -> bool:
    """Повертає True, якщо запис кешу молодший за CACHE_TTL_SECONDS."""
    cached_at = entry.get("cached_at", 0)
    age = datetime.now(timezone.utc).timestamp() - cached_at
    return age < CACHE_TTL_SECONDS


def _format_weather_for_lang(cached: dict, lang: str) -> dict:
    """Формує фінальний словник погоди для конкретної мови з кешованого запису."""
    return {
        "city":         cached["city_en"],
        "city_display": cached["city_names"].get(lang, cached["city_en"]),
        "city_names":   cached["city_names"],           # всі 4 мови — для довідки
        "lat":          cached["lat"],
        "lon":          cached["lon"],
        "time":         cached["time"],
        "temp":         cached["temp"],
        "desc":         cached["desc_i18n"].get(lang, cached["desc_raw"]),
        "desc_i18n":    cached["desc_i18n"],            # всі 4 мови
        "minmax":       cached["minmax_i18n"].get(lang, ""),
        "minmax_i18n":  cached["minmax_i18n"],          # всі 4 мови
        "icon":         cached["icon"],
        "is_current":   cached.get("is_current", False),
        "sunset":       cached["sunset"],
        "sunrise":      cached["sunrise"],
        "today_hours":  cached["today_hours"],
        "next_12h":     cached["next_12h"],
    }


def INVALIDATE_WEATHER_CACHE(city_en: str | None = None):
    """Примусово інвалідує кеш для конкретного міста або всього кешу."""
    global _weather_cache
    if city_en is None:
        _weather_cache = {}
    else:
        _weather_cache.pop(city_en.lower(), None)
    _save_weather_cache()


# ────────────────────────── WEATHER ──────────────────────────

def get_weather(city_en: str, lang: str | None = None) -> dict | None:
    """Повертає погодні дані для міста.

    Логіка кешування:
      • Якщо місто є в кеші і запис свіжіший за 5 хвилин → дані з кешу.
      • Інакше → запит до OpenWeather API (завжди lang=en для стабільного
        маппінгу описів), результат зберігається в кеш і повертається.

    Кеш зберігається у weather_cache.json поруч з api_request.py.
    Назви міст і текстові поля (опис, min/max) зберігаються на всіх 4 мовах.

    Args:
        city_en: канонічна назва міста англійською (для запиту до API).
        lang:    мова виводу; якщо None — береться з LanguageManager.
    """
    cur_lang = lang or LanguageManager.get_language()
    cache    = _load_weather_cache()
    cache_key = city_en.lower()

    # ── Перевірка кешу ──
    if cache_key in cache and _is_cache_fresh(cache[cache_key]):
        entry = cache[cache_key]
        age   = int(datetime.now(timezone.utc).timestamp() - entry["cached_at"])
        print(f"[weather_cache] {city_en}: з кешу (вік {age}с, TTL {CACHE_TTL_SECONDS}с)")
        return _format_weather_for_lang(entry, cur_lang)

    # ── Запит до API (завжди англійською) ──
    print(f"[weather_cache] {city_en}: запит до API")
    try:
        url  = (f"https://api.openweathermap.org/data/2.5/forecast"
                f"?q={city_en}&appid={API_KEY}&units=metric&lang=en")
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

        sunset_dt    = datetime.fromtimestamp(data["city"]["sunset"],  tz=tz)
        sunrise_dt   = datetime.fromtimestamp(data["city"]["sunrise"], tz=tz)
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
                    "time":       dt.strftime("%H:%M"),
                    "icon":       slot["weather"][0]["icon"],
                    "temp":       round(slot["main"]["temp"]),
                    "pop":        round(slot.get("pop", 0) * 100),
                    "is_sunset":  False,
                    "is_sunrise": False,
                    "is_current": False,
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
                        "time":       evt_time,
                        "icon":       icon,
                        "temp":       None,
                        "pop":        0,
                        "is_sunset":  flag == "is_sunset",
                        "is_sunrise": flag == "is_sunrise",
                        "is_current": False,
                    })
                    inserted = True
                    break
            if not inserted and evt_dt.date() == server_now.date() and evt_dt >= server_now:
                today_hours.append({
                    "time":       evt_time,
                    "icon":       icon,
                    "temp":       None,
                    "pop":        0,
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

        desc_raw = current_slot["weather"][0]["description"].lower().strip()

        # ── Формування запису для кешу ──
        cached_entry: dict = {
            "cached_at":   datetime.now(timezone.utc).timestamp(),
            "city_en":     city_en,
            "city_names":  _get_city_names_all_langs(city_en),  # {"uk":…, "ru":…, "en":…, "no":…}
            "lat":         data["city"]["coord"]["lat"],
            "lon":         data["city"]["coord"]["lon"],
            "time":        server_now.strftime("%H:%M"),
            "temp":        str(round(current_slot["main"]["temp"])),
            "desc_raw":    desc_raw,
            "desc_i18n":   _desc_to_translations(desc_raw),      # {"uk":…, "ru":…, "en":…, "no":…}
            "minmax_i18n": _format_minmax_all_langs(temp_max, temp_min),
            "icon":        current_slot["weather"][0]["icon"],
            "is_current":  False,
            "sunset":      sunset_time,
            "sunrise":     sunrise_time,
            "today_hours": today_hours,
            "next_12h":    next_12h,
        }

        cache[cache_key] = cached_entry
        _save_weather_cache()

        return _format_weather_for_lang(cached_entry, cur_lang)

    except Exception as e:
        print(f"Критична помилка [{city_en}]: {e}")
        return None