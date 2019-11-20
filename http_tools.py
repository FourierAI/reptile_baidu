#!/usr/bin/env python
# encoding: utf-8

# @author: Zhipeng Ye
# @contact: Zhipeng.ye19@xjtlu.edu.cn
# @file: http_tools.py
# @time: 2019-11-19 22:11
# @desc: tools for http
import random


class Http_tool:

    def __init__(self):
        self.hearder = {'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh,zh-CN;q=0.9',
                        'Sec-Fetch-Site': 'same-origin',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Sec-Fetch-Mode': 'cors',
                        'Referer': 'https://www.baidu.com/',
                        'is_xhr': '1',
                        'X-Requested-With': 'XMLHttpRequest',
                        'is_referer': 'https: // www.baidu.com / s?ie = utf - 8 & f = 8 & rsv_bp = 1 & rsv_idx = 1 & tn = baidu & wd = % E8 % 87 % AA % E6 % B2 % BB % E5 % 8C % BA & rsv_pq = 9920de180012c288 & rsv_t = d73eoIjdumalYBitcFYP % 2BS8JDjL41Fg0kk8H1Z9jjSo % 2FklkKKKDw % 2F9I % 2FzXE & rqlang = cn & rsv_enter = 1 & rsv_dl = ib & rsv_sug3 = 9 & rsv_sug1 = 4 & rsv_sug7 = 101'
                        }

        self.user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        ]

    def rand_user_agent(self):
        # chose one agent random
        user_agent = random.choice(self.user_agent_list)
        return user_agent

    def rand_user_agent_of_header(self):
        self.hearder['User-Agent'] = self.rand_user_agent()
        return self.hearder
