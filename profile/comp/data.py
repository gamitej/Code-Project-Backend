from mapping import get_data_mapping,get_topic_list,topicName,platformName

'''
Profile data dropdown manipulation
'''
def getOptions(arr, name):
    lis = []
    data_mapping = get_data_mapping()
    for idx, val in enumerate(arr):
        lis.append(
            {"id": idx+1, "label": data_mapping[name][val], "value": val})
    return lis


platformList =  get_topic_list(platformName)
topicList = get_topic_list(topicName)
 

platformOptionsList = getOptions(platformList, platformName)
topicOptionsList = getOptions(topicList, topicName)


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
