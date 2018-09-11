import re
import sqlite3

from docx import Document

from ParseMaterials import ParseMaterials
from ParseMachines import ParseMachines
from ParseWorkers import ParseWorkers

db_name = 'main.odb'

conn = sqlite3.connect(db_name)

query = conn.cursor()

documents = [
    # 'costs/doc/workers/2.docx',
    #     # 'costs/doc/workers/3.docx',
    #     # 'costs/doc/workers/4.docx',
    #     # 'costs/doc/workers/5.docx',
    'costs/doc/workers/main.docx',

    # '2.docx',
    # '3.docx',
    # '4.docx',
    # '5.docx',
    # '6.docx'
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
            try:
                if len(row.cells) < 2:
                    continue
            except Exception as e:
                continue
            # ParseMaterials(query).run(row)
            # ParseMachines(query).run(row)


    def parse_file(self, filename):
        doc = Document(filename)
        self.filename = filename
        tables = doc.tables
        print('Всего таблиц: ' + str(len(tables)))
        for table in range(0, len(tables)):
            if not table % 10:
                print('Process {} table of {}'.format(table, len(tables)) )
            self.parse_table(tables[table])
            ParseWorkers(query, filename.split('/')[3]).run(tables[table])


for file in documents:
    print('Parse file with name: {}'.format(file))
    ParserData(query).parse_file(file)

conn.commit()
