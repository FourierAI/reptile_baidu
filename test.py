#!/usr/bin/env python
# encoding: utf-8

# @author: Zhipeng Ye
# @contact: Zhipeng.ye19@xjtlu.edu.cn
# @file: test.py
# @time: 2019-11-20 15:50
# @desc:

from seleniumrequests import Firefox

# Simple usage with built-in WebDrivers:
webdriver = Firefox()

response = webdriver.request('Get','www.baidu.com')

print(response)