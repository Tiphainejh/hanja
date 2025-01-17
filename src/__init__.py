#! @file src/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register routes, blueprints, etc.
    from src import routes  # Import routes or register them using blueprints
    
    return app

#from data_access import create_connection, initialize_database
#from data_processing import extract_data, process_data