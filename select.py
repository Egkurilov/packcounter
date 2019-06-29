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
    return result


def message_formatter(sql_resut):
    for x, y in sql_resut:
        json = '''%s, %s''' % (x, y)
        print(json)

message_formatter(select_db_info())