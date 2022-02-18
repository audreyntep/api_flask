from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import re
from tinydb import TinyDB, Query
import networkx as nx


# Classe executant le scrapping
class Scraper:
    def __init__(self, url, tag):
        self.url = url
        self.tag = tag

    def parse(self):
        try:
            self.results = BeautifulSoup(requests.get(self.url).text, 'html.parser').find_all(self.tag)
        except HTTPError as e:
            print(e)

    def create_words(self):
        lists_of_strings = []
        for result in self.results:
            lists_of_strings.append(result.text.split())
        self.words = []
        for i in range(0,len(lists_of_strings)):
            for s in lists_of_strings[i]:
                out = re.sub(r'[^\w\s]','',s)
                self.words.append(out)
        
    def get_words(self):
        self.parse()
        self.create_words()
        return self.words


class Tree:
    # data = liste de tuples
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if self.data == None:
            self.data = data
        else:
            if data < self.data:
                if self.left is None:
                    self.left = Tree(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Tree(data)
                else:
                    self.right.insert(data)

    def get_data(self):
        return self.data

    def get_right(self):
        return self.right

    def get_left(self):
        return self.left

    def affiche(self):
        return self
    
    @staticmethod
    def build_tree(tuples):
        tree = Tree(tuples[0])
        for i in range(1,len(tuples)):
            tree.insert(tuples[i])
        return tree

    # fonction statique retournant un arbre
    @staticmethod
    def show_tree(Tree):
        if Tree != None:
            return (Tree.get_data(), Tree.show_tree(Tree.get_left()), Tree.show_tree(Tree.get_right()))


class Tuples:
    def __init__(self, words):
        self.words = words
    
    # fonction retournant une liste de tuples uniques : mot et nombre d'occurence du mot
    def create_tuples(self):
        tuples_without_occurences = []
        for word in self.words:
            tuples_without_occurences.append((word.lower(),1))
        tuples_with_occurences = []
        for tuple in tuples_without_occurences:
            occurence = tuples_without_occurences.count(tuple)
            tuples_with_occurences.append((tuple[0],occurence))
        self.tuples = []
        for tuple in tuples_with_occurences :
            if tuple not in self.tuples:
                self.tuples.append(tuple)

    def get_tuples(self):
        self.create_tuples()
        return self.tuples


class Database:
    def __init__(self, filename, data=None):
        self.db = TinyDB('project_api/'+filename,sort_keys=True, indent=2, separators=(',', ': '))
        if data != None:
            self.insert_data(data)

    def contains_url(self, url):
        return self.db.contains(Query().url == url)

    def create_url(self, url, data):
        return self.db.insert({'url': url, 'words': data})

    def contains_id(self, id):
        print(self.db.contains(doc_id=int(id)))
        return self.db.contains(doc_id=int(id))

    def remove_url(self, id):
        self.db.remove(doc_ids=[int(id)])

    def get_words(self, id):
        return self.db.get(doc_id=int(id))

    def get_all(self):
        return self.db.all()

    def get_url(self, id):
        if self.db.contains(doc_id=int(id)):
            return self.db.get(doc_id=int(id))
        else:
            return False


    def get_url_id(self, url):
        docs = self.db.search(Query().url == url)
        for doc in docs:
            return doc.doc_id

    def clear_db(self):
        self.db.truncate()
        self.db.all()

    def search_word(self, value):
        return self.db.search(Query().word == value)
    
