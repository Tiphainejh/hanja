# src/config.py
import os

# Chemin vers la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '..', 'database', 'korean_learning.db')

# Autres configurations (par exemple, chemins vers les données, paramètres, etc.)