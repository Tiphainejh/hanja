# src/data_processing.py
from datapackage import Package
import regex

class DataProcessor:
    def extract_data(self):
        """
        Extracts data from an online datapackage resource.
        Downloads and reads the 'kengdic' resource from the specified datapackage URL.
        :return: A list of dictionaries containing the raw data.
        """
        # Initialize the datapackage object from the provided URL
        package = Package('https://raw.githubusercontent.com/garfieldnate/kengdic/master/datapackage.json')
        # Get the 'kengdic' resource from the package
        resource = package.get_resource('kengdic')
        # Read the resource data in a keyed format (as a list of dictionaries)
        data = resource.read(keyed=True)
        # Return the extracted data (no additional processing here for now)
        return data

    def process_data(self, raw_data):
        """
        Processes raw data to extract and transform necessary fields for further use.
        :param raw_data: A list of dictionaries representing raw data entries.
        :return: A list of dictionaries with processed and relevant data.
        """
        processed_data = []
        for entry in raw_data:
            # Extract and transform specific fields from the raw data
            processed_entry = {
                'id': entry['id'],  # Unique identifier for the entry
                'word': entry['surface'],  # Korean word (surface form)
                'hanja': entry['hanja'],  # Hanja characters, if available
                'glossary': entry['gloss'],  # Glossary/meaning of the word
            }
            # Append the processed entry to the result list
            processed_data.append(processed_entry)
        # Return the fully processed data
        return processed_data

    def read_hanja_file(self, file_path):
        """
        Reads a Hanja data file line by line.
        :param file_path: Path to the Hanja data file.
        :return: A list of lines read from the file.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # Read all lines in the file
        return lines

    def process_hanja_data(self, lines):
        """
        Processes Hanja file lines to extract structured data.
        Groups Hanja characters, their corresponding Korean readings, and definitions.
        :param lines: A list of lines from the Hanja data file.
        :return: A dictionary where keys are Hanja characters and values are lists of corresponding Korean readings and definitions.
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
