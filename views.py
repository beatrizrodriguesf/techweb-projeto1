from utils import load_data, load_template, update_notes, build_response
import urllib
from database.database import Database, Note

db = Database('./database/banco_get-it')

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            chave, valor = urllib.parse.unquote_plus(chave_valor).split("=")
            params[chave] = valor

        update_notes(params)
        
        return build_response(code = 303, reason = 'See other', headers = 'Location: /')
            
    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados.title, details=dados.content, id = dados.id)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)

    return build_response(body = load_template('index.html').format(notes=notes))

def delete(id):
    db.delete(id)
    return build_response(code = 303, reason = 'See other', headers = 'Location: /')

def update(request,id):
    note = db.get_note(id)

    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}

        for chave_valor in corpo.split('&'):
            chave, valor = urllib.parse.unquote_plus(chave_valor).split("=")
            params[chave] = valor

        edited_note = Note(title=params["titulo"], content=params["conteudo"], id=id)
        db.update(edited_note)

        return build_response(code = 303, reason = 'See other', headers = 'Location: /')

    return build_response(body = load_template('update.html').format(titulo = note.title, conteudo = note.content))