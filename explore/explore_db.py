import uuid
from database.database import  data_base

class ExploreDatabase:

    table_name = "questions"
    key = ["topicId", "topic", "question", "url", "level", "platform"]

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.data_base_obj = data_base(connection)
        
    def selectedTopicUserData(self,user_id, topic):
        query = f"SELECT q.url, q.question_id, q.topic, q.question,q.level,q.platform, uq.mark_date, CASE WHEN uq.user_id IS NOT NULL THEN TRUE ELSE FALSE END AS completed FROM questions q LEFT JOIN user_questions uq ON q.question_id = uq.question_id AND uq.user_id = '{user_id}' WHERE uq.user_id = '{user_id}' OR uq.user_id IS NULL AND topic = '{topic}' " 
        data = self.data_base_obj.selectQuery(query,False)
        easy,medium,hard = [],[],[] 
        for row in data:
            url,que_id,topic,que_name,level,platform,completed  = row[0],row[1],row[2],row[3],row[4],row[5],row[7]
            if level == "easy":
                json = {"id":que_id,"name":que_name,"completed": 1 == completed,"platform":platform,"url":url}
                easy.append(json)
            elif level == "medium":
                json = {"id":que_id,"name":que_name,"completed": 1 == completed,"platform":platform,"url":url}
                medium.append(json)
            elif level == "hard":
                json = {"id":que_id,"name":que_name,"completed": 1 == completed,"platform":platform,"url":url}
                hard.append(json)
        easyJson = {"cardTitle":"Easy","cardType":"easy","body":easy}
        mediumJson = {"cardTitle":"Medium","cardType":"medium","body":medium}
        hardJson = {"cardTitle":"Hard","cardType":"hard","body":hard}
        return [easyJson, mediumJson, hardJson]

    def addQuestionToTable(self, url,topic, question, level, platform):
        question_id = uuid.uuid1().hex
        res = self.data_base_obj.insertIntoTable(self.table_name, "(?,?,?,?,?,?)",(url,question_id, topic, question, level, platform))
        return res

if __name__ == "__main__":
    pass