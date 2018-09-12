import sqlite3

start_odb = 'omsk_550.odb'
new_odb = 'omsk.odb'

conn = sqlite3.connect(start_odb)
conn_2 = sqlite3.connect(new_odb)

query = conn.cursor()
query_2 = conn_2.cursor()

res = query.execute('select * from machines').fetchall()
for q in res:
    arg = [q[1], q[2], q[3], q[4], q[0]]
    result = query_2.execute('update machines set name = ?, unit = ?, price = ?, price_driver = ? where id = ?', arg)
res = query.execute('select * from materials').fetchall()
for q in res:
    arg = [q[1], q[2], q[3], q[4], q[0]]
    result = query_2.execute('update materials set name = ?, unit = ?, price = ?, price_vacantion = ? where id = ?',
                             arg)
conn_2.commit()

print(res)
