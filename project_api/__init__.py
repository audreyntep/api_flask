"""project api module

Ce module propose de parser des textes depuis des pages web en utilisant beautifulSoup.
Les url et leurs listes de mots sont stockés en base de données.

"""

from flask import Flask
import os.path
from .Classes import Database

DB = 'db.json'

def create_app():
    app = Flask(__name__)

    # Define Flask configuration
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'test'

    # Define route with Blueprint
    from .myapp import myapp
    app.register_blueprint(myapp, url_prefix='/')

    # Create databases
    create_database()
    
    return app

def create_database():
    # création de la database gestion des tables
    if not os.path.isfile('project_api/'+DB):
        Database(DB)






