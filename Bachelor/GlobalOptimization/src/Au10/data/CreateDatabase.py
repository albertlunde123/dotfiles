import sqlite3

# Create a SQLite database in memory (you can also specify a file path)
conn = sqlite3.connect("Au10.db")

# Create a table to store configurations and energies
# Each row will have an ID, configuration as a string, and energy as a float
create_table_query = """
CREATE TABLE IF NOT EXISTS configurations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    configuration TEXT NOT NULL UNIQUE,
    energy REAL NOT NULL
);
"""
conn.execute(create_table_query)

create_table_query = """
CREATE TABLE IF NOT EXISTS actual_points (
    points TEXT NOT NULL UNIQUE,
    energy REAL NOT NULL
);
"""
conn.execute(create_table_query)

conn.commit()
conn.close()
