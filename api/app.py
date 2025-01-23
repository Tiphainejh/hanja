# ! @file api/app.py

from flask import Flask, render_template, request, session, redirect, url_for, jsonify, make_response
from src.data_access import DataAccess
from src.data_processing import DataProcessor
from deep_translator import GoogleTranslator
import os

# Get the absolute path for templates folder

app = Flask(
    __name__,
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
)
app.secret_key = os.urandom(12).hex()

# Instantiate the classes and specify the path to the folder
folder_path = "data/전체 내려받기_한국어기초사전_json_20250112"
data_access = DataAccess()
data_processor = DataProcessor(folder_path)

@app.route('/')
def index():
    """!
    @brief Render the main page with a search form and sets the default language to english.
    """
    # Get the current language, default to English if not set
     # Essayer de récupérer la langue de la session, sinon du cookie
    language = session.get('language') or request.cookies.get('language', 'en')  # 'en' comme langue par défaut
    return render_template('index.html', language=language, is_homepage=True)

@app.route('/set_language', methods=['POST'])
def set_language():
    language = request.form['language']
    session['language'] = language  # Enregistrer la langue dans la session
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('language', language, max_age=30*24*60*60, secure=True, httponly=True)  # Enregistrer la langue dans le cookie (30 jours)
    return resp

@app.route('/search', methods=['POST'])
def search():
    """!
    @brief Handle search requests and display results.
    """
    language = session.get('language') or request.cookies.get('language', 'en')  # 'en' comme langue par défaut
    if request.method == 'POST':
        word_to_search = request.form['word'].replace(" ", "")
        hanja_characters = data_access.get_hanja_for_word(word_to_search)
        korean_results = data_access.get_word_by_korean(word_to_search, language)
        if hanja_characters == None :
            hanja_results = None
        else :
            hanja_results = data_processor.reorder_hanja_results(data_access.get_hanja_meanings_for_word(word_to_search, hanja_characters, language), hanja_characters)
            hanja_characters="".join(hanja_characters)
        
        text_language = {'def':"Définition", "lang":"Français", "load":"Recherche des mots liés...", "no_res":"Pas de résultats pour", "no_res_hanja":"Pas de hanja associé au mot", "no_related":"Aucun mot lié trouvé.", "err_load":"Erreur lors du chargement des données."} if language == "fr" else {'def': "Definition", "lang" : "English", "load":"Loading related words...", "no_res":"No results found for", "no_res_hanja":"No hanja character linked to the word", "no_related":"No related words found.", "err_load":"Error while loading the data."}
        return render_template('index.html', word=word_to_search, hanja_results=hanja_results, korean_results=korean_results, hanja_characters=hanja_characters, text_language=text_language, language=language, is_homepage=False)

@app.route('/related-words')
def related_words():
    language = session.get('language') or request.cookies.get('language', 'en')  # 'en' comme langue par défaut
    hanja_character = request.args.get('hanja')
    original_word = request.args.get('original_word')  # Pass the original word from the client-side
    print(original_word)
    # Query your database for related words
    related_words = data_access.get_related_words(hanja_character, language)
    
    # Filter duplicates by keeping only the first occurrence of each unique pair of Hanja
    # Filter duplicates and exclude the original word
    seen_hanja_pairs = set()
    unique_words = []
    for word in related_words:
        hanja = word['hanja']
        korean_word = word['word']
            
        # Exclude the original word
        if korean_word != original_word and hanja[:2] not in seen_hanja_pairs:
            seen_hanja_pairs.add(hanja[:2])
            unique_words.append(word)

    return jsonify(unique_words)

# This is needed for Vercel to run the app as a serverless function
def vercel_app(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)

