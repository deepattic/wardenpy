import sqlite3

def create_sqlite_connection():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    return cursor

db = create_sqlite_connection()
