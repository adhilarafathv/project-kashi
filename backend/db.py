
import mysql.connector
from mysql.connector import Error


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql80",
            database="project_kashi"
        )
        return connection

    except Error as error:
        print(f"Database connection failed: {error}")
        return None
