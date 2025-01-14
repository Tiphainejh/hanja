# src/main.py
from data_access import DataAccess
from data_processing import DataProcessor

def main():
    data_access = DataAccess()
    data_processor = DataProcessor()

    # Initialize the database and create tables
    data_access.initialize_database()

    # Extract and process word data
    raw_data = data_processor.extract_data()
    processed_data = data_processor.process_data(raw_data)
    data_access.insert_data(processed_data)

    # Read and process hanja data
    lines = data_processor.read_hanja_file('data/hanja.txt')
    hanja_dict = data_processor.process_hanja_data(lines)
    data_access.insert_hanja_data(hanja_dict)

    # Example word to search for
    word_to_search = '혼자'

    # Retrieve associated hanja characters and their meanings
    hanja_results = data_access.get_hanja_meanings_for_word(word_to_search)

    if hanja_results:
        print(f"Hanja characters and meanings associated with '{word_to_search}':")
        for hanja, korean, meaning in hanja_results:
            print(f"Character: {hanja}, Korean: {korean}, Meaning: {meaning}")
    else:
        print(f"No hanja characters found for '{word_to_search}'.")

if __name__ == '__main__':
    main()