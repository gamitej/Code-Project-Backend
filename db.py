from app import connection

class data_base():
    def __init__(self):
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


    def insertIntoTable(self,table_name, total_values, values):
        cursor = self.connection.cursor()
        insert_query = f"INSERT OR IGNORE INTO {table_name} VALUES{total_values}"
        cursor.execute(insert_query, values)
        self.connection.commit()


    def updateTable(self,table_name, rows_to_update, where_cond, values):
        cursor = self.connection.cursor()
        update_query = f"UPDATE {table_name} SET {rows_to_update} where {where_cond}"
        cursor.execute(update_query, values)
        self.connection.commit()


    def deleteRowFromTable(self,table_name, id):
        cursor = self.connection.cursor()
        del_query = f"DELETE from {table_name} where id = '{id}'"
        cursor.execute(del_query)
        self.connection.commit()


if __name__=='__main__':
    pass
    data_base(x)