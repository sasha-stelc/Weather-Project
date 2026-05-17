import requests
from datetime import datetime, timezone, timedelta
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    API_KEY = "7fb932921b9597af25d051ceecc43627"


CITY_MAP = {
    "Дніпро": "Dnipro",
    "Київ": "Kyiv",
    "нью-йорк": "New York",
    "Лондон": "London",
    "Париж": "Paris",
}


def get_weather(city_ua: str) -> dict | None:
    city_en = CITY_MAP.get(city_ua, city_ua)
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_en}&appid={API_KEY}&units=metric&lang=uk"
        data = requests.get(url, timeout=10).json()

        if data.get("cod") != "200":
            print(f"Помилка API [{city_ua}]: {data.get('message')}")
            return None

        tz_offset = data["city"]["timezone"]
        tz = timezone(timedelta(seconds=tz_offset))

        server_now = datetime.now(tz)

        current_slot = min(data["list"], key=lambda x: abs(x["dt"] - server_now.timestamp()))
        
        # Захід та схід сонця
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

        # ====================== TODAY HOURS ======================
        today_hours = []
        for slot in data["list"]:
            dt = datetime.fromtimestamp(slot["dt"], tz=tz)
            if dt >= server_now and len(today_hours) < 12:
                today_hours.append({
                    "time": dt.strftime("%H:%M"),
                    "icon": slot["weather"][0]["icon"],
                    "temp": round(slot["main"]["temp"]),
                    "pop": round(slot.get("pop", 0) * 100),
                    "is_sunset": False,
                    "is_sunrise": False,
                    "is_current": False,
                })

        # Вставка заходу сонця
        inserted = False
        for i in range(len(today_hours) - 1):
            curr = datetime.strptime(today_hours[i]["time"], "%H:%M").replace(
                year=server_now.year, month=server_now.month, day=server_now.day, tzinfo=tz)
            nxt = datetime.strptime(today_hours[i+1]["time"], "%H:%M").replace(
                year=server_now.year, month=server_now.month, day=server_now.day, tzinfo=tz)

            if curr.hour <= sunset_dt.hour < nxt.hour:
                today_hours.insert(i + 1, {
                    "time": sunset_time,
                    "icon": "sunset",
                    "temp": None,
                    "pop": 0,
                    "is_sunset": True,
                    "is_sunrise": False,
                    "is_current": False,
                })
                inserted = True
                break

        if not inserted and sunset_dt.date() == server_now.date() and sunset_dt >= server_now:
            today_hours.append({
                "time": sunset_time,
                "icon": "sunset",
                "temp": None,
                "pop": 0,
                "is_sunset": True,
                "is_sunrise": False,
                "is_current": False,
            })

        # Вставка сходу сонця
        inserted_sunrise = False
        for i in range(len(today_hours) - 1):
            curr = datetime.strptime(today_hours[i]["time"], "%H:%M").replace(
                year=server_now.year, month=server_now.month, day=server_now.day, tzinfo=tz)
            nxt = datetime.strptime(today_hours[i+1]["time"], "%H:%M").replace(
                year=server_now.year, month=server_now.month, day=server_now.day, tzinfo=tz)

            if curr.hour <= sunrise_dt.hour < nxt.hour:
                today_hours.insert(i + 1, {
                    "time": sunrise_time,
                    "icon": "sunrise",
                    "temp": None,
                    "pop": 0,
                    "is_sunset": False,
                    "is_sunrise": True,
                    "is_current": False,
                })
                inserted_sunrise = True
                break

        if not inserted_sunrise and sunrise_dt.date() == server_now.date() and sunrise_dt >= server_now:
            today_hours.append({
                "time": sunrise_time,
                "icon": "sunrise",
                "temp": None,
                "pop": 0,
                "is_sunset": False,
                "is_sunrise": True,
                "is_current": False,
            })

        # Next 12h
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
            "city": city_ua,
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
        print(f"Критична помилка [{city_ua}]: {e}")
        return None
import requests
import json


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
import requests
import json


def SEARCH_CITIES(query: str, path="cities.json") -> list:
    q = query.lower().strip()
    if not q:
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
    return city.get("en", "")