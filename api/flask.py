# api/flask.py

from flask import Flask, render_template, request
from src.data_access import DataAccess
from src.data_processing import DataProcessor

"""
# Get the absolute path for templates folder
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
app = Flask(__name__, template_folder=template_folder)
"""

# Initialize Flask app
app = Flask(__name__)

# Instantiate your classes
data_access = DataAccess()
data_processor = DataProcessor()

@app.route('/')
def index():
    """
    Render the main page with a search form.
    """
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """
    Handle search requests and display results.
    """
    if request.method == 'POST':
        word_to_search = request.form['word']
        hanja_results = data_access.get_hanja_meanings_for_word(word_to_search)

        return render_template('index.html', word=word_to_search, results=hanja_results)

# This is needed for Vercel to run the app as a serverless function
def vercel_app(environ, start_response):
    return app(environ, start_response)

