import json
from database.database import Database, Note

db = Database('./database/banco_get-it')

def extract_route(request):
    if request != "":
        return request.split(" ")[1][1:]
    return ""

def read_file(path):
    arquivo = open(path, mode = "r+b").read()
    return arquivo

def load_data():
    notes = db.get_all()
    return notes

def load_template(template):
    arquivo = open("templates/" + template, mode = "r", encoding="utf-8").read()
    return arquivo

def update_notes(params):
    db.add(Note(title=f'{params["titulo"]}', content=f'{params["detalhes"]}'))
    notes = load_data()
    return notes

def build_response(body='', code=200, reason='OK', headers=''):
    if headers != '':
        return f"HTTP/1.1 {code} {reason}\n{headers}\n\n{body}".encode()
    return f"HTTP/1.1 {code} {reason}\n\n{body}".encode()