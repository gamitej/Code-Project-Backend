import uuid
from db import selectFromTable, insertIntoTable, deleteRowFromTable, updateTable

key = ["topicId", "topic", "question", "url", "level", "platform"]

table_name = "questions"


def getRemarks():
    lis = []
    rows = selectFromTable("*", table_name)
    for row in rows:
        json = {}
        for col in range(len(row)):
            json[key[col]] = row[col]
        lis.append(json)
        json = {}

    return lis


def addQuestionToTable(topic, question, url, level, platform):
    topicId = uuid.uuid1().hex
    res = insertIntoTable(table_name, "(?,?,?,?,?,?)",
                          (topicId, topic, question, url, level, platform))
    return res


def delRemark(id):
    res = deleteRowFromTable(table_name, id)
    return res


def updateRemark(study, remark, work, id):
    val = (study, remark, work, id)
    res = updateTable(table_name, "study=?,remark=?,work=?", "id=?", val)
    return res
