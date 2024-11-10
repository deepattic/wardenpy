import os
from db import db

filenames = next(os.walk("migrations/"))[2]
for file in filenames:
    with open(f'migrations/{file}','r') as file:
        query = file.read()
        try:
            db.execute(query)
        # TODO: make this sqlite3.Error type later
        except:
            print("Some thing is worng with the migration query?")
