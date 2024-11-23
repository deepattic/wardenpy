import os

from libwardenpy.db import get_connection


# all this funtion does is create and init the sqlite3 database
# it read the SQL files in the migration directory and run them against the db
def migrate_DB():
    filenames = next(os.walk("migrations/"))[2]
    for file in filenames:
        with open(f"migrations/{file}", "r") as file:
            query = file.read()

            try:
                with get_connection() as conn:
                    conn.execute(query)

            except Exception as err:
                print(f"Some thing is worng with the migration query?\nError -> {err}")
