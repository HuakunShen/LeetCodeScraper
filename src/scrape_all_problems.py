# %%
import os
import json
import requests
import pandas as pd

dirname = os.path.dirname(os.path.abspath(__file__))
leetcode_csv_relative_path = '../Data/leetcode_problems.csv'
leetcode_csv_full_path = os.path.join(dirname, leetcode_csv_relative_path)
# %%
res = requests.get("https://leetcode.com/api/problems/all/")


# %%
all_data = json.loads(res.text)
all_problems = all_data['stat_status_pairs']


# %%
def run_method_1():
    parsed_data = []
    for problem in all_problems:
        parsed_data_dict = {}
        parsed_data_dict['difficulty'] = problem['difficulty']['level']
        parsed_data_dict['paid_only'] = problem['paid_only']
        parsed_data_dict['is_new_question'] = problem['stat']['is_new_question']
        parsed_data_dict['question_id'] = problem['stat']['question_id']
        parsed_data_dict['frontend_question_id'] = problem['stat']['frontend_question_id']
        parsed_data_dict['total_acs'] = problem['stat']['total_acs']
        parsed_data_dict['total_submitted'] = problem['stat']['total_submitted']
        parsed_data_dict['question__title'] = problem['stat']['question__title']
        parsed_data_dict['question__title_slug'] = problem['stat']['question__title_slug']
        parsed_data.append(parsed_data_dict)
    df = pd.DataFrame(columns=['question_id', 'frontend_question_id', 'question__title', 'question__title_slug', 'difficulty',
                               'paid_only', 'is_new_question', 'total_acs', 'total_submitted', 'likes', 'dislikes', 'topic_tags', 'similar_question_ids'])
    for problem in parsed_data:
        df = df.append(problem, ignore_index=True)
    df.sort_index(inplace=True)
    df.to_csv(leetcode_csv_full_path, index=False)


# %%
def run_method_2():
    df1 = pd.DataFrame(index=['question_id'], columns=['frontend_question_id', 'question__title', 'question__title_slug', 'difficulty',
                                                       'paid_only', 'is_new_question', 'total_acs', 'total_submitted', 'likes', 'dislikes', 'topic_tags', 'similar_question_ids'])
    for problem in all_problems:
        difficulty = problem['difficulty']['level']
        paid_only = problem['paid_only']
        is_new_question = problem['stat']['is_new_question']
        question_id = problem['stat']['question_id']
        frontend_question_id = problem['stat']['frontend_question_id']
        total_acs = problem['stat']['total_acs']
        total_submitted = problem['stat']['total_submitted']
        question__title = problem['stat']['question__title']
        question__title_slug = problem['stat']['question__title_slug']
        df1.loc[question_id] = [frontend_question_id, question__title, question__title_slug,
                                difficulty, paid_only, is_new_question, total_acs, total_submitted, None, None, None, None]
    df1.dropna(how='all', inplace=True)
    df1.sort_index(inplace=True)
    df1['url'] = 'https://leetcode.com/problems/' + df1['question__title_slug']
    df1.to_csv(leetcode_csv_full_path, index_label='question_id')


# %%
if __name__ == "__main__":
    run_method_2()
