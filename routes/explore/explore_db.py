import uuid
from routes.database.database import  data_base
from routes.profile.profile_data import ProfileDataDropdown

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
        query = f"SELECT q.topic, COUNT(q.question_id) AS total_questions, COUNT(uq.question_id) AS questions_done FROM questions q LEFT JOIN user_questions uq ON q.question_id = uq.question_id AND uq.user_id = '{user_id}' GROUP BY q.topic order by q.topic;"
        data = self.data_base_obj.selectQuery(query,False)
        finalJson = []
        for row in data:
            topic,total_questions,questions_done = row[0],row[1],row[2]
            if topic in topicMap:
                json = {"title":topicMap[topic],"total":total_questions,"solved":questions_done,"urlTitle":topic}
                finalJson.append(json)        
        return finalJson
        
    def selectedTopicUserData(self,user_id, topic):
        query = f"SELECT q.url, q.question_id, q.topic, q.question,q.level,q.platform, uq.mark_date, CASE WHEN uq.user_id IS NOT NULL THEN TRUE ELSE FALSE END AS completed FROM questions q LEFT JOIN user_questions uq ON q.question_id = uq.question_id AND uq.user_id = '{user_id}' WHERE (uq.user_id = '{user_id}' OR uq.user_id IS NULL) AND q.topic ='{topic}' order by q.question" 
        data = self.data_base_obj.selectQuery(query,False)
        easy,medium,hard = [],[],[] 
        for row in data:
            url,que_id,topic,que_name,level,platform,completed  = row[0],row[1],row[2],row[3].strip(),row[4],row[5],row[7]
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
        query = f"insert into questions (url,question_id, topic, question, level, platform) values ('{url}','{question_id}','{topic}','{question.strip()}','{level}','{platform}')"
        res = self.data_base_obj.insertIntoTable(query)
        return res

if __name__ == "__main__":
    pass