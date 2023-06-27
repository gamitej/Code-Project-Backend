import sqlite3


def connect_to_db():
    connection = sqlite3.connect('data.db')
    return connection


def execute_query(query):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()


def selectQuery(query, fetchOne=True):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query)
    if fetchOne:
        res = cursor.fetchone()
    else:
        res = cursor.fetchall()
    connection.close()
    return res


def selectFromTable(col, table_name):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = f"select {col} from {table_name}"
    result = cursor.execute(query)
    row = result.fetchall()
    connection.close()
    return row


def insertIntoTable(table_name, total_values, values):
    connection = connect_to_db()
    cursor = connection.cursor()
    insert_query = f"INSERT OR IGNORE INTO {table_name} VALUES{total_values}"
    cursor.execute(insert_query, values)
    connection.commit()
    connection.close()


def updateTable(table_name, rows_to_update, where_cond, values):
    connection = connect_to_db()
    cursor = connection.cursor()
    update_query = f"UPDATE {table_name} SET {rows_to_update} where {where_cond}"
    cursor.execute(update_query, values)
    connection.commit()
    connection.close()


def deleteRowFromTable(table_name, id):
    connection = connect_to_db()
    cursor = connection.cursor()
    del_query = f"DELETE from {table_name} where id = '{id}'"
    cursor.execute(del_query)
    connection.commit()
    connection.close()
