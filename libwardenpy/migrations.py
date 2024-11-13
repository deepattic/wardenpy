import os
import sqlite3


def migrate_DB():
    filenames = next(os.walk("migrations/"))[2]
    for file in filenames:
        with open(f'migrations/{file}', 'r') as file:
            query = file.read()
            try:
                with sqlite3.connect('db.sqlite3') as con:
                    con.execute(query)

            # TODO: make this sqlite3.Error type later
            except sqlite3.Error as err:
                print(f"Some thing is worng with the migration query?\nError -> {err}")
