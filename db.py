import sqlite3

con = sqlite3.connect('station.db')

cur = con.cursor()

cur.execute("""DROP TABLE IF EXISTS measurements;""")
cur.execute("""CREATE TABLE measurements(
id INTEGER PRIMARY KEY AUTOINCREMENT,
temperature float DEFAULT 0,
humidity float DEFAULT 0,
pressure float DEFAULT 0,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);""")

for i in range(20):
    cur.execute("""INSERT INTO measurements (id, temperature, humidity, pressure) VALUES (1, 1, 1, 1);""")
    con.commit()

for row in cur.execute("SELECT * FROM measurements;"):
    print(row)
    
con.close()