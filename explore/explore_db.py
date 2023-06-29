import uuid
from database.database import  data_base

class ExploreDatabase:

    table_name = "questions"
    key = ["topicId", "topic", "question", "url", "level", "platform"]

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.data_base_obj = data_base(connection)
        
    def getRemarks(self):
        lis = []
        rows = self.data_base_obj.selectFromTable("*", self.table_name)
        for row in rows:
            json = {}
            for col in range(len(row)):
                json[self.key[col]] = row[col]
            lis.append(json)
            json = {}
        return lis

    def addQuestionToTable(self, url,topic, question, level, platform):
        topic_id = uuid.uuid1().hex
        print( url,topic, question, level, platform)
        res = self.data_base_obj.insertIntoTable(self.table_name, "(?,?,?,?,?,?)",(url,topic_id, topic, question, level, platform))
        return res

if __name__ == "__main__":
    pass