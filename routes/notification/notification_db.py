from routes.database.database import data_base

class NotificationDb:
    table_name = "users"
    key = ["id", "username", "password"]

    def __init__(self,connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.data_base_obj = data_base(connection)

    def getNotificationOfUser(self,id):
        query = f"SELECT n.notification_id, n.content,CASE WHEN un.user_id IS NULL THEN FALSE ELSE TRUE END AS seen FROM notifications n LEFT JOIN user_notification un ON n.notification_id = un.notification_id AND un.user_id = '{id}' order by n.timestamp desc"

        data = self.data_base_obj.selectQuery(query,False)
        jsonData = []
        if data !=[]:
            for row in data:
                id,text,seen = row[0],row[1],row[2]
                json = {"id":id, "text":text, "seen":seen}
                jsonData.append(json)
        return jsonData
    
    def markNotificationsUser(self,id,req):
        for row in req:
            notif_id = row['id']
            query = f"insert into user_notification (user_id,notification_id,seen) values ('{id}','{notif_id}','true')"
            self.data_base_obj.insertIntoTable(query)

    

if __name__=='__main__':
    pass