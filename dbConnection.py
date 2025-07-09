import mysql.connector

def get_db_connector():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="umsdc"
    )