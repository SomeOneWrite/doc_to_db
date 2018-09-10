from docx import Document
from check_reg import get_unit

unit_position = list()

class Parser:
    def __init__(self, query):
        self.query = query
        self.collection_id = 1
        self.filename = ''
        self.old_unit_str = ''

    def get_last_insert_id(self, table_name):
        last_id = self.query.execute('select seq from sqlite_sequence where name="' + table_name + '"')
        return last_id.fetchone()[0]

    def parse_table(self, table):
        rows = table.rows
        parent_id = None
        self.has_next = True
        for row in rows:
            unit_str, razdel_str, podrazdel_str = get_unit(row.cells[0].text)
            if not unit_str:
                unit_str = self.old_unit_str
                continue
            else:
                self.old_unit_str = unit_str
            if razdel_str:
                if not parent_id:
                    self.query.execute('insert into captions (collection_id, parent_id, name) values(?, ?, ?)',
                                       (self.collection_id, parent_id, razdel_str))
                parent_id = self.get_last_insert_id('captions')

            if podrazdel_str:
                parent_id = self.get_last_insert_id('captions')
                self.query.execute('insert into captions (collection_id, parent_id, name) values(?, ?, ?)',
                                   (self.collection_id, parent_id, podrazdel_str))
            if self.has_next:
                self.has_next = False
                continue
            self.has_next = True
            name_str = row.cells[0].text
            cells = row.cells
            if (cells[0].text == cells[1].text): continue
            self.query.execute('insert into unit_positions values(:id, :name, :unit, :cost_workers, :cost_machines, :cost_drivers, :cost_materials, :mass, :caption_id)',
                               {
                                   'id': cells[0].text,
                                   'name': name_str + cells[1].text,
                                   'unit': unit_str,
                                   'cost_workers': cells[3].text,
                                   'cost_machines': cells[4].text,
                                   'cost_drivers': cells[5].text,
                                   'cost_materials': cells[6].text,
                                   'mass': '',
                                   'caption_id': self.get_last_insert_id('captions'),
                               })


    def parse_file(self, conn, filename, collection_id):
        doc = Document(filename)
        self.filename = filename
        self.collection_id = collection_id
        tables = doc.tables
        for table in range(2, 10):
            self.parse_table(tables[table])




