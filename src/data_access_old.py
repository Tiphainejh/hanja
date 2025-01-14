import sqlite3
from config import DATABASE_PATH

def create_connection(db_path=DATABASE_PATH):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None

def initialize_database():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        drop_hanja_characters_table()
        # Création des tables, par exemple :
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS korean_words (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL,
            hanja TEXT,
            glossary TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hanja_characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character TEXT NOT NULL UNIQUE,
            korean TEXT NOT NULL UNIQUE,
            meaning TEXT
        )
        ''')
        conn.commit()
        conn.close()
    else:
        print("Impossible d'initialiser la base de données.")

def insert_data(processed_data):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        for entry in processed_data:
            word_id = entry['id']
            word = entry['word']
            glossary = entry['glossary']
            hanja_str = entry['hanja']

            # Insertion du mot dans la table 'words'
            cursor.execute('''
            INSERT OR IGNORE INTO korean_words (id, word, hanja, glossary)
            VALUES (?, ?, ?, ?)
            ''', (word_id, word, hanja_str, glossary))

        conn.commit()
        conn.close()
    else:
        print("Failed to insert data into the database.")

def insert_hanja_data(hanja_dict):
    conn = create_connection()
    if conn:
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
        conn.close()
    else:
        print("Failed to insert hanja data into the database.")

def drop_hanja_characters_table():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DROP TABLE IF EXISTS hanja_characters')
            conn.commit()
            print("Table 'hanja_characters' has been dropped.")
        except sqlite3.Error as e:
            print(f"Error dropping table 'hanja_char': {e}")
    else:
        print("Failed to connect to the database.")

    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DROP TABLE IF EXISTS korean_words')
            conn.commit()
            print("Table 'korean_words' has been dropped.")
        except sqlite3.Error as e:
            print(f"Error dropping table 'korean_words': {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")


def get_hanja_meanings_for_word(word):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        # Retrieve the hanja string from the korean_words table
        cursor.execute('SELECT hanja FROM korean_words WHERE word = ?', (word,))
        hanja_result = cursor.fetchone()
        
        if hanja_result:
            hanja_string = hanja_result[0]
            hanja_list = list(hanja_string)  # Convert the string into a list of characters

            # Prepare a query to find meanings for each hanja character
            query = 'SELECT character, korean, meaning FROM hanja_characters WHERE character IN ({seq})'.format(
                seq=','.join(['?']*len(hanja_list))
            )
            cursor.execute(query, hanja_list)
            results = cursor.fetchall()
            conn.close()
            return results
        else:
            print(f"No hanja found for word '{word}'.")
            conn.close()
            return None
    else:
        print("Failed to connect to the database.")
        return None