from routes.database.database import data_base

class ProfileDatabase:
    def __init__(self,connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.data_base_object = data_base(connection)

    def calcUserStatus(self,totalData,id):
        query = f"SELECT q.level, COUNT(DISTINCT uq.question_id) AS total_solved_questions FROM questions q LEFT JOIN user_questions uq ON q.question_id = uq.question_id WHERE uq.user_id = '{id}' or uq.user_id IS NULL GROUP BY q.level"
        data  = self.data_base_object.selectQuery(query,False)

        json = {"easyTotal":0,"easySolved":0,"mediumTotal":0,"mediumSolved":0,"hardTotal":0,"hardSolved":0,"total":0,"totalSolved":0}
        if data is not None:
            total = totalData[0][1] + totalData[1][1] + totalData[2][1]
            totalSolved  = data[0][1] + data[1][1] + data[2][1] 
            json = {"easyTotal":totalData[0][1],"easySolved":data[0][1],"mediumTotal":totalData[1][1],"mediumSolved":data[1][1],"hardTotal":totalData[2][1],"hardSolved":data[2][1],"total":total,"totalSolved":totalSolved}
        return json


if __name__ == '__main__':
    pass
        
