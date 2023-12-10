import sqlite3

def show_database_content(db_path, table_name):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM " + table_name)
    rows = c.fetchall()

        # Print the rows
    # print("ID | Encoding | Energy")
    # print("------------------------")

    for row in rows:
        print(f"{row[0]} | {row[1]}")

    # Close the connection
    conn.close()

# Example usage
show_database_content('10Conf.db', 'actual_points')
