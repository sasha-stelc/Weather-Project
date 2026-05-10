import requests
from datetime import datetime, timezone, timedelta

API_KEY = "7fb932921b9597af25d051ceecc43627"

CITY_MAP = {
    "Дніпро": "Dnipro",
    "Київ":   "Kyiv",
}

def get_weather(city_ua: str) -> dict | None:
    city_en = CITY_MAP.get(city_ua, city_ua)
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_en}&appid={API_KEY}&units=metric&lang=uk"
        data = requests.get(url).json()

        # UTC-зміщення в секундах — працює для будь-якого міста світу
        tz   = timezone(timedelta(seconds=data["timezone"]))
        time = datetime.now(tz).strftime("%H:%M")  # ← поточний час у часовому поясі міста
        print(f"иконка:{data['weather'][0]['icon']} описание:{data['weather'][0]['description'].capitalize()}")        
        return {
            "city":   city_ua,
            "time":   time,
            "temp":   str(round(data["main"]["temp"])),
            "desc":   data["weather"][0]["description"].capitalize(),
            "minmax": f"Макс.:{round(data['main']['temp_max'])}°, мін.:{round(data['main']['temp_min'])}°",
            "timezone": tz,
            "icon": data["weather"][0]["icon"],  # ← для картинки
            "is_current": False,

        }
    
    except Exception as e:
        print(f"Ошибка [{city_ua}]: {e}")
        return None
