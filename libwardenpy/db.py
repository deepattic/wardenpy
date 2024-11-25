import sqlite3
from contextlib import contextmanager


### This just create a sqlite connection to pass around the other functions
### https://stackoverflow.com/questions/67436362/decorator-for-sqlite3/67436763#67436763
@contextmanager
def get_connection(DB_PATH="data/db.sqlite3"):
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        raise e
    else:
        conn.commit()
    finally:
        conn.close()
