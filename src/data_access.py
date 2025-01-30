#! @file src/data_access.py
import sqlite3
from src.config import DATABASE_PATH
from src.database import DatabaseConnection

class DataAccess:
    """!
    @brief A class to handle database operations for managing Korean words and their associated Hanja characters.
    """

    def initialize_database(self):

        """!@brief Initializes the database by creating necessary tables if they don't already exist.
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
        - `englishDefinition` (TEXT): Meaning of the Hanja character in english.
        - `frenchDefinition` (TEXT): Meaning of the Hanja character in french.
        - `pronounciation` (TEXT): html link of audio for the word's pronounciation.

        @image html database_diagram.png width=400
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
                    frenchDefinition TEXT,
                    pronounciation TEXT
                )
                ''')
                """ cursor.execute('''
                CREATE TABLE hanja_characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    character TEXT NOT NULL UNIQUE,
                    korean TEXT NOT NULL,
                    englishDefinition TEXT,
                    frenchDefinition TEXT
                )
                ''') """
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
            - `pronounciation` (str): html link of audio for the word's pronounciation.
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
                pronounciation = entry.get('pronounciation')
                query = """
                INSERT INTO korean_words (word, hanja, glossary, englishLemma, englishDefinition, frenchLemma, frenchDefinition, pronounciation)
                SELECT ?, ?, ?, ?, ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM korean_words
                    WHERE word = ? AND hanja = ?
                );
                """
                cursor.execute(query, (word, hanja, glossary, english_lemma, english_definition, french_lemma, french_definition, pronounciation, word, hanja))
            conn.commit()
            print("Values inserted in the table korean_words.")


    def insert_hanja_data(self, hanja_dict):
        """!
        @brief Inserts Hanja data into the 'hanja_characters' table.
        
        @param hanja_dict (dict): A dictionary mapping Hanja characters to a list of related Korean data. 
        Example:
        @code{.json}
                    {
                        '漢': [{'kor': '한', 'englishDefinition': 'China'}, 'frenchDefinition': 'Chine'}],
                        '字': [{'kor': '자', 'englishDefinition': 'Character'}, 'frenchDefinition': 'Caractère'}]
                    }
        @endcode
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            for hanja, items in hanja_dict.items():
                for item in items:
                    korean = item['kor']
                    english_def = item['english_def']
                    french_def = item['french_def']
                    cursor.execute('''
                    INSERT OR IGNORE INTO hanja_characters (character, korean, englishDefinition, frenchDefinition)
                    VALUES (?, ?, ?, ?)
                    ''', (hanja, korean, english_def, french_def))
            conn.commit()
            print("Values inserted in the table hanja_characters.")

    def drop_tables(self):
        """!
        @brief Drops the 'hanja_characters' and 'korean_words' tables if they exist.
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DROP TABLE IF EXISTS korean_words')
                print("Table 'korean_words' has been dropped.")
            except sqlite3.Error as e:
                print(f"Error dropping tables: {e}")
       
    def remove_duplicates(self):

        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM korean_words WHERE id NOT IN ( SELECT MIN(id) FROM korean_words GROUP BY word, hanja);')
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error deleting duplicates: {e}") 
    
    def get_hanja_for_word(self, word):
        """!
        @brief Retrieves Hanja associated with a given Korean word.
        @param word (str): The Korean word for which to fetch Hanja character.
        @return a list of tuples containing Hanja character.
                  Returns None if no data is found.
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT hanja FROM korean_words WHERE word = ? AND hanja IS NOT NULL', (word,))
            hanja_result = cursor.fetchall()
            if hanja_result:
                if hanja_result is None:
                    print(f"No Hanja found for word '{word}'.")
                    return None
                else:
                    hanja_list = [h[0] for h in hanja_result]
                    return hanja_list

    def get_hanja_meanings_for_word(self, word, hanja_list, language):
        """!
        @brief Retrieves Hanja meanings of every characters associated with a given Korean word.
        @param word (str): The Korean word for which to fetch Hanja meanings.
        @param hanja_list (list): The list of hanja associated to the initial words.
        @param language (str): The language of the page.
        @return a list of tuples containing Hanja character, Korean pronunciation, and meaning.
                  Returns None if no data is found.
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
           
            if hanja_list is None:
                print(f"No Hanja found for word '{word}'.")
                return None
            else:         
                if language == "fr":           
                    query = 'SELECT character, korean, frenchDefinition FROM hanja_characters WHERE character IN ({seq})'.format(
                    seq=','.join(['?'] * len(hanja_list))
                )
                else :
                    query = 'SELECT character, korean, englishDefinition FROM hanja_characters WHERE character IN ({seq})'.format(
                    seq=','.join(['?'] * len(hanja_list))
                )
                cursor.execute(query, hanja_list)
                results = cursor.fetchall()
                return results


    def get_word_by_korean(self, korean_word, language, hanja_characters=None):
            """@brief Fetches a word entry by its Korean text.
            
            @param korean_word: The Korean word to search for.
            @param language: The language for the definition
            @return: A list of matching entries.
            """      
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                if hanja_characters == None :
                    if language == "fr":
                        cursor.execute("SELECT glossary, frenchLemma, frenchDefinition, pronounciation  FROM korean_words WHERE word = ?", (korean_word,))
                    else :
                        cursor.execute("SELECT glossary, englishLemma, englishDefinition, pronounciation  FROM korean_words WHERE word = ?", (korean_word,))
                    return cursor.fetchall()
                else :
                    if language == "fr":
                        conditions = " AND ".join(["hanja LIKE ?"] * len(hanja_characters))
                        query = f"""
                            SELECT glossary, frenchLemma, frenchDefinition, pronounciation 
                            FROM korean_words 
                            WHERE word = ? AND {conditions}
                        """

                        # Construire les paramètres de la requête (un '%' + caractère + '%' pour chaque caractère)
                        params = [korean_word] + [f"%{char}%" for char in hanja_characters]

                        cursor.execute(query, params)
                    else :
                        conditions = " AND ".join(["hanja LIKE ?"] * len(hanja_characters))
                        query = f"""
                            SELECT glossary, englishLemma, englishDefinition, pronounciation 
                            FROM korean_words 
                            WHERE word = ? AND {conditions}
                        """

                        # Construire les paramètres de la requête (un '%' + caractère + '%' pour chaque caractère)
                        params = [korean_word] + [f"%{char}%" for char in hanja_characters]

                        cursor.execute(query, params)
                    return cursor.fetchall()
            
    def get_related_words(self, hanja_character, language):
        """! @brief Gets all the words that contains the specified hanja character.
            
            @param hanja_character: the hanja character to search for.
            @param language: The language for the definition
            @return: A list of matching entries.
        """  
        if language == "fr" :
            query = """
            SELECT word, hanja, glossary, frenchLemma, frenchDefinition
            FROM korean_words
            WHERE hanja LIKE ?;
            """
        elif language == "en":
            query = """
            SELECT word, hanja, glossary, englishLemma, englishDefinition
            FROM korean_words
            WHERE hanja LIKE ?;
            """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
    
            # Execute the query
            cursor.execute(query, (f"%{hanja_character}%",))

            # Fetch all matching rows
            results = cursor.fetchall()

            # Map results to a list of dictionaries
            words = [
                {
                    "word": row[0],
                    "hanja": row[1],
                    "glossary": row[2],
                    "lemma": row[3],
                    "definition": row[4],
                }
                for row in results
            ]

            return words


    def find_word_with_unique_hanja(self):
        """!
        @brief Finds a Korean word where at least one Hanja character is unique to that word.
        @returns list of words with unique Hanja characters.
        """
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            # Step 1: Flatten all Hanja characters into a single column
            cursor.execute("SELECT word, hanja FROM korean_words WHERE hanja IS NOT NULL;")
            rows = cursor.fetchall()

            # Step 2: Create a mapping of Hanja characters to the words they appear in
            hanja_to_words = {}
            for word, hanja in rows:
                for char in hanja:  # Iterate over each character in the Hanja string
                    if char not in hanja_to_words:
                        hanja_to_words[char] = set()
                    hanja_to_words[char].add(word)

            # Step 3: Find unique Hanja characters and the corresponding words
            unique_hanja_words = []
            for char, words in hanja_to_words.items():
                if len(words) == 1:  # This Hanja character is unique
                    unique_hanja_words.append((list(words)[0], char))

            # Step 4: Filter the words that contain unique Hanja characters
            result_words = []
            for word, char in unique_hanja_words:
                result_words.append((word, char))

            return result_words
