#! @file src/main.py
from src.data_access import DataAccess
from src.data_processing import DataProcessor

def main():
    """
    @brief Main function to orchestrate the data extraction, processing, and database operations.

    - Initializes the database and creates tables if they don't exist.
    - Extracts and processes word data, then inserts it into the database.
    - Reads and processes hanja data from a file, then inserts it into the database.
    - Retrieves and displays hanja characters and meanings for a given Korean word.
    """

    data_access = DataAccess()
    # Specify the path to the folder
    folder_path = "data/전체 내려받기_한국어기초사전_json_20250112"
    data_processor = DataProcessor(folder_path)

    
    # Extract and process word data
    raw_data = data_processor.extract_data()
    processed_data = data_processor.process_data(raw_data)
    
    # Initialize the database and create tables
    data_access.drop_tables()
    data_access.initialize_database()
    data_access.insert_data(processed_data)
    """
    # Read and process hanja data
    lines = data_processor.read_hanja_file('data/hanja.txt')
    hanja_dict = data_processor.process_hanja_data(lines)
    data_access.insert_hanja_data(hanja_dict)
    data_access.remove_duplicates()
    """

if __name__ == '__main__':
    main()
