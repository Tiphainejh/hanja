# ! @file api/app.py

from flask import Flask, render_template, request
from src.data_access import DataAccess
from src.data_processing import DataProcessor
import os

# Get the absolute path for templates folder
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
app = Flask(__name__, template_folder=template_folder)

# Instantiate your classes
data_access = DataAccess()
data_processor = DataProcessor()

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

        return render_template('index.html', word=word_to_search, results=hanja_results)

# This is needed for Vercel to run the app as a serverless function
def vercel_app(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)

