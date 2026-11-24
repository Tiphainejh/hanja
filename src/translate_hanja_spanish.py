#! @file src/translate_hanja_spanish.py
"""!
@brief Translates the meanings of the hanja characters from English to Spanish
and fills hanja_characters.spanishDefinition.

Uses Google Translate through deep-translator (already in requirements.txt),
one request per meaning, with a few requests running at the same time.
Translations are saved in data/hanja_spanish_cache.json as they arrive, so the
script can be stopped and started again without losing work.

Run from the repository root:  python -m src.translate_hanja_spanish
"""
import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from deep_translator import GoogleTranslator

from src.database import DatabaseConnection

CACHE_PATH = os.path.join("data", "hanja_spanish_cache.json")
WORKERS = 3  # requests running at the same time
PAUSE_ON_LIMIT = 60  # seconds to wait when Google says there are too many requests
MAX_ATTEMPTS = 6

_pause_lock = threading.Lock()
_paused_until = [0.0]  # shared by all workers: when Google complains, everybody waits
SAVE_EVERY = 100  # progress is shown and saved every 100 meanings
STROKES = re.compile(r"\s*(\(\d+\))\s*$")  # stroke count at the end, e.g. "(8)"


def split_strokes(text):
    """!
    @brief Separates the meaning from the stroke count at its end.
    @return (meaning, stroke count or "").
    """
    match = STROKES.search(text)
    if match:
        return text[:match.start()].strip(), match.group(1)
    return text.strip(), ""


def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as file:
        json.dump(cache, file, ensure_ascii=False, indent=0)


def wait_if_paused():
    while True:
        remaining = _paused_until[0] - time.time()
        if remaining <= 0:
            return
        time.sleep(min(remaining, 5))


def pause_everyone(seconds):
    with _pause_lock:
        if _paused_until[0] < time.time() + seconds:
            _paused_until[0] = time.time() + seconds
            print(f"  Google says there are too many requests: pausing {seconds} s...", flush=True)


def translate_one(text):
    """!
    @brief Translates one meaning. When Google limits the requests, all workers pause together.
    @return (english, spanish or None if it failed; it will be retried on the next run).
    """
    translator = GoogleTranslator(source="en", target="es")
    for attempt in range(MAX_ATTEMPTS):
        wait_if_paused()
        try:
            result = translator.translate(text)
            time.sleep(1)  # stay well under 5 requests per second
            return text, (result or "").strip() or None
        except Exception as error:
            if "too many requests" in str(error).lower():
                pause_everyone(PAUSE_ON_LIMIT * (attempt + 1))
            else:
                print(f"  Error on '{text[:40]}' ({error}), retrying...", flush=True)
                time.sleep(5)
    return text, None


def main():
    cache = load_cache()

    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        columns = [row[1] for row in cursor.execute("PRAGMA table_info(hanja_characters)")]
        if "spanishDefinition" not in columns:
            cursor.execute("ALTER TABLE hanja_characters ADD COLUMN spanishDefinition TEXT")
        rows = cursor.execute("SELECT id, englishDefinition FROM hanja_characters").fetchall()

        meanings = sorted({split_strokes(english)[0] for _, english in rows if english})
        to_translate = [m for m in meanings if m and m not in cache]
        print(f"{len(meanings)} different meanings, {len(to_translate)} left to translate.", flush=True)

        done = 0
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = [pool.submit(translate_one, text) for text in to_translate]
            for future in as_completed(futures):
                english, spanish = future.result()
                if spanish:
                    cache[english] = spanish
                done += 1
                if done % SAVE_EVERY == 0 or done == len(to_translate):
                    save_cache(cache)
                    print(f"{done}/{len(to_translate)} done ({len(cache)} meanings translated in total).", flush=True)

        updated = 0
        for row_id, english in rows:
            if not english:
                continue
            meaning, strokes = split_strokes(english)
            spanish = cache.get(meaning)
            if spanish:
                spanish = spanish[:1].upper() + spanish[1:]
                if strokes:
                    spanish = f"{spanish} {strokes}"
                cursor.execute(
                    "UPDATE hanja_characters SET spanishDefinition = ? WHERE id = ?",
                    (spanish, row_id),
                )
                updated += 1
        conn.commit()

    missing = len([m for m in meanings if m and m not in cache])
    print(f"Done: {updated} hanja now have a Spanish meaning.")
    if missing:
        print(f"{missing} meanings could not be translated: run the script again to retry them.")


if __name__ == "__main__":
    main()
