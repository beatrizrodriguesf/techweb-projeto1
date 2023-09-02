import sqlite3
from dataclasses import dataclass

class Database:

    def __init__(self, nome_banco) -> None:
        self.conn = sqlite3.connect(nome_banco + ".db")
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title STRING, content STRING NOT NULL)")

    def add(self, note):
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO note (title,content) VALUES ('{note.title}','{note.content}')")
        self.conn.commit()

    def get_all(self):
        lista_notes = []
        cursor = self.conn.execute("SELECT id, title, content FROM note")
        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]
            new_note = Note(id, title, content)
            lista_notes.append(new_note)
        return lista_notes
    
    def update(self, entry):
        cur = self.conn.cursor()
        cur.execute(f"UPDATE note SET title = '{entry.title}', content = '{entry.content}' WHERE id = {entry.id}")
        self.conn.commit()

    def get_note(self, id):
        cursor = self.conn.execute(f"SELECT title, content FROM note WHERE id = {id}")
        linha = cursor.fetchone()
        return Note(id, linha[0], linha[1])

    def delete(self, note_id):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM note WHERE id = {note_id}")
        self.conn.commit()

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''