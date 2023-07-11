import uuid
from routes.database.database import data_base

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
        query = f"select * from {self.table_name} where username = '{username}'"
        result = self.data_base_obj.selectQuery(query,True)
        return result

    def insertUser(self,username, password):
        id = uuid.uuid1().hex
        query = f"insert into users (user_id,username,password) values ('{id}','{username}','{password}')"
        res = self.data_base_obj.insertIntoTable(query)
        return res

if __name__=='__main__':
    pass