import mysql.connector
from mysql.connector import Error


def get_connection():
    """Return a MySQL connection to the pantrix database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          # ← Change to your MySQL username
            password="Rene@2007",          # ← Change to your MySQL password
            database="PANTRIX"
        )
        return conn
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None