import uuid
from db import insertIntoTable, data_base
from app import connection


class AuthDb():
    key = ["id", "username", "password"]
    table_name = "users"

    def __init__(self,connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.data_base_obj = data_base()

    def checkUserValidity(self,user, passwd):
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE username = '{user}' AND password = '{passwd}'")
        result = self.cursor.fetchone()
        if result is None:
            return False
        else:
            return True

    def getUsers(self,username):
        query = f"select * from {self.table_name} where username = ?"
        result = self.cursor.execute(query, (username,))
        row = result.fetchone()
        return row

    def insertUser(self,username, password):
        id = uuid.uuid1().hex
        res = insertIntoTable(self.table_name, "(?,?,?)", (id, username, password))
        return res

if __name__ == "__main__":
    db = AuthDb(connection)