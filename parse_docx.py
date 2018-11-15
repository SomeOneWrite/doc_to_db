import os
import sqlite3

from docx import Document

from Model import SqlModel

conn = sqlite3.connect("result.sqlite")
query = conn.cursor()
query.execute(
    "create table if not exists materials(id text, name text, unit text, prefixMat text, prefixOKVD text)")
last_prefix = ''


def parse(table):
    for row in table.rows:
        global last_prefix
        cells = row.cells
        try:
            if cells[0].text == "":
                continue
            mat_id = cells[0].text.strip()
            if "часть" in mat_id.lower():
                last_prefix = cells[0].text
                print(last_prefix)
                continue

            name = cells[1].text.strip()
            unit = cells[2].text.strip()
            okvd_prefix = cells[0].text.strip()[0:5]
            query.execute("insert into materials (id, name, unit, prefixMat, prefixOKVD) values(?, ?, ?, ?, ?)",
                          [mat_id, name, unit, last_prefix, okvd_prefix])
        except:
            pass
        # model.insert_material(cells[0].text, cells[1].text, cells[2].text, 0, 0, 1)
        # print("id = {} name = {} unit = {}".format(cells[0].text, cells[1].text, cells[2].text))


for dirpath, dirnames, filenames in os.walk("mat"):
    for filename in [f for f in filenames if f.endswith(".docx") and not f.startswith("~")]:
        path = os.path.join(dirpath, filename)
        doc = Document(path)
        for table in doc.tables:
            parse(table)

conn.commit()
