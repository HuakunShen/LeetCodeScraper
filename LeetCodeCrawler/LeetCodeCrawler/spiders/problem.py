import scrapy
import os
import json
import copy
import requests
import pandas as pd


class ProblemSpider(scrapy.Spider):
    handle_httpstatus_list = [400]
    name = 'problem'
    allowed_domains = ['leetcode.com']
    # start_urls = ['http://leetcode.com/']
    filepath = os.path.realpath(__file__)
    dirname = os.path.dirname(filepath)
    df = pd.read_csv(os.path.join(
        dirname, '../../../Data/leetcode_problems.csv'), index_col='question_id')

    def start_requests(self):
        template_filename = os.path.join(
            self.dirname, "../template/body_template.json")
        with open(template_filename, 'r') as file:
            payload_template = json.load(file)
            # payload = payload_template.copy()

        print(self.df)

        payload_str = '{"operationName":"questionData","variables":{"titleSlug":"two-sum"},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      paidOnly\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    enableDebugger\n    envInfo\n    libraryUrl\n    adminUrl\n    __typename\n  }\n}\n"}'
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Content-Length": "1019",
            "referer": "https://leetcode.com/problems/two-sum/",
            "content-type": "application/graphql",
            "accept-encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "origin": "https://leetcode.com",
        }
        self.logger.debug(payload_str)
        yield scrapy.Request(url='https://leetcode.com/graphql/', errback=self.errback_httpbin,
                             callback=self.parse, method='POST', dont_filter=True, headers=headers, body=payload_str.encode())
        # for index, slug in enumerate(self.df['question__title_slug']):
        #     if index == 5:  # debug TODO: remove this
        #         break
        #     payload = copy.deepcopy(payload_template)
        #     payload["variables"]["titleSlug"] = slug
        #     # payload_str = json.dumps(payload)
        #     payload_str = '{"operationName":"questionData","variables":{"titleSlug":"two-sum"},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      paidOnly\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    enableDebugger\n    envInfo\n    libraryUrl\n    adminUrl\n    __typename\n  }\n}\n"}'
        #     headers = {
        #         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        #         "Content-Length": "1019",
        #         "referer": "https://leetcode.com/problems/two-sum/",
        #         "content-type": "application/json",
        #         "accept-encoding": "gzip, deflate, br",
        #         "Connection": "keep-alive",
        #         "Accept": "*/*",
        #         "origin": "https://leetcode.com",
        #     }
        #     self.logger.debug(payload_str)
        #     yield scrapy.Request(url='https://leetcode.com/graphql', errback=self.errback_httpbin,
        #                          callback=self.parse, method='POST', headers=headers, body=payload_str.encode())
        # yield scrapy.Request('https://huakunshen.com')

    def parse(self, response):
        self.logger.debug("status code: {}".format(response.status))
        # logger.debug("body: {}".format(response.body))
        self.logger.debug("text: {}".format(response.text))
        self.logger.debug("flags: {}".format(response.flags))
        self.logger.debug("headers: {}".format(response.headers))
        # logger.debug("id: " + response.json()
        #              ['data']['question']['questionId'])
        pass

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error("Error")
        self.logger.error(repr(failure))
