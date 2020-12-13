import sqlite3

conn = sqlite3.connect('ronatutoring.sqlite')
cur = conn.cursor()

cur.execute("SELECT * FROM pending_requests")

rows = cur.fetchall()

print(rows)

print('\n\n\n\n\n')

for row in rows:
    print(len(row))
    print(row)
    print('\n')

conn.close()