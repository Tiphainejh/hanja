import sqlite3
from config import DATABASE_PATH
from database import DatabaseConnection

class DataAccess:
    def initialize_database(self):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            # Check if tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='korean_words'")
            table_exists = cursor.fetchone()
            
            if not table_exists:
                # Create tables if they don't exist
                cursor.execute('''
                CREATE TABLE korean_words (
                    id INTEGER PRIMARY KEY,
                    word TEXT NOT NULL,
                    hanja TEXT,
                    glossary TEXT
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
                conn.commit()
                print("Tables created.")
            else:
                print("Tables already exist.")

    def insert_data(self, processed_data):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            for entry in processed_data:
                word_id = entry['id']
                word = entry['word']
                glossary = entry['glossary']
                hanja_str = entry['hanja']

                # Insert into 'korean_words'
                cursor.execute('''
                INSERT OR IGNORE INTO korean_words (id, word, hanja, glossary)
                VALUES (?, ?, ?, ?)
                ''', (word_id, word, hanja_str, glossary))
            conn.commit()

    def insert_hanja_data(self, hanja_dict):
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
        try:
            cursor.execute('DROP TABLE IF EXISTS hanja_characters')
            print("Table 'hanja_characters' has been dropped.")
            cursor.execute('DROP TABLE IF EXISTS korean_words')
            print("Table 'korean_words' has been dropped.")
        except sqlite3.Error as e:
            print(f"Error dropping tables: {e}")

    def get_hanja_meanings_for_word(self, word):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT hanja FROM korean_words WHERE word = ?', (word,))
            hanja_result = cursor.fetchone()
            
            if type(hanja_result) != None:
                hanja_string = hanja_result[0]
                if hanja_string is None :
                    print(f"No hanja found for word '{word}'.")
                    return None
                else :
                    hanja_list = list(hanja_string)  # Convert to a list of characters

                    query = 'SELECT character, korean, meaning FROM hanja_characters WHERE character IN ({seq})'.format(
                        seq=','.join(['?']*len(hanja_list))
                    )
                    cursor.execute(query, hanja_list)
                    results = cursor.fetchall()
                    return results
            else:
                print(f"No hanja found for word '{word}'.")
                return None