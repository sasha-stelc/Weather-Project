import requests
from datetime import datetime, timezone, timedelta

API_KEY = "7fb932921b9597af25d051ceecc43627"

CITY_MAP = {
    "Дніпро":    "Dnipro",
    "Київ":      "Kyiv",
    "Братіслава": "Bratislava",
    "Варшава":   "Warsaw",
    "Рим":       "Rome",
}

def get_weather(city_ua: str) -> dict | None:
    city_en = CITY_MAP.get(city_ua, city_ua)
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_en}&appid={API_KEY}&units=metric&lang=uk"
        data = requests.get(url, timeout=5).json()
        tz   = timezone(timedelta(seconds=data["timezone"]))
        time = datetime.fromtimestamp(data["dt"], tz=tz).strftime("%H:%M")
        
        return {
            "city":   city_ua,
            "time":   time,
            "temp":   str(round(data["main"]["temp"])),
            "desc":   data["weather"][0]["description"].capitalize(),
            "minmax": f"Макс.:{round(data['main']['temp_max'])}°, мін.:{round(data['main']['temp_min'])}°",
            "is_current": False,
        }
    except Exception as e:
        print(f"Ошибка [{city_ua}]: {e}")
        return None