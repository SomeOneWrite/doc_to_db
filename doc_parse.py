from docx import Document
import sqlite3
from check_reg import get_unit, get_otdel, get_podrazdel, get_razdel, get_table_name, check_id

unit_position = list()


class MainParser:
    def __init__(self, query):
        self.query = query
        self.collection_id = 1
        self.filename = ''
        self.old_unit_str = ''
        self.last_razdel_id = 0
        self.last_podrazdel_id = 0
        self.last_otdel_id = 0
        self.parent_id = None
        self.last_razdel_id = None
        self.last_otdel_id = None
        self.last_inserted = None

    def get_last_insert_id(self, table_name):
        last_id = self.query.execute('select seq from sqlite_sequence where name="' + table_name + '"')
        return last_id.fetchone()[0]

    def parse_table(self, table):
        rows = table.rows
        for row in rows:
            if not row.cells: continue
            if len(row.cells) < 8: continue
            table_name = get_table_name(row.cells[0].text)
            otdel_str = get_otdel(row.cells[0].text)
            razdel_str = get_razdel(row.cells[0].text)

            podrazdel_str = get_podrazdel(row.cells[0].text)
            unit_str = get_unit(row.cells[0].text)

            if otdel_str:
                self.query.execute('insert into captions (collection_id, parent_id, name) values(?, ?, ?)',
                                   (self.collection_id, None, otdel_str))
                self.parent_id = self.get_last_insert_id('captions')
                self.last_otdel_id = self.parent_id
                self.last_inserted = 1
            if razdel_str:
                self.query.execute('insert into captions (collection_id, parent_id, name) values(?, ?, ?)',
                                   (self.collection_id, self.last_otdel_id, razdel_str))
                self.parent_id = self.get_last_insert_id('captions')
                self.last_razdel_id = self.parent_id
                self.last_inserted = 2
            if podrazdel_str:
                self.query.execute('insert into captions (collection_id, parent_id, name) values(?, ?, ?)',
                                   (self.collection_id, self.last_razdel_id, podrazdel_str))
                self.parent_id = self.get_last_insert_id('captions')
                self.last_inserted = 3
            if table_name:
                self.query.execute('insert into captions (collection_id, parent_id, name) values(?, ?, ?)',
                                   (self.collection_id, self.parent_id, table_name))
                self.last_inserted = 4
            name_str = row.cells[0].text
            cells = row.cells
            if check_id(cells[0].text):
                try:
                    self.query.execute(
                        'insert into unit_positions values(:id, :name, :unit, :cost_workers, :cost_machines, :cost_drivers, :cost_materials, :mass, :caption_id)',
                        {
                            'id': ''.join(cells[0].text.split()),
                            'name': name_str + cells[1].text,
                            'unit': unit_str,
                            'cost_workers': cells[3].text,
                            'cost_machines': cells[4].text,
                            'cost_drivers': cells[5].text,
                            'cost_materials': cells[6].text,
                            'mass': '',
                            'caption_id': self.get_last_insert_id('captions'),
                        })
                except sqlite3.DatabaseError as e:
                    pass

    def parse_file(self, conn, filename, collection_id):
        doc = Document(filename)
        self.filename = filename
        self.collection_id = collection_id
        tables = doc.tables
        print('Всего таблиц: ' + str(len(tables)))
        for table in tables:
            self.parse_table(table)
