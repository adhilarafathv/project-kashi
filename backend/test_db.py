
from db import get_db_connection

connection = get_db_connection()

if connection and connection.is_connected():
    print("Project KASHI database connected successfully!")

    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE(), VERSION()")
    print(cursor.fetchone())

    cursor.close()
    connection.close()
else:
    print("Could not connect to the database.")
