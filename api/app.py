# ! @file api/app.py

from flask import Flask, render_template, request
from src.data_access import DataAccess
from src.data_processing import DataProcessor
import os

# Get the absolute path for templates folder
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
app = Flask(__name__, template_folder=template_folder)

# Instantiate the classes and specify the path to the folder
folder_path = "data/전체 내려받기_한국어기초사전_json_20250112"
data_access = DataAccess()
data_processor = DataProcessor(folder_path)

@app.route('/')
def index():
    """!
    @brief Render the main page with a search form.
    """
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """!
    @brief Handle search requests and display results.
    """
    if request.method == 'POST':
        word_to_search = request.form['word']
        print(f"Word to search: {word_to_search}")  # This will print in the terminal or logs
        
        hanja_results = data_access.get_hanja_meanings_for_word(word_to_search)
        print(f"Hanja results: {hanja_results}")  # Check what the results look like
        
        korean_results = data_access.get_word_by_korean(word_to_search)
        print(f"Korean results: {korean_results}")  # Check what the results look like

        return render_template('index.html', word=word_to_search, hanja_results=hanja_results, korean_results=korean_results)

# This is needed for Vercel to run the app as a serverless function
def vercel_app(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)

