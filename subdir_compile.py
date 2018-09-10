import os
import sqlite3

from doc_parse import Parser

conn = sqlite3.connect('result.sqlite')

query = conn.cursor()

query_create_tables = [
    'CREATE TABLE dirs ( id integer primary key autoincrement, parent_id integer references dirs(id) on delete cascade on update cascade, name text )',
    'CREATE TABLE collections ( id integer primary key autoincrement, dir_id integer references dirs(id) on delete cascade on update cascade, type integer not null, name text, techpart text )',
    'CREATE TABLE captions ( id integer primary key autoincrement, collection_id integer not null references collections(id) on delete cascade on update cascade, parent_id integer references captions(id) on delete cascade on update cascade, name text )',
    'CREATE TABLE unit_positions ( id text not null, name text, unit text, cost_workers real, cost_machines real, cost_drivers real, cost_materials real, mass real, caption_id integer not null references captions(id) on delete cascade on update cascade )'
]

for query_create in query_create_tables:
    try:
        query.execute(query_create)
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()

root_dir = "C:\\users\\anonim\\test"

dirs = list()


def get_last_insert_id(table_name):
    last_id = query.execute('select seq from sqlite_sequence where name="' + table_name + '"')
    return last_id.fetchone()[0]

def insert_dir(parent_id, file_name):
    query.execute('insert into dirs(parent_id, name) values(?, ?)', (parent_id, file_name))


def build_file(dir_id, file_name):
    query.execute('insert into collections(dir_id, type, name, techpart) values(?, ?, ?, ?)', (dir_id, '2',  file_name[:-5], 'techpart'))
    collection_id = get_last_insert_id('collections')
    Parser(conn).parse_file(query, file_name, collection_id)


def build_dir(root, parent_id=None):
    for file in os.listdir(root):
        if os.path.isdir(os.path.join(root, file)):
            insert_dir(parent_id, file)
            last_parent_id = parent_id
            parent_id = get_last_insert_id('dirs')
            build_dir(os.path.join(root, file), parent_id)
            parent_id = last_parent_id
            continue
        if file.endswith(".docx"):
            if file.startswith('~'): continue
            build_file(parent_id, os.path.join(root, file))


build_dir(root_dir)

conn.commit()
conn.close()
