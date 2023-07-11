
class data_base:
    def __init__(self,connection):
        self.connection = connection

    def execute_query(self,query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def selectQuery(self,query, fetchOne=True):
        cursor = self.connection.cursor()
        cursor.execute(query)
        if fetchOne:
            res = cursor.fetchone()
        else:
            res = cursor.fetchall()
        return res

    def selectFromTable(self,col, table_name):
        cursor = self.connection.cursor()
        query = f"select {col} from {table_name}"
        result = cursor.execute(query)
        row = result.fetchall()
        return row

    def insertIntoTable(self,insert_query):
        cursor = self.connection.cursor()
        print(insert_query)
        cursor.execute(insert_query)
        self.connection.commit()


if __name__=='__main__':
    pass