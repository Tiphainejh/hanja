# src/data_processing.py
from datapackage import Package
import regex

class DataProcessor:
    def extract_data(self):
        package = Package('https://raw.githubusercontent.com/garfieldnate/kengdic/master/datapackage.json')
        resource = package.get_resource('kengdic')
        data = resource.read(keyed=True)
        # Additional processing if necessary
        return data

    def process_data(self, raw_data):
        # Process raw_data to extract necessary information
        processed_data = []
        for entry in raw_data:
            # Extract and transform data
            processed_entry = {
                'id': entry['id'],
                'word': entry['surface'],
                'hanja': entry['hanja'],
                'glossary': entry['gloss'],
            }
            processed_data.append(processed_entry)
        return processed_data

    def read_hanja_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines

    def process_hanja_data(self, lines):
        hanja_dict = {}
        kor = ''

        for line in lines:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                kor = line[1:-1]
            else:
                if '=' in line:
                    kor_part = []
                    def_part = []
                    chi, rest = line.split('=', 1)
                    parts = rest.split(',')

                    for part in parts:
                        if regex.search(r'\p{IsHangul}', part):
                            kor_part.append(part.strip())
                        else:
                            def_part.append(part.strip())
                    kor_parts = ', '.join(kor_part)
                    def_parts = ', '.join(def_part)

                    item = {
                        'kor': kor_parts,
                        'def': def_parts
                    }

                    if chi in hanja_dict:
                        hanja_dict[chi].append(item)
                    else:
                        hanja_dict[chi] = [item]

        return hanja_dict