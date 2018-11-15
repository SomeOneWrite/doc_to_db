import sqlite3
from Helpers import without_whitespace

conn_min = sqlite3.connect("minstroy_old.odb")
conn_new = sqlite3.connect("minstroy.odb")
conn_result = sqlite3.connect("r.sqlite")

query_min = conn_min.cursor()
query_new = conn_new.cursor()
query_result = conn_result.cursor()

res_min = query_min.execute("select * from workers").fetchall()
res_new = query_new.execute("select * from workers").fetchall()
query_result.execute("create table if not exists workers(id1 text, id2 text, name text, unit text)")
# query_result.execute("create table if not exists workers(id1 text, id2 text, name text, unit text)")
# query_new.execute("create table if not exists machines(id text not null primary key, name text, unit text)")


res_new = list(res_new)
res_min = list(res_min)

count = 0

for rnew in res_new:
    count += 1
    print(count)
    # # query_new.execute("update materials set id = ? where id = ?", [without_whitespace(rnew[0]), rnew[0]])
    # if "маш" in rnew[2]:
    #     query_new.execute("delete from materials where id = ?", [rnew[0]])
    #     query_new.execute("insert into machines values(?, ?, ?)", [rnew[0], rnew[1], rnew[2]])
    #     continue
    #
    # continue
    finded = False
    for rmin in res_min:
        r1_str = rnew[1].lower().strip()
        r2_str = rmin[1].lower().strip()
        if r1_str == r2_str:
            count += 1
            query_result.execute("insert into workers (id1, id2, name, unit) values(?, ?, ?, ?)",
                                 [rnew[0], rmin[0], rmin[1], rmin[2]])
            finded = True
            print(count)
            break
    if not finded:
        query_result.execute("insert into workers (id1, id2, name, unit) values(?, ?, ?, ?)",
                             [rnew[0], 0, rnew[1], rnew[2]])
    finded = False
    conn_result.commit()

conn_result.commit()
conn_new.commit()
print(count)
