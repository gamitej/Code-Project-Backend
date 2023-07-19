import psycopg2

class data_base:
    def __init__(self,connection):
        self.connection = connection

    def execute_query(self,query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
        except (Exception,psycopg2.Error) as error:
            print(error)

    def selectQuery(self,query, fetchOne=True):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            if fetchOne:
                res = cursor.fetchone()
            else:
                res = cursor.fetchall()
            return res
        except (Exception,psycopg2.Error) as error:
            print(error)

    def selectFromTable(self,col, table_name):
        cursor = self.connection.cursor()
        query = f"select {col} from {table_name}"
        result = cursor.execute(query)
        row = result.fetchall()
        return row

    def insertIntoTable(self,insert_query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query)
            self.connection.commit()
        except (Exception,psycopg2.Error) as error:
            print(error)


if __name__=='__main__':
    pass