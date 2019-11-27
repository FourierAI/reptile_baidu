#!/usr/bin/env python
# encoding: utf-8

# @author: Zhipeng Ye
# @contact: Zhipeng.ye19@xjtlu.edu.cn
# @file: test_http.py
# @time: 2019-11-19 22:16
# @desc:

import unittest
import logging
import http_tools

class TestHTTPTools(unittest.TestCase):


    def test_agent(self):
        http_tools1 = http_tools.HttpTool()

        agent = http_tools1.rand_user_agent()
        logging.info(agent)

