from email import header
from flask import Blueprint, render_template, request
from matplotlib.font_manager import json_dump
from tinydb import Query
from . import DB
from .Classes import TreeNode, Scraper, Tree, Tuples, Database
import json

myapp = Blueprint('myapp', __name__)

@myapp.route('/')
def index():
    return render_template('index.html')

@myapp.route('/create', methods=['GET','POST'])
def create():
    # on récupère l'url à scrapper
    if request.is_json:
        url = request.json['url']
            
        # on verifie si l'url existe déjà dans la db
        db = Database(DB)
        if db.contains_url(url) :
            return {'error':'Url "'+url+'" found'}
        # sinon on crée une entrée en db {url , mots}
        else:
            words = Scraper(url, 'p').get_words()
            tuples = Tuples(words).get_tuples()
            id_url = db.create_url(url, tuples)
            return created_json(str(id_url))
        
    return render_template('index.html')

@myapp.route('/delete', methods=['GET','POST'])
def delete():
    if request.is_json:
        id_url = request.json['id_url']
        # on verifie si l'id est absent de la db
        db = Database(DB)
        if not db.contains_id(id_url):
            return nocontent_json(str(id_url))
        # sinon on le supprime de la db
        else:
            db.remove_url(id_url)
        return accepted_json(str(id_url))

    return render_template('index.html')

@myapp.route('/read', methods=['GET','POST'])
def read():
    if request.is_json:
        id_url = request.json['id_url']
        # on verifie si l'id est absent de la db
        db = Database(DB)
        if not db.contains_id(id_url):
            return nocontent_json(str(id_url))
        # sinon on récupère son contenu
        else:
            words = db.get_words(id_url)
            return words
    return render_template('index.html')

@myapp.route('/read_all', methods=['GET','POST'])
def read_all():
    if request.is_json:
        db = Database(DB)
        return json.dumps(db.get_all())
    return render_template('index.html')

@myapp.route('/delete_all', methods=['GET','POST'])
def delete_all():
    if request.is_json:
        db = Database(DB)
        db.clear_db()
        return accepted_json()
    return render_template('index.html')

@myapp.route('/graph', methods=['GET','POST'])
def graph():
    if request.is_json:
        id_url = request.json['id_url']
        db = Database(DB)
        url = db.get_words(id_url)
        tuples = convert_to_tuples(url['words'])
        tree = Tree.build_tree(tuples)
        tree1 = Tree.show_tree(tree)
        for i in tree1:
            for j in parse_tuple(i).key:
                print(parse_tuple(j).key)
        

        # On récupère un arbre binaire
        #tree = Tree.build_tree(tuples)
        # On affiche un arbre
        #print(Tree.show_tree(tree))
        #return json.dumps(Tree.show_tree(tree))
    return render_template('index.html')


def nocontent_json(id):
    return {'204 No content' : 'id '+id+' not found'}

def accepted_json(id):
    return {'202 Accepted' : 'id '+id+' successfully deleted'}

def created_json(id):
    return {'201 Created' : 'id '+id+' successfully created'}

def convert_to_tuples(words):
    list_of_tuples = []
    for word in words:
        list_of_tuples.append(tuple(word))
    return list_of_tuples
