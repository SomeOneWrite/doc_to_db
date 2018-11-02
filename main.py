import sqlite3
import json

# con = sqlite3.connect("minstroy_old.sqlite")
#
# query = con.cursor()
#
# count = 0
#
# result = query.execute("select * from unit_positions").fetchall()
# for r in result:
#     last_id = r[0]
#     str_ = r[0].replace("m","м")
#     str_ = str_.replace("M", "М")
#     query.execute("update unit_positions set id = ? where id = ?", [str_, r[0]])
#     count += 1
#     print(count)
#
# con.commit()

# result = query.execute("select * from materials").fetchall()
#
# data = list()
#
# for res in result:
#     c = 0
#     record = dict()
#     for col in res:
#
#         record[c] = col
#
#         c += 1
#     data.append(record)
#
# json.dump(data, open("data.json", 'w', encoding="utf-8"), indent=4, ensure_ascii=False)


conn = sqlite3.connect('minstroy_old.odb')
conn_2017 = sqlite3.connect('minstroy.odb')
res_con = sqlite3.connect('result.sqlite')

query = conn.cursor()
query7 = conn_2017.cursor()
res_query = res_con.cursor()

tables = [
    'materials',
    'machines',
    'transports',
    'workers'
]

is_all = False

for table in tables:
    res = query.execute("select * from {}".format(table)).fetchall()
    res_7 = query7.execute("select * from {}".format(table)).fetchall()
    res_query.execute(
        "create table if not exists {}(id1 text not null primary key, id2 text not null, name text, price real, price_driver real)".format(
            table))
    for r in res:
        for r7 in res_7:
            ls = r[1].split(' ')
            if r[1] == r7[1] or r[0] == r7[0]:
                try:
                    res_query.execute("insert into {} (id1, id2, name) values(?, ?, ?)".format(table),
                                      [r[0], r7[0], r[1]])
                except:
                    a = 2
                res_con.commit()
                print("Finded {} | {} ".format(r[1], r7[1]))
                is_all = True
                break
        if is_all:
            is_all = False
        else:
            res_query.execute("insert into {} (id1, id2, name) values(?, ?, ?)".format(table), [r[0], 0, r[1]])
