import sqlite3

conn = sqlite3.connect('db/data_base.db', check_same_thread=False)  # Connect DB.
cursor = conn.cursor()  # Create cursor for work with tables.


