import uuid
import sqlite3
from db import selectFromTable, insertIntoTable

key = ["id", "username", "password"]

table_name = "users"


def connect_to_db():
    connection = sqlite3.connect('data.db')
    return connection


def checkUserValidity(user, passwd):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM {table_name} WHERE username = '{user}' AND password = '{passwd}'")
    result = cursor.fetchone()
    connection.close()
    print(result, "h")
    if result is None:
        return False
    else:
        return True


def getUsers(username):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = f"select * from {table_name} where username = ?"
    result = cursor.execute(query, (username,))
    row = result.fetchone()
    connection.close()
    return row


def insertUser(username, password):
    id = uuid.uuid1().hex
    res = insertIntoTable(table_name, "(?,?,?)", (id, username, password))
    return res
