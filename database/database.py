import sqlite3
from dataclasses import dataclass

class Database:

    def __init__(self, nome_banco) -> None:
        self.conn = sqlite3.connect(nome_banco + ".db")
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, category STRING, title STRING, content STRING NOT NULL)")

    def add(self, note):
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO note (category,title,content) VALUES ('{note.category}','{note.title}','{note.content}')")
        self.conn.commit()

    def get_all(self):
        lista_notes = []
        cursor = self.conn.execute("SELECT id, category, title, content FROM note")
        for linha in cursor:
            id = linha[0]
            category = linha[1]
            title = linha[2]
            content = linha[3]
            new_note = Note(id, category, title, content)
            lista_notes.append(new_note)
        return lista_notes
    
    def update(self, entry):
        cur = self.conn.cursor()
        cur.execute(f"UPDATE note SET category = '{entry.category}', title = '{entry.title}', content = '{entry.content}' WHERE id = {entry.id}")
        self.conn.commit()

    def get_note(self, id):
        cursor = self.conn.execute(f"SELECT category, title, content FROM note WHERE id = {id}")
        linha = cursor.fetchone()
        return Note(id, linha[0], linha[1], linha[2])

    def delete(self, note_id):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM note WHERE id = {note_id}")
        self.conn.commit()

@dataclass
class Note:
    id: int = None
    category: str = ''
    title: str = None
    content: str = ''