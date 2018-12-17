import sqlite3 as lite


def initialize_db(db_name_arg):
    try:
        conn0 = lite.connect(db_name_arg)
        c0 = conn0.cursor()
        c0.execute('''CREATE TABLE IF NOT EXISTS users(employee_id INTEGER PRIMARY KEY, username TEXT NOT NULL, 
						name TEXT NOT NULL, password TEXT NOT NULL );''')
        conn0.commit()
    except lite.Error as e:
        conn0.rollback()
        app.logger.error("An error occurred : " + e.args[0])
    finally:
        conn0.close()
