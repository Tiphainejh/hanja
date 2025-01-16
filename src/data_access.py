# src/data_access.py
import sqlite3
from config import DATABASE_PATH
from database import DatabaseConnection

class DataAccess:
    def initialize_database(self):
        """
        Initializes the database by creating necessary tables if they don't already exist.
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
                conn.commit()  # Save the changes to the database
                print("Tables created.")
            else:
                print("Tables already exist.")

    def insert_data(self, processed_data):
        """
        Inserts processed data into the 'korean_words' table.
        :param processed_data: A list of dictionaries containing word data.
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            for entry in processed_data:
                word_id = entry['id']  # Extract the word ID
                word = entry['word']  # Extract the word itself
                glossary = entry['glossary']  # Extract the glossary/meaning
                hanja_str = entry['hanja']  # Extract the associated Hanja characters

                # Insert the data into the 'korean_words' table
                cursor.execute('''
                INSERT OR IGNORE INTO korean_words (id, word, hanja, glossary)
                VALUES (?, ?, ?, ?)
                ''', (word_id, word, hanja_str, glossary))
            conn.commit()  # Save changes to the database

    def insert_hanja_data(self, hanja_dict):
        """
        Inserts Hanja data into the 'hanja_characters' table.
        :param hanja_dict: A dictionary where keys are Hanja characters, and values are lists of related Korean data.
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            for chi, items in hanja_dict.items():  # Iterate over each Hanja character and its related items
                for item in items:
                    korean = item['kor']  # Extract the Korean pronunciation
                    meaning = item['def']  # Extract the Hanja meaning

                    # Insert the Hanja data into the 'hanja_characters' table
                    cursor.execute('''
                    INSERT OR IGNORE INTO hanja_characters (character, korean, meaning)
                    VALUES (?, ?, ?)
                    ''', (chi, korean, meaning))
            conn.commit()  # Save changes to the database

    def drop_tables(self, cursor):
        """
        Drops the 'hanja_characters' and 'korean_words' tables if they exist.
        :param cursor: The database cursor for executing SQL commands.
        """
        try:
            # Drop the 'hanja_characters' table
            cursor.execute('DROP TABLE IF EXISTS hanja_characters')
            print("Table 'hanja_characters' has been dropped.")

            # Drop the 'korean_words' table
            cursor.execute('DROP TABLE IF EXISTS korean_words')
            print("Table 'korean_words' has been dropped.")
        except sqlite3.Error as e:
            print(f"Error dropping tables: {e}")

    def get_hanja_meanings_for_word(self, word):
        """
        Retrieves Hanja meanings associated with a given Korean word.
        :param word: The Korean word for which to fetch Hanja meanings.
        :return: A list of tuples containing Hanja character, Korean pronunciation, and meaning.
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()

            # Fetch the associated Hanja string for the given word
            cursor.execute('SELECT hanja FROM korean_words WHERE word = ?', (word,))
            hanja_result = cursor.fetchone()
            
            if hanja_result:  # Check if Hanja data exists for the word
                hanja_string = hanja_result[0]
                if hanja_string is None:  # Handle cases where Hanja data is empty
                    print(f"No Hanja found for word '{word}'.")
                    return None
                else:
                    # Convert the Hanja string into a list of individual characters
                    hanja_list = list(hanja_string)

                    # Fetch Hanja details from the 'hanja_characters' table
                    query = 'SELECT character, korean, meaning FROM hanja_characters WHERE character IN ({seq})'.format(
                        seq=','.join(['?'] * len(hanja_list))  # Prepare placeholders for the query
                    )
                    cursor.execute(query, hanja_list)
                    results = cursor.fetchall()  # Fetch all matching records
                    return results
            else:
                # Handle cases where the word has no Hanja data in the database
                print(f"No Hanja found for word '{word}'.")
                return None
