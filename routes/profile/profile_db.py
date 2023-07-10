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
            easyTotal,easySolved,mediumTotal,mediumSolved,hardTotal,hardSolved = 0,0,0,0,0,0
            for i in range(len(data)):
                if totalData[i][0] == "easy":
                    easyTotal = totalData[i][1]
                if data[i][0] == "easy":
                    easySolved = data[i][1]
                if totalData[i][0] == "medium":
                    mediumTotal = totalData[i][1]
                if data[i][0] == "medium":
                    mediumSolved = data[i][1]
                if totalData[i][0] == "hard":
                    hardTotal = totalData[i][1]
                if data[i][0] == "hard":
                    hardSolved = data[i][1]

            total = totalData[0][1] + totalData[1][1] + totalData[2][1]
            totalSolved  = data[0][1] + data[1][1] + data[2][1] 
            json = {"easyTotal":easyTotal,"easySolved":easySolved,"mediumTotal":mediumTotal,"mediumSolved":mediumSolved,"hardTotal":hardTotal,"hardSolved":hardSolved,"total":total,"totalSolved":totalSolved}
        return json


if __name__ == '__main__':
    pass
        
