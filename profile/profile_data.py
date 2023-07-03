class ProfileDataDropdown:

    # ================ DROP DOWN ===============

    topicName = "topics"
    platformName = "platform"

    topicMappping = {"twoPointers": "Two Pointers",
                    "strings": "Strings", "arrays": "Arrays"}

    platformMappping = {"codechef": "Codechef",
                        "codeforces": "Codeforces", "leetcode": "Leetcode"}

    dataMapping = {topicName: topicMappping, platformName: platformMappping}

    # ================== TABLE CONSTANTS =================

    tableColumn = [
        {
            "accessorKey": "level",
            "header": "Level",
            "size": 40,
        },
        {
            "accessorKey": "question",
            "header": "Question",
            "size": 220,
        },
         {
            "accessorKey": "topic",
            "header": "Topic",
            "size": 60,
        },
        {
            "accessorKey": "url",
            "header": "Question url",
            "size": 220,
        },
        {
            "accessorKey": "done",
            "header": "Done",
            "size": 40,
        },
        {
            "accessorKey": "platform",
            "header": "Platform",
            "size": 40,
        },
    ],

    def __init__(self):
        # lists
        self.topicList = self.get_topic_list(self.topicName)
        self.platformList =  self.get_topic_list(self.platformName)
        # options
        self.topicOptionsList = self.getOptions(self.topicList, self.topicName)
        self.platformOptionsList = self.getOptions(self.platformList, self.platformName)

    def get_topic_list(self,name):
        lis = {self.topicName:self.topicMappping,self.platformName:self.platformMappping}
        ans = []
        for key in lis[name]:
            ans.append(key)
        return ans

    def getOptions(self,arr, name):
        lis = []
        data_mapping = self.dataMapping
        for idx, val in enumerate(arr):
            lis.append(
                {"id": idx+1, "label": data_mapping[name][val], "value": val})
        return lis

    def getProfileDropDown(self):
        return [
        {
            "id": "1",
            "options": self.platformOptionsList,
            "label": "Platform",
            "name": "platform",
        },
        {
            "id": "2",
            "options": [
                {"id": 1, "label": "Easy", "value": "easy"},
                {"id": 2, "label": "Medium", "value": "medium"},
                {"id": 3, "label": "Hard", "value": "hard"},
            ],
            "label": "Level",
            "name": "level",
        },
        {
            "id": "3",
            "options": self.topicOptionsList,
            "label": "Topic",
            "name": "topic",
        },
    ]

    def getTopicMapping(self):
        return self.topicMappping
    

    def getQueTableData(self,data):
        rows = []
        for row in data:
            url,topic,question,level,platform,done=row[0],row[1],row[2],row[3],row[4],row[5]
            rows.append({"level":level,"topic":topic,"question":question,"platform":platform,"done":done == 1,"url":url})
        return {"columns":self.tableColumn,"rows":rows}

if __name__=="__main__":
    obj = ProfileDataDropdown()