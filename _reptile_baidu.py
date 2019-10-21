#!/usr/bin/python

import requests
import os
from requests import ReadTimeout
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tkinter import _flatten


def generate_request_baidu_url(file_path):
    file_keyword = open(file_path)
    try:
        file_content = file_keyword.read()
        keywords = file_content.splitlines()
    finally:
        file_keyword.close()
    urls = []
    for keyword in keywords:
        # failure to reptile information from bing
        # url = "https://cn.bing.com/search?q=" + keyword
        # url = "https://bing.com/search?q=" + keyword + "&PC=U" + str(pc_code) + "&FORM=CHROMN"
        # it seem that baidu is ok
        url = "https://www.baidu.com/s?ie=utf-8&wd=" + keyword
        urls.append(url)

    # imitate as browser
    request_hearders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }

    return urls, request_hearders


def get_urls_in_baidu(urls, request_hearders):
    removed_invalid_url = []

    # get information from baidu

    # generate parameters_map for multithreading
    parameters_list = []
    for i in range(len(urls)):
        parameters_map = {'i': i, 'request_headers': request_hearders, 'urls': urls}
        parameters_list.append(parameters_map)

    with ThreadPoolExecutor(max_workers=20) as pool:
        valid_urls = pool.map(get_url_in_baidu, parameters_list)

        removed_invalid_url.extend(valid_urls)

    return removed_invalid_url


def get_url_in_baidu(parameters):
    i = parameters['i']

    request_hearders = parameters['request_headers']

    urls = parameters['urls']

    valid_urls = []
    try:
        # set timeout and turnoff ssl
        r = requests.get(urls[i], headers=request_hearders, timeout=2)
        if r.status_code == 200:

            html_doc = r.content.decode('utf-8')

            soup = BeautifulSoup(html_doc, 'html.parser')

            b_content = soup.find('div', id='content_left')

            list1 = b_content.find_all('a', href=True)

            for elem in list1:
                url = elem['href']
                if url.startswith('https') or url.startswith('http'):
                    valid_urls.append(url)
                    # removed_invalid_url.append(url)

            for elem in list1:
                attrs = elem.attrs
                if hasattr(attrs, 'data-url'):
                    url = elem['data-url']
                    if 'baike' in url:
                        valid_urls.append(url)

    except (requests.exceptions.ConnectionError, ReadTimeout):
        print('get Baidu information timeout!')

    return valid_urls


def separater_direct_indirect_list(removed_invalid_url):
    # remove same elements
    removed_invalid_url_set = set(_flatten(removed_invalid_url))
    url_direct_list = []
    url_redirect_list = []
    for url in removed_invalid_url_set:
        if "link?url=" in url:
            url_redirect_list.append(url)
        else:
            url_direct_list.append(url)
    return url_direct_list, url_redirect_list


def generate_html_list(url_direct_list, url_redirect_list):
    html_list = []

    with ThreadPoolExecutor(max_workers=20) as pool:
        # opearte respectively
        html_direct_list2 = pool.map(get_direct_website_from_direct, url_direct_list)

        html_list.extend(html_direct_list2)
        html_list = list(filter(None, html_list))

    with ThreadPoolExecutor(max_workers=20) as pool:
        html_indirect_list2 = pool.map(get_direct_website_from_indirect_location, url_redirect_list)

        html_list.extend(html_indirect_list2)
        html_list = list(filter(None, html_list))

    return html_list


def get_direct_website_from_direct(url):
    response_content = None

    if 'baike' in url:
        try:
            response = requests.get(url, headers=request_hearders, timeout=2)
            response_content = response.content
        except (requests.exceptions.ConnectionError, ReadTimeout):
            print("Direct connection is timeout!")

    return response_content


def get_direct_website_from_indirect_location(url):
    html = None
    res = None

    try:

        # turn off redirect function
        res = requests.get(url=url, allow_redirects=False, headers=request_hearders, timeout=2)
    except (requests.exceptions.ConnectionError, ReadTimeout):
        print("Redirect is failure!")

    if (res is not None) and (res.status_code == 302):

        direct_url = res.headers['location']

        if 'baike' in direct_url:

            response = None
            try:
                response = requests.get(direct_url, allow_redirects=False, headers=request_hearders, timeout=2)
            except (requests.exceptions.ConnectionError, ReadTimeout):
                print("Reptile original website is failure!")

            if (response is not None) and (response.status_code == 200):
                html = response.content

    return html


def convert_html_txt(html_list):

    # remove same html by default hashcode
    html_list = list(set(html_list))
    text_list = []
    for html in html_list:
        soup = BeautifulSoup(html, 'html.parser')

        text = soup.text

        info = [s.extract() for s in soup('script')]

        for script_content in info:
            text = text.replace(script_content.text, '')

        text = text.replace('\n', '')
        text_list.append(text)

    return text_list


# main function
if __name__ == '__main__':

    # files_path = input('files_path (case sensitive):')

    # file_path = input('file_path(case sensitive):')
    file_path = '/users/geekye/Desktop/keywords.txt'

    # file_path = sys.argv[0]
    # generate urls of request of baidu from txt file
    urls, request_hearders = generate_request_baidu_url(file_path)

    removed_invalid_url = get_urls_in_baidu(urls, request_hearders)

    if len(removed_invalid_url) < 1:
        raise Exception('there is nothing in removed_invalid_url')

    # separater_direct_indirect_list
    url_direct_list, url_redirect_list = separater_direct_indirect_list(removed_invalid_url)

    html_list = generate_html_list(url_direct_list, url_redirect_list)

    dir_list = file_path.split('/')
    file_fpath = '/'.join(dir_list[:len(dir_list) - 1]) + '/html_files'

    if not os.path.exists(file_fpath):
        os.mkdir(file_fpath)

    os.chdir(file_fpath)

    text_list = convert_html_txt(html_list)

    # write files
    for i in range(len(text_list)):

        with open(str(i) + '.txt', 'w+') as html_content_file:
            html_content_file.write(text_list[i])

# /users/geekye/Desktop/keywords.txt
