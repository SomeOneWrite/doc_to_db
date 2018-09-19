import os
import sqlite3

from doc_parse import MainParser
from ParserData import ParserData

db_name = 'minstroy_old.140.odb'

if os.path.exists(db_name):
    pass  # os.remove(db_name)
conn = sqlite3.connect(db_name)

query = conn.cursor()

query_create_tables = [
    'CREATE TABLE dirs ( id integer primary key autoincrement, parent_id integer references dirs(id) on delete cascade on update cascade, name text )',
    'CREATE TABLE collections ( id integer primary key autoincrement, dir_id integer references dirs(id) on delete cascade on update cascade, type integer not null, name text, techpart text )',
    'CREATE TABLE captions ( id integer primary key autoincrement, collection_id integer not null references collections(id) on delete cascade on update cascade, parent_id integer references captions(id) on delete cascade on update cascade, name text )',
    'CREATE TABLE unit_positions ( id text not null, name text, unit text, cost_workers real, cost_machines real, cost_drivers real, cost_materials real, mass real, caption_id integer not null references captions(id) on delete cascade on update cascade )',
    'CREATE TABLE options ( name text not null, val text, primary key(name) )',
    # 'CREATE TABLE materials ( id text not null, name text, unit text, price real, price_vacantion real, caption_id integer references captions(id) on delete set null on update cascade, primary key(id) )',
    'CREATE TABLE machines ( id text not null, name text, unit text, price real, price_driver real, caption_id integer references captions(id) on delete set null on update cascade, primary key(id) )',
    'CREATE TABLE transports ( id text not null, name text, unit text, price real, type integer check(type >= 1 and type <= 4), caption_id integer references captions(id) on delete set null on update cascade, primary key(id) )',
    'CREATE TABLE workers ( id text not null, name text, unit text, price real, caption_id integer references captions(id) on delete set null on update cascade, primary key(id) )',
]

for query_create in query_create_tables:
    try:
        query.execute(query_create)
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()

root_dir = "C:\\users\\rinat\\test"


def get_last_insert_id(table_name):
    last_id = query.execute('select seq from sqlite_sequence where name="' + table_name + '"')
    return last_id.fetchone()[0]

def insert_dir(parent_id, file_name):
    query.execute('insert into dirs(parent_id, name) values(?, ?)', (parent_id, file_name))


def build_file(dir_id, root, file_name):
    query.execute('insert into collections(dir_id, type, name, techpart) values(?, ?, ?, ?)',
                  (dir_id, '2', file_name[:-5], 'techpart'))
    collection_id = get_last_insert_id('collections')
    print('Обработка файла ' + file_name)
    ParserData(conn).parse_file(query, os.path.join(root, file_name), collection_id)
    conn.commit()

def build_data(dir_id, root, file_name):
    query.execute('insert into collections(dir_id, type, name, techpart) values(?, ?, ?, ?)', (dir_id, '2',  file_name[:-5], 'techpart'))
    collection_id = get_last_insert_id('collections')
    print('Обработка файла материалов' + file_name)
    ParserData(conn).parse_file(os.path.join(root, file_name), collection_id)
    conn.commit()


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
            build_file(parent_id, root, file)

build_dir(root_dir)

conn.commit()
conn.close()
