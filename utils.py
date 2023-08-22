import json

def extract_route(request):
    rota = request.split(" ")[1][1:]
    return rota

def read_file(path):
    arquivo = open(path, mode = "r+b").read()
    return arquivo

def load_data(data):
    arquivo = json.loads(read_file("data/" + data))
    return arquivo

def load_template(template):
    arquivo = open("templates/" + template, mode = "r").read()
    return arquivo

def update_notes(params):
    notes = load_data("notes.json")
    notes.append(params)
    arquivo = open("data/notes.json", mode = "w").write(json.dumps(notes))
    return arquivo

def build_response(body='', code=200, reason='OK', headers=''):
    if headers != '':
        return f"HTTP/1.1 {code} {reason}\n{headers}\n\n{body}".encode()
    return f"HTTP/1.1 {code} {reason}\n\n{body}".encode()