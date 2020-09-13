# %%
import os
import json
import copy
import time
import requests
import argparse
import src.scrape_all_problems as scrape_all_problems
import src.scrape_extra_info as spider
import src.to_table as to_table
import multiprocessing
import pandas as pd


# %%
dirname = os.path.dirname(os.path.abspath(__file__))
leetcode_csv_relative_path = '../Data/leetcode_problems.csv'
leetcode_csv_full_path = os.path.join(dirname, leetcode_csv_relative_path)
if not os.path.exists(leetcode_csv_full_path):
    scrape_all_problems.run_method_2()
try:
    df = pd.read_csv(leetcode_csv_full_path, index_col='question_id')
    if len(df) < 1500:
        raise Exception(
            "Content Doesn't seem to be correct, there must be more than 1500 rows.")
except Exception as e:
    print(e)
    scrape_all_problems.run_method_2()
    df = pd.read_csv(leetcode_csv_full_path, index_col='question_id')
slugs = list(df['question__title_slug'])

# %%
s = requests.Session()
template = {"operationName": "questionData", "variables": {"titleSlug": None}, "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      paidOnly\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    enableDebugger\n    envInfo\n    libraryUrl\n    adminUrl\n    __typename\n  }\n}\n"}


# %%
def slug_to_qid(slug: str):
    search = df[df['question__title_slug'] == slug]
    assert len(search) <= 1
    return None if len(search) == 0 else int(search.index[0])


# %%
def run(slug):
    print("run slug '{}'".format(slug))
    payload = {"operationName": "questionData", "variables": {"titleSlug": slug}, "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      paidOnly\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    enableDebugger\n    envInfo\n    libraryUrl\n    adminUrl\n    __typename\n  }\n}\n"}
    payload_str = json.dumps(payload)
    headers = {
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "content-length": str(len(payload_str)),
        "content-type": "application/json",
        # "accept-encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "origin": "https://leetcode.com",
        "referer": "https://leetcode.com/problems/two-sum/"
    }
    response = s.post("https://leetcode.com/graphql",
                      headers=headers, json=payload)
    question = response.json()['data']['question']
    question_id = int(question['questionId'])
    similar_question_ids = [slug_to_qid(
        problem['titleSlug']) for problem in json.loads(question['similarQuestions'])]
    topic_tags = [{'name': tag['name'], 'slug': tag['slug']}
                  for tag in question['topicTags']]
    return {
        "question_id": question_id,
        "topic_tags": topic_tags,
        "similar_question_ids": similar_question_ids,
        "likes": question["likes"],
        "dislikes": question["dislikes"]
    }


# %%
def run_requests(yield_=False):
    results = []
    for index, slug in enumerate(slugs):
        print("{}. {}".format(index, slug))
        if yield_:
            yield run(slug)
        else:
            results.append(run(slug))
    if not yield_:
        return results


# %%
def main(yield_=False, multiprocess=True):
    if multiprocess:
        cpu_cores = multiprocessing.cpu_count()
        with multiprocessing.Pool(cpu_cores) as p:
            results = p.map(run, slugs)
    else:
        results = run_requests(yield_=yield_)

    for question in results:
        df.loc[question['question_id'], 'likes'] = question['likes']
        df.loc[question['question_id'], 'dislikes'] = question['dislikes']
        df.loc[question['question_id'], 'topic_tags'] = str(
            question['topic_tags'])
        df.loc[question['question_id'], 'similar_question_ids'] = str(
            question['similar_question_ids'])

    df.to_csv(leetcode_csv_full_path)
