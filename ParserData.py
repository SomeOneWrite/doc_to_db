import sqlite3

from docx import Document

db_name = 'main.odb'

conn = sqlite3.connect(db_name)

query = conn.cursor()

documents = [
    ''
]


class ParserData:

    def get_last_insert_id(self, table_name):
        last_id = self.query.execute('select seq from sqlite_sequence where name="' + table_name + '"')
        return last_id.fetchone()[0]

    def __init__(self, query):
        self.query = query
        pass

    def parse_table(self, table):
        rows = table.rows
        for row in rows:
            pass

    def parse_file(self, filename):
        doc = Document(filename)
        self.filename = filename
        tables = doc.tables
        print('Всего таблиц: ' + str(len(tables)))
        for table in tables:
            self.parse_table(table)
