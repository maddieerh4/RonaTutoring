import sqlite3

conn = sqlite3.connect("ronatutoring.sqlite")

c = conn.cursor()

c.execute("""CREATE TABLE pending_requests (id INTEGER PRIMARY KEY AUTOINCREMENT, userType VARCHAR(10), 
            lastName VARCHAR(1000), firstName VARCHAR(1000), location VARCHAR(1000), age INTEGER,
            grade INTEGER, availability VARCHAR(4000), marketingSource VARCHAR(1000), 
            studentContact VARCHAR(400), parentContact VARCHAR(400), 
            math INTEGER, science INTEGER, english INTEGER, history INTEGER, compsci INTEGER, otherSubj VARCHAR(1000),
            specificClass VARCHAR(4000), additional VARCHAR(4000))""")

conn.commit()
conn.close()