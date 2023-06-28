# ============== MAPPING ================

topicName = "topics"
platformName = "platform"

topicMappping = {"twoPointers": "Two Pointers",
                 "strings": "Strings", "arrays": "Arrays","hi":"Hi"}

platformMappping = {"codechef": "Codechef",
                    "codeforces": "Codeforces", "leetcode": "Leetcode"}

dataMapping = {topicName: topicMappping, platformName: platformMappping}


def get_data_mapping():
    return dataMapping

def get_topic_list(name):
    lis = {topicName:topicMappping,platformName:platformMappping}
    ans = []
    for key in lis[name]:
        ans.append(key)
    print(ans)
    return ans