import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# =========== CREATE USER TABLE ===============

create_user_table = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id text PRIMARY KEY,
            username text,
            password VARCHAR(25) NOT NULL
        )
        '''
cursor.execute(create_user_table)

# =========== CREATE QUESTIONS TABLE ===============

create_que_table = '''
        CREATE TABLE IF NOT EXISTS questions (
            topic_id text PRIMARY KEY,
            topic VARCHAR(25) NOT NULL,
            question text,
            url VARCHAR(25) NOT NULL,
            level VARCHAR(25) NOT NULL,
            platform VARCHAR(25) NOT NULL
        )
        '''
cursor.execute(create_que_table)

# =========== CREATE USER-QUESTIONS TABLE ===============

sqlQuery = '''
        CREATE TABLE IF NOT EXISTS user_questions (
            mark_date TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) PRIMARY KEY,
            user_id text,
            question_id text,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (question_id) REFERENCES quentions (question_id)
        )
        '''

cursor.execute(sqlQuery)

# =========== INSERT MANY ROWS ================

user_data = [
    ("1", "Amitej", "1234"),
]

insert_query = "INSERT OR IGNORE INTO users VALUES(?,?,?)"

cursor.executemany(insert_query, user_data)

connection.commit()
connection.close()
