import uuid
from database.database import data_base

class AuthDb:
    table_name = "users"
    key = ["id", "username", "password"]

    def __init__(self,connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.data_base_obj = data_base(connection)

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
        res = self.data_base_obj.insertIntoTable(self.table_name, "(?,?,?)", (id, username, password))
        return res

if __name__=='__main__':
    pass