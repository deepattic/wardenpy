import sqlite3
from contextlib import contextmanager


### This just create a sqlite connection to pass around the other functions
### https://stackoverflow.com/questions/67436362/decorator-for-sqlite3/67436763#67436763
@contextmanager
def get_connection(DB_PATH="data/db.sqlite3"):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            salt BLOB NOT NULL)
            """
        )
        conn.execute(
            """
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            site TEXT NOT NULL,
            encrypted_password BLOB NOT NULL,
            nonce BLOB NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username))
            """
        )
        yield conn

    except Exception as e:
        conn.rollback()
        raise e

    else:
        conn.commit()

    finally:
        conn.close()
