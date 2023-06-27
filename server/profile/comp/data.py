from mapping import get_data_mapping

'''
Profile data dropdown manipulation
'''


def getOptions(arr, name):
    lis = []
    for idx, val in enumerate(arr):
        lis.append(
            {"id": idx+1, "label": data_mapping[name][val], "value": val})
    return lis


data_mapping = get_data_mapping()

platformList = ["codechef", "codeforces", "leetcode"]
topicList = ["arrays", "twoPointers", "strings"]


platformOptionsList = getOptions(platformList, "platform")
topicOptionsList = getOptions(topicList, "topics")


dropDownData = [
    {
        "id": "1",
        "options": platformOptionsList,
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
        "options": topicOptionsList,
        "label": "Topic",
        "name": "topic",
    },
]


def getProfileDropDown():
    return dropDownData
