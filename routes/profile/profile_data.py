class ProfileDataDropdown:

    # ================ DROP DOWN ===============

    topicName = "topics"
    platformName = "platform"

    topicMappping = {"twoPointers": "Two Pointers",
                    "strings": "Strings", "arrays": "Arrays","stack":"Stack","binarySearch":"Binary Search","linkedlist":"Linked List","tree-1":"Tree - 1","tree-2":"Tree - 2","dp-1":"Dynamic Programming - 1","heap":"Heap - Priority Queue","dp-2":"Dynamic Programming - 2","slidingWindow":"Sliding Window"}

    platformMappping = {"codechef": "Codechef",
                        "codeforces": "Codeforces", "leetcode": "Leetcode"}

    dataMapping = {topicName: topicMappping, platformName: platformMappping}

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
        myKeys = list(self.topicMappping.keys())
        myKeys.sort()
        sorted_dict = {i: self.topicMappping[i] for i in myKeys}
        return sorted_dict
    

    def getQueTableData(self,data):
        rows = []
        for row in data:
            url,topic,question,level,platform,date,done=row[0],row[1],row[2],row[3],row[4],row[5],row[6]
            if done == 1:
                done = "Yes"
            else:
                done ="No"
            rows.append({"level":level,"topic":self.topicMappping.get(topic),"question":question,"platform":platform,"done":done,"url":url,"date":date})
        return {"rows":rows}

if __name__=="__main__":
    obj = ProfileDataDropdown()