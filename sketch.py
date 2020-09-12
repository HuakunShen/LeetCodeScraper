# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
import json
import pandas as pd


# %%
with open('./LeetCodeCrawler/LeetCodeCrawler/template/body_template.json', 'r') as file:
    payload_template = json.load(file)


# %%
payload = payload_template.copy()
payload["variables"]["titleSlug"] = 'longest-palindromic-substring'


# %%
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
response = requests.post("https://leetcode.com/graphql",
                         headers=headers, data=json.dumps(payload))
response.status_code


# %%
print(response.json())


# %%


# %%


# %%


# %%


# %%


# %%
