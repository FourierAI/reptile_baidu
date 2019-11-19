#!/usr/bin/env python
# encoding: utf-8

# @author: Zhipeng Ye
# @contact: Zhipeng.ye19@xjtlu.edu.cn
# @file: test_http.py
# @time: 2019-11-19 22:16
# @desc:


import http_tools


http_tools = http_tools.Http_tool()

agent = http_tools.rand_user_agent()

print(agent)