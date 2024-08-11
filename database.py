import sqlite3

conn = sqlite3.connect('customerData.db')

tabelCreation = """
create table customerData(name varchar(20),email varchar(50),messege varchar(200))
"""

cur = conn.cursor()
cur.execute(tabelCreation)
print('table created successfully')
cur.close()
conn.close()