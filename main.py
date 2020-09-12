# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os
import json
import requests
import pandas as pd


# %%
payload_template = {
    "operationName": "questionData",
    "variables": {"titleSlug": "two-sum"},
    "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      paidOnly\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    enableDebugger\n    envInfo\n    libraryUrl\n    adminUrl\n    __typename\n  }\n}\n"
}


# %%
payload = payload_template.copy()
payload["variables"]["titleSlug"] = 'longest-palindromic-substring'
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "content-length": str(len(json.dumps(payload))),
    "content-type": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "origin": "https://leetcode.com",
    "referer": "https://leetcode.com/problems/two-sum/"
}


# %%
response = requests.post("https://leetcode.com/graphql",
                         headers=headers, data=json.dumps(payload))


# %%
print(response.json())
