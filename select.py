import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()


def select_db_info():
    cursor.execute("""SELECT distinct(user_name), sum(message) FROM pack_counter
                              WHERE user_name is not null
                              AND date(datetime) = date('now') 
                              GROUP BY user_name
                              ORDER BY message ASC""")
    result = cursor.fetchall()
    gg= " ".join(str(x) for x in result)
    return(gg)

def delete():
    cursor.execute("""delete from pack_counter""")
    result = cursor.fetchall()

    conn.commit()





delete()