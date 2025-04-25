import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='Offices',
                                         user='root',
                                         password='.')
    print(connection)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        query = ("SELECT meetid, date, slot FROM Meetings")
        cursor.execute(query)

        for (first, second, third) in cursor:
            print(first, second, third)
     


except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.commit()
        print("MySQL changes are commited")
        connection.close()
        print("MySQL connection is closed")
