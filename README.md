# API FLASK

- Construit avec le microframework Flask
- Utilise la base de données TinyDB
- Utilise la bibliothèque d'analyse syntaxique de documents HTML BeautifulSoup

## Run :

<code>
FLASK_APP = "main.py"
  
flask run
</code>

## Endpoints :

HTTP method : POST

/create?url= : Create a text

/delete?id_url= : Delete a text

/read?id_url= : Read a single text

/real_all : Read all texts

/delete_all : Delete all texts

