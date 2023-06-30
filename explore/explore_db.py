import uuid
from database.database import  data_base
from profile.profile_data import ProfileDataDropdown

class ExploreDatabase:

    table_name = "questions"
    key = ["topicId", "topic", "question", "url", "level", "platform"]

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.data_base_obj = data_base(connection)
        self.profileObj = ProfileDataDropdown()
    
    def topicsInfoUser(self,user_id):
        topicMap = self.profileObj.getTopicMapping()
        query = f"SELECT q.topic, COUNT(q.question_id) AS total_questions, COUNT(uq.question_id) AS questions_done FROM questions q LEFT JOIN user_questions uq ON q.question_id = uq.question_id AND uq.user_id = '{user_id}' GROUP BY q.topic;"
        data = self.data_base_obj.selectQuery(query,False)
        finalJson = []
        for row in data:
            topic,total_questions,questions_done = row[0],row[1],row[2]
            if topic in topicMap:
                json = {"title":topicMap[topic],"total":total_questions,"solved":questions_done,"urlTitle":topic}
                finalJson.append(json)        
        return finalJson
        
    def selectedTopicUserData(self,user_id, topic):
        query = f"SELECT q.url, q.question_id, q.topic, q.question,q.level,q.platform, uq.mark_date, CASE WHEN uq.user_id IS NOT NULL THEN TRUE ELSE FALSE END AS completed FROM questions q LEFT JOIN user_questions uq ON q.question_id = uq.question_id AND uq.user_id = '{user_id}' WHERE (uq.user_id = '{user_id}' OR uq.user_id IS NULL) AND q.topic ='{topic}' " 
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