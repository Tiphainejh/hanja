#! @file src/data_processing.py
from datapackage import Package
import regex
import os 
import json 

class DataProcessor:
    """!
    @class DataProcessor
    @brief A class to process the data of the json file.
    """
    def __init__(self, folder_path):
        """
        @brief Initialize the DataExtractor with the folder path containing the JSON files.
        @param folder_path Path to the folder with JSON files.
        """
        self.folder_path = folder_path

    def extract_data(self):
        """!
        @brief Extracts data from JSON files in the specified folder.
        Reads and combines the contents of all JSON files in the folder.
        @return A list of dictionaries containing the combined data from all JSON files.
        """
        combined_data = []  # Initialize an empty list to store data

        # Loop through all files in the folder
        for filename in os.listdir(self.folder_path):
            # Check if the file has a .json extension
            if filename.endswith('.json'):
                file_path = os.path.join(self.folder_path, filename)  # Get the full path to the file

                # Open and read the JSON file
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        # Load the JSON content
                        data = json.load(file)
                        # Append the data to the combined list
                        combined_data.extend(data if isinstance(data, list) else [data])
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {filename}: {e}")

        return combined_data

    def process_data(self, raw_data):
        """!
        @brief Processes raw data to extract and transform necessary fields for further use.
        @param raw_data A list of dictionaries representing raw data entries.
        @return A list of dictionaries with processed and relevant data.
        
        @property lexical_entries Represents a single lexical entry in the dictionary, containing various features of the word.
            Lemma:
                - A list of 'feat' elements that represent the main word form.
                - Each 'feat' contains:
                    - 'att': The attribute name, typically 'writtenForm' for the main word.
                    - 'val': The actual value, which is the word itself (e.g., '침팬지').
            RelatedForm:
                - Represents any related forms of the word, such as variations or inflections.
                - Typically contains 'feat' elements with 'att' representing the type of form (e.g., 'variant') and 'val' representing the word form (e.g., '침팬치').
            Sense:
                - Contains detailed information about the meaning(s) of the word.
                - Typically contains the following sub-elements:
                    - Equivalent: A list of 'feat' elements representing the word's equivalent forms in other languages.
                        Each 'feat' contains:
                            - 'att': The attribute name, such as 'language', 'lemma', or 'definition'.
                            - 'val': The corresponding value for the attribute, such as:
                                - 'language' -> The language name (e.g., '영어' for English, '프랑스어' for French).
                                - 'lemma' -> The word in the equivalent language.
                                - 'definition' -> The definition of the word in the equivalent language.
                    - SenseExample:
                        - Contains example usage of the word, typically in context.
                        - 'feat': A list containing:
                            - 'att': 'type' represents the type of example (e.g., '문장' for sentence, '대화' for conversation).
                            - 'val': The actual example text.
                    - att : could represent the identifier for sense.
                    - feat: This part contains the different specifications
                        - 'att': 'type' represents different specifications of the word such as 'homonym_number', 'partOfSpeech', 'origin', 'vocabularyLevel', 'lexicalUnit'.
                        - 'val': The actual value of the specification.
                    - val : could represent the id of the word
            WordForm:
                - Contains pronunciation information or other related word forms.
                - Typically contains 'feat' elements with:
                    - 'att': 'pronunciation' for pronunciation details.
                    - 'val': The value for pronunciation or another related form.
            att:
                - Can represent various attributes or features of the word, such as:
                    - 'id': The unique identifier for the lexical entry.
                    - 'partOfSpeech': The part of speech (e.g., 'noun', 'verb').
                    - 'origin': The origin of the word (e.g., '한자' for Hanja-based words).
            feat:
                - Contains various additional features of the word, such as:
                    - 'att': Could include attributes like 'homonym_number', 'partOfSpeech', 'origin', 'vocabularyLevel', 'lexicalUnit'.
                    - 'val': The actual value for each feature (e.g., a specific homonym number, part of speech, or origin of the word).
            val:
                - Can represent a variety of values such as the 'id' of the word, or specific properties like part of speech or lexical unit.
        """
        processed_data = []
        for file in raw_data:
            lexical_entries = file.get("LexicalResource", {}).get("Lexicon", {}).get("LexicalEntry", [])
            
            # Variables to store data
            korean_definition = None
            english_lemma = None
            english_definition = None
            french_lemma = None
            french_definition = None
            language = None
            lemma = None
            definition = None
            
            # Iterate through the Lexical Entries
            for entry in lexical_entries:
                lemma_data = entry.get("Lemma")
                korean_word = self.extract_word(lemma_data)
                hanja_datas = entry.get("feat")
                hanja = self.extract_hanja(hanja_datas)
                korean_definition = self.extract_korean_definition(entry)
                equivalents = self.extract_equivalents(entry.get("Sense", {}))
              
                for equivalent in equivalents:
                    language = self.extract_language(equivalent)
                    lemma = self.extract_lemma(equivalent)
                    definition = self.extract_definition(equivalent)
                    
                    # Store the English and French data specifically
                    if language == "영어":
                        english_lemma = lemma
                        english_definition = definition
                    elif language == "프랑스어":
                        french_lemma = lemma
                        french_definition = definition

                # Extract and transform specific fields from the raw data
                processed_entry = {
                    'word': korean_word,  # Korean word (surface form)
                    'hanja': hanja,  # Hanja characters, if available
                    'glossary': korean_definition,  # Glossary/meaning of the word
                    'englishLemma' : english_lemma,
                    'englishDefinition' : english_definition,
                    'frenchLemma' : french_lemma,
                    'frenchDefinition' : french_definition,
                }
                # Append the processed entry to the result list
                processed_data.append(processed_entry) 

        # Return the fully processed data """
        return processed_data
    
    def extract_word(self, lemma_datas):
        """! 
        @brief Extracts the 'val' from the lemma element.
        @param lemma_data The lemma data, which can be a list or a dictionary.
        @return The extracted word value, or None if not found.
        """
        if isinstance(lemma_datas, list):
            # If it's a list, iterate through each item
            for lemma_data in lemma_datas:
                if "feat" in lemma_data:
                    return lemma_data["feat"].get("val")
        elif isinstance(lemma_datas, dict):
            # If it's a single dictionary
            return lemma_datas.get("feat", {}).get("val")
        return None

    def extract_hanja(self, hanja_datas):
        """! 
        @brief Extracts the 'origin' feat value for hanja from the entry.
        @param hanja_datas The hanja data, which can be a list or a dictionary.
        @return The extracted hanja value, or None if not found.
        """
        hanja = None
        if isinstance(hanja_datas, list):
            for hanja_data in hanja_datas:
                if hanja_data.get("att") == "origin":
                    hanja = hanja_data.get("val")
        elif isinstance(hanja_datas, dict) and hanja_datas.get("att") == "origin":
            hanja = hanja_datas.get("val")
        return hanja

    def extract_equivalents(self, sense_datas):
        """! 
        @brief Extracts the Equivalent data from the Sense.
        @param sense_data The Sense data, which can be a list or a dictionary.
        @return The extracted Equivalent data, or an empty dictionary if not found.
        """
        equivalents = {}
        if isinstance(sense_datas, list):
            equivalents = sense_datas[0].get('Equivalent', {}) #only getting the first one because the others are similar
        elif isinstance(sense_datas, dict):
            equivalents = sense_datas.get('Equivalent', {})
        return equivalents

    def extract_language(self, equivalents):
        """! 
        @brief Extracts the 'language' from the Equivalent.
        @param equivalents A dictionary containing equivalent data.
        @return The language value, or None if not found.
        """
        return next((f["val"] for f in equivalents.get("feat", []) if f["att"] == "language"), None)

    def extract_lemma(self, equivalents):
        """! 
        @brief Extracts the 'lemma' from the Equivalent.
        @param equivalents A dictionary containing equivalent data.
        @return The lemma value, or None if not found.
        """
        return next((f["val"] for f in equivalents.get("feat", []) if f["att"] == "lemma"), None)

    def extract_definition(self, equivalents):
        """! 
        @brief Extracts the 'definition' from the Equivalent.
        @param equivalents A dictionary containing equivalent data.
        @return The definition value, or None if not found.
        """
        return next((f["val"] for f in equivalents.get("feat", []) if f["att"] == "definition"), None)

    def extract_korean_definition(self, entry):
        """! @brief Extracts the 'definition' feat value for the Korean definition from the entry.    
        @param entry A dictionary representing a single lexical entry.
        @return The Korean definition if present, otherwise None."""
        
        sense_data = entry.get("Sense", {})
        # Normalize `sense_data` to always be a list for consistency
        sense_list = sense_data if isinstance(sense_data, list) else [sense_data]

        for sense in sense_list:
            sense_feat = sense.get("feat", [])
            # Normalize `sense_feat` to always be a list
            sense_feat_list = sense_feat if isinstance(sense_feat, list) else [sense_feat]

            for feat in sense_feat_list:
                if feat.get("att") == "definition":
                    return feat.get("val")  # Return the first definition found
        return None  # If no definition is found
    
    def read_hanja_file(self, file_path):
        """!
        @brief Reads a Hanja data file line by line.
        @param file_path Path to the Hanja data file.
        @return A list of lines read from the file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # Read all lines in the file
        return lines

    def process_hanja_data(self, lines):
        """!
        @brief Processes Hanja file lines to extract structured data.
        Groups Hanja characters, their corresponding Korean readings, and definitions.
        @param lines A list of lines from the Hanja data file.
        @return A dictionary where keys are Hanja characters and values are lists of corresponding Korean readings and definitions.
        """
        hanja_dict = {}  # Dictionary to store processed Hanja data
        kor = ''  # Variable to keep track of the Korean context for Hanja

        for line in lines:
            line = line.strip()  # Remove surrounding whitespace
            if line.startswith('[') and line.endswith(']'):
                # Lines with square brackets contain Korean context (e.g., [context])
                kor = line[1:-1]
            else:
                # Lines without brackets represent Hanja entries with definitions
                if '=' in line:
                    # Split the line into the Hanja character and the rest of the entry
                    kor_part = []  # Korean readings (Hangul)
                    def_part = []  # Definitions (non-Hangul parts)
                    chi, rest = line.split('=', 1)  # Separate the Hanja character and its data
                    parts = rest.split(',')  # Split data into individual parts

                    # Classify parts as Hangul or non-Hangul
                    for part in parts:
                        if regex.search(r'\p{IsHangul}', part):  # Check if the part contains Hangul
                            kor_part.append(part.strip())
                        else:
                            def_part.append(part.strip())

                    # Join the classified parts into strings
                    kor_parts = ', '.join(kor_part)
                    def_parts = ', '.join(def_part)

                    # Create a structured entry for the current Hanja character
                    item = {
                        'kor': kor_parts,  # Korean readings
                        'def': def_parts  # Definitions
                    }

                    # Add the entry to the dictionary under the current Hanja character
                    if chi in hanja_dict:
                        hanja_dict[chi].append(item)  # Append to existing entries
                    else:
                        hanja_dict[chi] = [item]  # Create a new list for this character

        # Return the fully processed Hanja dictionary
        return hanja_dict
