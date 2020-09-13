import os
import json
import pandas as pd

dirname = os.path.dirname(os.path.abspath(__file__))
leetcode_csv_relative_path = '../Data/leetcode_problems.csv'
leetcode_csv_full_path = os.path.join(dirname, leetcode_csv_relative_path)
tag_url_prefix = "https://leetcode.com/tag"
df = pd.read_csv(leetcode_csv_full_path, index_col='question_id')


# %%
def to_a_link(text: str, url: str) -> str:
    return "<a href='" + url + "'>" + text + "</a>"


# %%
def topic_tags_to_links(tags_str: str) -> str:
    tags_list = json.loads(tags_str.replace("'", '"'))
    a_links = []
    for tag in tags_list:
        a_links.append(
            to_a_link(tag['name'], "{}/{}".format(tag_url_prefix, tag['slug'])))
    return a_links


# %%
def similar_question_ids_to_links(similar_question_ids_str):
    similar_question_ids = json.loads(similar_question_ids_str)
    a_links = []
    for id in similar_question_ids:
        row = df.loc[id]
        a_links.append(to_a_link(row['question__title'], row['url']))
    return a_links

# %%


def main():
    difficulty_map = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
    for i in df.index:
        df.loc[i, 'difficulty'] = difficulty_map[df.loc[i]['difficulty']]

    df['Title'] = "<a href='" + df['url'] + \
        "'>" + df['question__title'] + "</a>"

    df.rename(columns={'frontend_question_id': 'id', 'paid_only': 'Paid Only',
                       'is_new_question': 'New Question', 'difficulty': 'Difficulty'}, inplace=True, errors='raise')

    new_df = df[['id', 'Title', 'Difficulty', 'Paid Only', 'New Question']]

    new_df.loc[:, 'Topic Tags'] = None
    new_df.loc[:, 'Similar Questions'] = None

    for index in new_df.index:
        new_df.loc[index, 'Topic Tags'] = ', '.join(
            topic_tags_to_links(df.loc[index, 'topic_tags']))
        new_df.loc[index, 'Similar Questions'] = ', '.join(
            similar_question_ids_to_links(df.loc[index, 'similar_question_ids']))

    new_df.to_html(os.path.join(dirname, "../Data/problems.md"),
                   escape=False, index=False)
    new_df.to_html(os.path.join(dirname, "../Data/problems.html"),
                   escape=False, index=False)
