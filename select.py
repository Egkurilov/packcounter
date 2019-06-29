import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()


for row in cursor.execute("SELECT sum(message), user_name FROM pack_counter"):
    print(row)
   #conn.close()