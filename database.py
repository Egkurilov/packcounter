import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()



cursor.execute("""CREATE TABLE IF NOT EXISTS pack_counter
                  (datetime NUMERIC, message text, chat_id text, user_name text)
               """)


