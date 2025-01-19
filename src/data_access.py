#! @file src/data_access.py
import sqlite3
from src.config import DATABASE_PATH
from src.database import DatabaseConnection

class DataAccess:
    """!
    @class DataAccess
    @brief A class to handle database operations for managing Korean words and their associated Hanja characters.
    """

    def initialize_database(self):
        """! 
        @brief Initializes the database by creating necessary tables if they don't already exist.

        Database Schema:
        ----------------
        **korean_words**
        - `id` (INTEGER, PRIMARY KEY): Unique identifier for each word.
        - `word` (TEXT, NOT NULL): Korean word.
        - `hanja` (TEXT): Associated Hanja characters.
        - `glossary` (TEXT): Word's glossary or definition in Korean.
        - `englishLemma` (TEXT): Lemma/word in English.
        - `englishDefinition` (TEXT): English definition of the word.
        - `frenchLemma` (TEXT): Lemma/word in French.
        - `frenchDefinition` (TEXT): French definition of the word.

        **hanja_characters**
        - `id` (INTEGER, PRIMARY KEY AUTOINCREMENT): Unique identifier for each Hanja character.
        - `character` (TEXT, NOT NULL, UNIQUE): The Hanja character.
        - `korean` (TEXT, NOT NULL): Korean pronunciation of the Hanja.
        - `meaning` (TEXT): Meaning of the Hanja character.

        \image html database_diagram.png width=400
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            # Check if the 'korean_words' table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='korean_words'")
            table_exists = cursor.fetchone()
            
            if not table_exists:
                # Create 'korean_words' and 'hanja_characters' tables if they don't exist
                cursor.execute('''
                CREATE TABLE korean_words (
                    id INTEGER PRIMARY KEY,
                    word TEXT NOT NULL,
                    hanja TEXT,
                    glossary TEXT,
                    englishLemma TEXT,
                    englishDefinition TEXT,
                    frenchLemma TEXT,
                    frenchDefinition TEXT
                )
                ''')
                cursor.execute('''
                CREATE TABLE hanja_characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    character TEXT NOT NULL UNIQUE,
                    korean TEXT NOT NULL,
                    meaning TEXT
                )
                ''')
                conn.commit()  # Save the changes to the database
                print("Tables created.")
            else:
                print("Tables already exist.")

    def insert_data(self, processed_data):
        """!
        @brief Inserts processed data into the 'korean_words' table.
        
        @param processed_data (list): A list of dictionaries containing word data. Each dictionary should have:
            - `id` (int): The unique ID for the word (optional if the database assigns it automatically).
            - `word` (str): The Korean word.
            - `hanja` (str): Associated Hanja characters.
            - `glossary` (str): Meaning of the word in Korean.
            - `englishLemma` (str): Lemma/word in English.
            - `englishDefinition` (str): English definition of the word.
            - `frenchLemma` (str): Lemma/word in French.
            - `frenchDefinition` (str): French definition of the word.
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            for entry in processed_data:
                word = entry['word']
                hanja = entry.get('hanja')
                glossary = entry.get('glossary')
                english_lemma = entry.get('englishLemma')
                english_definition = entry.get('englishDefinition')
                french_lemma = entry.get('frenchLemma')
                french_definition = entry.get('frenchDefinition')

                cursor.execute('''
                INSERT OR IGNORE INTO korean_words (
                    word, hanja, glossary, englishLemma, englishDefinition, frenchLemma, frenchDefinition
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (word, hanja, glossary, english_lemma, english_definition, french_lemma, french_definition))
            conn.commit()
            print("Values inserted in the table.")


    def insert_hanja_data(self, hanja_dict):
        """!
        @brief Inserts Hanja data into the 'hanja_characters' table.
        
        @param hanja_dict (dict): A dictionary mapping Hanja characters to a list of related Korean data. 
        Example:
        @code{.json}
                    {
                        '漢': [{'kor': '한', 'def': 'China'}],
                        '字': [{'kor': '자', 'def': 'character'}]
                    }
        @endcode
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            for chi, items in hanja_dict.items():
                for item in items:
                    korean = item['kor']
                    meaning = item['def']

                    cursor.execute('''
                    INSERT OR IGNORE INTO hanja_characters (character, korean, meaning)
                    VALUES (?, ?, ?)
                    ''', (chi, korean, meaning))
            conn.commit()

    def drop_tables(self, cursor):
        """!
        @brief Drops the 'hanja_characters' and 'korean_words' tables if they exist.
        
        @param cursor (sqlite3.Cursor): The database cursor for executing SQL commands.
        """
        try:
            cursor.execute('DROP TABLE IF EXISTS hanja_characters')
            print("Table 'hanja_characters' has been dropped.")
            cursor.execute('DROP TABLE IF EXISTS korean_words')
            print("Table 'korean_words' has been dropped.")
        except sqlite3.Error as e:
            print(f"Error dropping tables: {e}")

    def get_hanja_meanings_for_word(self, word):
        """!
        @brief Retrieves Hanja meanings associated with a given Korean word.
        
        @param word (str): The Korean word for which to fetch Hanja meanings.
        
        @return a list of tuples containing Hanja character, Korean pronunciation, and meaning.
                  Returns None if no data is found.
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT hanja FROM korean_words WHERE word = ?', (word,))
            hanja_result = cursor.fetchone()
            
            if hanja_result:
                hanja_string = hanja_result[0]
                if hanja_string is None:
                    print(f"No Hanja found for word '{word}'.")
                    return None
                else:
                    hanja_list = list(hanja_string)
                    query = 'SELECT character, korean, meaning FROM hanja_characters WHERE character IN ({seq})'.format(
                        seq=','.join(['?'] * len(hanja_list))
                    )
                    cursor.execute(query, hanja_list)
                    results = cursor.fetchall()
                    return results
            else:
                print(f"No Hanja found for word '{word}'.")
                return None
