# """
# fetch_norwegian_names.py
# ========================
# Підтягує справжні норвезькі (Bokmål) назви міст через Wikidata API
# і додає їх як "no" в об'єкт translations кожного міста.

# Встановлення залежностей:
#     pip install aiohttp tqdm

# Запуск:
#     python fetch_norwegian_names.py

# Файли:
#     INPUT      — cities.json          (вхідний файл)
#     OUTPUT     — cities_with_no.json  (результат)
#     CHECKPOINT — checkpoint.json      (прогрес; видали щоб почати заново)
# """

# import asyncio
# import json
# from pathlib import Path

# import aiohttp
# from tqdm import tqdm

# # ── Налаштування ──────────────────────────────────────────────────────────────

# BASE_DIR   = Path(__file__).parent
# INPUT      = BASE_DIR / "cities.json"
# OUTPUT     = BASE_DIR / "cities_with_no.json"
# CHECKPOINT = BASE_DIR / "checkpoint.json"

# BATCH_SIZE  = 50    # Wikidata API приймає до 50 QID за раз
# CONCURRENT  = 8     # паралельних запитів одночасно (не збільшуй > 10)
# RETRY_MAX   = 4     # спроб при помилці
# RETRY_DELAY = 2.0   # початкова затримка між спробами (подвоюється)

# WIKIDATA_API = "https://www.wikidata.org/w/api.php"

# # ── Завантаження чекпоінту ────────────────────────────────────────────────────

# def load_checkpoint() -> dict[str, str]:
#     """Повертає вже отримані переклади {wikiDataId: no_label}."""
#     if CHECKPOINT.exists():
#         with open(CHECKPOINT, encoding="utf-8") as f:
#             data = json.load(f)
#         print(f"[checkpoint] Відновлення: знайдено {len(data):,} записів")
#         return data
#     return {}

# def save_checkpoint(cache: dict[str, str]) -> None:
#     with open(CHECKPOINT, "w", encoding="utf-8") as f:
#         json.dump(cache, f, ensure_ascii=False)

# # ── Запит до Wikidata ─────────────────────────────────────────────────────────

# async def fetch_batch(
#     session: aiohttp.ClientSession,
#     qids: list[str],
#     semaphore: asyncio.Semaphore,
# ) -> dict[str, str]:
#     """
#     Запитує Wikidata API через POST для списку QID.
#     Повертає {qid: no_label}. Якщо норвезького підпису немає — None.
#     """
#     post_data = {
#         "action":    "wbgetentities",
#         "ids":       "|".join(qids),
#         "props":     "labels",
#         "languages": "no",
#         "format":    "json",
#     }
#     headers = {
#         "User-Agent":   "CityNorwegianLabels/1.0 (https://github.com/local; cities-project)",
#         "Content-Type": "application/x-www-form-urlencoded",
#     }

#     async with semaphore:
#         for attempt in range(1, RETRY_MAX + 1):
#             try:
#                 async with session.post(
#                     WIKIDATA_API,
#                     data=post_data,
#                     headers=headers,
#                     timeout=aiohttp.ClientTimeout(total=30),
#                 ) as resp:
#                     resp.raise_for_status()
#                     result_data = await resp.json()

#                 result = {}
#                 for qid, entity in result_data.get("entities", {}).items():
#                     labels = entity.get("labels", {})
#                     no_label = labels.get("no", {}).get("value")
#                     result[qid] = no_label   # може бути None
#                 return result

#             except Exception as e:
#                 if attempt == RETRY_MAX:
#                     print(f"\n[error] Пакет {qids[:3]}… провалився: {e}")
#                     return {qid: None for qid in qids}
#                 await asyncio.sleep(RETRY_DELAY * (2 ** (attempt - 1)))

#     return {qid: None for qid in qids}

# # ── Основна логіка ────────────────────────────────────────────────────────────

# async def main() -> None:
#     print("Завантаження cities.json …")
#     with open(INPUT, encoding="utf-8") as f:
#         cities = json.load(f)
#     print(f"Завантажено {len(cities):,} міст")

#     # Збираємо унікальні QID, які ще не в чекпоінті
#     cache = load_checkpoint()
#     all_qids = [
#         c["wikiDataId"] for c in cities
#         if c.get("wikiDataId") and c["wikiDataId"] not in cache
#     ]
#     unique_qids = list(dict.fromkeys(all_qids))  # без дублів, зі збереженням порядку

#     print(f"Потрібно запросити: {len(unique_qids):,} QID "
#           f"(у кеші: {len(cache):,}, без QID: {len(cities) - len(all_qids) - len(cache):,})")

#     # Розбиваємо на пакети
#     batches = [unique_qids[i : i + BATCH_SIZE] for i in range(0, len(unique_qids), BATCH_SIZE)]
#     print(f"Пакетів: {len(batches):,}  |  Паралельно: {CONCURRENT}  |  ~{len(batches) * 0.5 / 60:.0f} хв\n")

#     semaphore = asyncio.Semaphore(CONCURRENT)
#     checkpoint_interval = 100  # зберігати прогрес кожні N пакетів

#     connector = aiohttp.TCPConnector(limit=CONCURRENT)
#     async with aiohttp.ClientSession(connector=connector) as session:
#         with tqdm(total=len(unique_qids), unit="QID", desc="Wikidata") as pbar:
#             for i, batch in enumerate(batches):
#                 result = await fetch_batch(session, batch, semaphore)
#                 cache.update(result)
#                 pbar.update(len(batch))

#                 if (i + 1) % checkpoint_interval == 0:
#                     save_checkpoint(cache)
#                     pbar.write(f"[checkpoint] збережено {len(cache):,} записів")

#                 # невелика пауза між пакетами щоб не навантажувати API
#                 await asyncio.sleep(0.1)

#     save_checkpoint(cache)
#     print(f"\nWikidata: отримано {sum(v is not None for v in cache.values()):,} норвезьких назв")

#     # ── Застосовуємо до даних ─────────────────────────────────────────────────
#     stats = {"wikidata": 0, "fallback": 0, "no_id": 0}

#     for city in cities:
#         if not isinstance(city.get("translations"), dict):
#             city["translations"] = {}

#         qid = city.get("wikiDataId")
#         no_label = cache.get(qid) if qid else None

#         if no_label:
#             city["translations"]["no"] = no_label
#             stats["wikidata"] += 1
#         else:
#             # Fallback: нідерландська або англійська назва
#             fallback = (city.get("translations") or {}).get("nl") or city.get("name", "")
#             city["translations"]["no"] = fallback
#             if qid:
#                 stats["fallback"] += 1
#             else:
#                 stats["no_id"] += 1

#     print(f"\nРезультат:")
#     print(f"  ✅ Справжні норвезькі назви (Wikidata):    {stats['wikidata']:>8,}")
#     print(f"  ⚠️  Fallback (немає NO-мітки в Wikidata):  {stats['fallback']:>8,}")
#     print(f"  ℹ️  Без wikiDataId:                         {stats['no_id']:>8,}")

#     print("\nЗапис результату …")
#     with open(OUTPUT, "w", encoding="utf-8") as f:
#         json.dump(cities, f, ensure_ascii=False, indent=4)
#     print(f"✅ Готово → {OUTPUT}")


# if __name__ == "__main__":
#     asyncio.run(main())
"""
add_country_translations.py
===========================
Додає переклади назв країн на 4 мови (uk, ru, en, no) в cities.json

- Для кожного міста додає/оновлює "country_translations"
- Використовує Wikidata або простий мапінг для популярних країн
- Зберігає норвезькі назви міст, які ти вже додав

Запуск:
    python add_country_translations.py
"""

import json
from pathlib import Path

# ── Налаштування ──────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
INPUT    = BASE_DIR / "cities.json"
OUTPUT   = BASE_DIR / "cities_with_country_translations.json"

# Базовий словник перекладів країн (можна розширити)
COUNTRY_TRANSLATIONS = {
    "Ukraine": {
        "en": "Ukraine",
        "uk": "Україна",
        "ru": "Украина",
        "no": "Ukraina"
    },
    "Afghanistan": {
        "en": "Afghanistan",
        "uk": "Афганістан",
        "ru": "Афганистан",
        "no": "Afghanistan"
    },
    # Додай інші країни за потребою або зробимо автоматично через Wikidata пізніше
}

# ── Основна логіка ────────────────────────────────────────────────────────────

def main() -> None:
    print(f"Завантаження {INPUT} …")
    with open(INPUT, encoding="utf-8") as f:
        cities = json.load(f)

    print(f"Завантажено {len(cities):,} міст")

    updated = 0
    missing_countries = set()

    for city in cities:
        country_name = city.get("country_name") or city.get("country", "")
        if not country_name:
            continue

        # Ініціалізуємо translations країни
        if "country_translations" not in city or not isinstance(city.get("country_translations"), dict):
            city["country_translations"] = {}

        trans = COUNTRY_TRANSLATIONS.get(country_name, {
            "en": country_name,
            "uk": country_name,
            "ru": country_name,
            "no": country_name
        })

        city["country_translations"] = trans
        updated += 1

        if country_name not in COUNTRY_TRANSLATIONS:
            missing_countries.add(country_name)

    # Статистика
    print(f"\nДодано/оновлено переклади країн для {updated:,} міст")
    if missing_countries:
        print(f"   ⚠️  Країни без повних перекладів: {len(missing_countries)}")
        print(f"   Приклади: {list(missing_countries)[:10]}")

    print("\nЗапис результату …")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(cities, f, ensure_ascii=False, indent=2)

    print(f"✅ Готово → {OUTPUT}")


if __name__ == "__main__":
    main()