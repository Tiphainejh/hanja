#! @file src/add_spanish.py
"""!
@brief Adds Spanish to the existing database without rebuilding it.

- korean_words: adds spanishLemma and spanishDefinition, filled from the Spanish
  equivalents (스페인어) of the krdict JSON export.
- hanja_characters: adds spanishDefinition, left empty until a source is found;
  the site shows the English meaning while it is empty.

Run from the repository root:  python -m src.add_spanish
"""
import json
import os
import sys

from src.data_processing import DataProcessor
from src.database import DatabaseConnection

FOLDER_PATH = "data/전체 내려받기_한국어기초사전_json_20250112"


def add_column(cursor, table, column):
    """!
    @brief Adds a TEXT column to a table if it does not exist yet.
    """
    columns = [row[1] for row in cursor.execute(f"PRAGMA table_info({table})")]
    if column not in columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")


def extract_spanish_entries(processor, folder_path):
    """!
    @brief Reads the krdict JSON files one by one and yields the Spanish data of each entry.
    @return Generator of (word, hanja, glossary, spanish_lemma, spanish_definition).
    """
    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith(".json"):
            continue
        print(f"Reading {filename}...", flush=True)
        with open(os.path.join(folder_path, filename), encoding="utf-8") as file:
            data = json.load(file)
        entries = data.get("LexicalResource", {}).get("Lexicon", {}).get("LexicalEntry", [])
        for entry in entries:
            word = processor.extract_word(entry.get("Lemma"))
            hanja = processor.extract_hanja(entry.get("feat"))
            glossary = processor.extract_korean_definition(entry)
            equivalents = processor.extract_equivalents(entry.get("Sense", {}))
            if isinstance(equivalents, dict):
                equivalents = [equivalents]
            spanish_lemma = spanish_definition = None
            for equivalent in equivalents:
                if processor.extract_language(equivalent) == "스페인어":
                    lemma = (processor.extract_lemma(equivalent) or "").strip().rstrip(".").strip()
                    spanish_lemma = lemma[:1].upper() + lemma[1:] + "." if lemma else None
                    spanish_definition = (processor.extract_definition(equivalent) or "").strip() or None
                    break
            if spanish_lemma or spanish_definition:
                yield word, hanja, glossary, spanish_lemma, spanish_definition


def main(folder_path=FOLDER_PATH):
    processor = DataProcessor(folder_path)
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        add_column(cursor, "korean_words", "spanishLemma")
        add_column(cursor, "korean_words", "spanishDefinition")
        add_column(cursor, "hanja_characters", "spanishDefinition")
        # Temporary index so that matching each entry stays fast
        cursor.execute("CREATE INDEX IF NOT EXISTS tmp_word_idx ON korean_words(word)")

        matched = missed = 0
        for word, hanja, glossary, lemma, definition in extract_spanish_entries(processor, folder_path):
            cursor.execute(
                """
                UPDATE korean_words SET spanishLemma = ?, spanishDefinition = ?
                WHERE word = ? AND hanja IS ? AND glossary IS ? AND spanishLemma IS NULL
                """,
                (lemma, definition, word, hanja, glossary),
            )
            if cursor.rowcount:
                matched += 1
            else:
                missed += 1
        cursor.execute("DROP INDEX IF EXISTS tmp_word_idx")
        conn.commit()

        total, filled = cursor.execute(
            "SELECT COUNT(*), COUNT(spanishLemma) FROM korean_words"
        ).fetchone()
        print(f"Entries matched: {matched}, not matched: {missed}")
        print(f"korean_words rows with Spanish: {filled} / {total}")


if __name__ == "__main__":
    main(*sys.argv[1:])
