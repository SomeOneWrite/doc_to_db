import re
import sqlite3

from docx import Document

db_name = 'main.odb'

conn = sqlite3.connect(db_name)

query = conn.cursor()

documents = [
    '1.docx'
]


class ParserData:

    def get_last_insert_id(self, table_name):
        last_id = self.query.execute('select seq from sqlite_sequence where name="' + table_name + '"')
        return last_id.fetchone()[0]

    def __init__(self, query):
        self.query = query
        pass

    def check_material_key(self, cells):
        cell = cells[0]
        result = re.search(r'(\d\d\d-\d\d\d\d)', cell.text)
        if result:
            print(result.group(1))
            return result.group(1)
        return None

    def check_machines_key(self, cells):
        cell = cells[0]
        result = re.search(r'(\d\d\d\d\d\d)', cell.text)
        if result:
            print(result.group(1))
            return result.group(1)
        return None

    def parse_machines(self, rows):
        for row in rows:
            try:
                if not row.cells:
                    continue
                if len(row.cells) < 2:
                    continue
            except Exception as e:
                continue
            self.check_machines_key(row.cells)

    def parse_materials(self, rows):
        for row in rows:
            try:
                if not row.cells:
                    continue
                if len(row.cells) < 2:
                    continue
            except Exception as e:
                continue
            self.check_material_key(row.cells)

    def parse_table(self, table):
        rows = table.rows
        self.parse_materials(rows)
        self.parse_machines(rows)

    def parse_file(self, filename):
        doc = Document(filename)
        self.filename = filename
        tables = doc.tables
        print('Всего таблиц: ' + str(len(tables)))
        for table in range(0, len(tables)):
            self.parse_table(tables[table])


for file in documents:
    ParserData(query).parse_file(file)
