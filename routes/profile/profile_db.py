from routes.database.database import data_base

class ProfileDatabase:
    def __init__(self,connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.data_base_object = data_base(connection)

    def calcUserStatus(self,res,id):
        query = f"SELECT q.level, COUNT(DISTINCT uq.question_id) AS total_solved_questions FROM questions q LEFT JOIN user_questions uq ON q.question_id = uq.question_id WHERE uq.user_id = '{id}' or uq.user_id IS NULL GROUP BY q.level"
        data  = self.data_base_object.selectQuery(query,False)
        


if __name__ == '__main__':
    pass
        
