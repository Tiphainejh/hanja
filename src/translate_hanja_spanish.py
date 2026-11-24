#! @file src/translate_hanja_spanish.py
"""!
@brief Translates the meanings of the hanja characters from English to Spanish
and fills hanja_characters.spanishDefinition.

Uses Google Translate through deep-translator (already in requirements.txt).
Several meanings are sent in one request, one per line, to keep the number of
requests low. Translations are saved in data/hanja_spanish_cache.json as they
arrive, so the script can be stopped and started again without losing work.

Run from the repository root:  python -m src.translate_hanja_spanish
"""
import json
import os
import re
import time

from deep_translator import GoogleTranslator

from src.database import DatabaseConnection

CACHE_PATH = os.path.join("data", "hanja_spanish_cache.json")
MAX_CHARS = 4000  # Google Translate accepts up to 5000 characters per request
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


def make_chunks(texts):
    """!
    @brief Groups meanings into chunks of at most MAX_CHARS characters.
    """
    chunk, size = [], 0
    for text in texts:
        if chunk and size + len(text) + 1 > MAX_CHARS:
            yield chunk
            chunk, size = [], 0
        chunk.append(text)
        size += len(text) + 1
    if chunk:
        yield chunk


def request(translator, text):
    """!
    @brief Sends one request to Google Translate, retrying on network errors or rate limits.
    @return The translated text, or None after 3 failures.
    """
    for attempt in range(3):
        try:
            return translator.translate(text)
        except Exception as error:
            print(f"  Error ({error}), retrying in {5 * (attempt + 1)} s...")
            time.sleep(5 * (attempt + 1))
    return None


def translate_chunk(translator, chunk):
    """!
    @brief Translates a chunk of meanings, one per line.
    If Google merges or splits lines, the chunk is cut in two and each half is
    translated again, so only a few extra requests are needed.
    """
    result = request(translator, "\n".join(chunk))
    lines = [line.strip() for line in (result or "").split("\n")]
    if result is not None and len(lines) == len(chunk):
        return lines
    if len(chunk) == 1:
        return [result.strip() if result else None]
    middle = len(chunk) // 2
    return translate_chunk(translator, chunk[:middle]) + translate_chunk(translator, chunk[middle:])


def main():
    translator = GoogleTranslator(source="en", target="es")
    cache = load_cache()

    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        columns = [row[1] for row in cursor.execute("PRAGMA table_info(hanja_characters)")]
        if "spanishDefinition" not in columns:
            cursor.execute("ALTER TABLE hanja_characters ADD COLUMN spanishDefinition TEXT")
        rows = cursor.execute("SELECT id, englishDefinition FROM hanja_characters").fetchall()

        meanings = sorted({split_strokes(english)[0] for _, english in rows if english})
        to_translate = [m for m in meanings if m and m not in cache]
        print(f"{len(meanings)} different meanings, {len(to_translate)} left to translate.")

        chunks = list(make_chunks(to_translate))
        for number, chunk in enumerate(chunks, start=1):
            for english, spanish in zip(chunk, translate_chunk(translator, chunk)):
                if spanish:
                    cache[english] = spanish
            save_cache(cache)
            print(f"Chunk {number}/{len(chunks)} done ({len(cache)} meanings translated).")
            time.sleep(1)

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
