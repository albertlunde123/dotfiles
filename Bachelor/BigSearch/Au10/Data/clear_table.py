import sqlite3

def clear_table(db_path, table_name):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the SQL query to delete all rows from the table
    cursor.execute(f"DELETE FROM {table_name}")

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

# Example usage
clear_table('Au10.db', 'configurations')
clear_table('Au10.db', 'actual_points')

