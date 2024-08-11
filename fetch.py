import sqlite3

conn = sqlite3.connect('customerData.db')

fethQuerry = """
select * from customerData
"""
cur = conn.cursor()
cur.execute(fethQuerry)
output = cur.fetchall()
i = 1
for row in output:
    print(i,' ',row)
    i += 1
cur.close()
conn.close()