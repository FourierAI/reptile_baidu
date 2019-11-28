#!/usr/bin/env python
# encoding: utf-8

# @author: Zhipeng Ye
# @contact: Zhipeng.ye19@xjtlu.edu.cn
# @file: clean_data.py
# @time: 2019-11-27 22:49
# @desc: clean html
from io import StringIO


def clean_data(html):

    # remove invalid data
    if '{"title":' in html or '{"status":' in html \
            or '<&for(var i in' in html or '.zaixiankefu {' in html:
        return ''

    if '百度资讯搜索' in html or '百度地图' in html or '百度数据开放平台' in html:
        return ''

    if '查询-企查查查一下' in html or '当当' in html:
        return ''


    # clean program language
    html = html.split("window.alogObjectConfig = ")[0]
    html = html.split("Copyright  ©")[0]
    html = html.split("网上有害信息举报专区")[0]

    # clean \n
    content = StringIO()
    count_n = 0
    for str in html:
        if '\n' is not str:
            content.write(str)
            count_n = 0
        elif count_n >= 1:
            continue
        else:
            content.write(str)
            count_n = count_n + 1

    html = content.getvalue()
    return html


if __name__ == '__main__':
    str = '\n\n\n\n123\n\n23423\n\n\n\n342\n'

    test = clean_data(str)

    print(test)
