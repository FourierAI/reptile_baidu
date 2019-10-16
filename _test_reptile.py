#!/usr/bin/python

import requests
from requests import ReadTimeout
from bs4 import BeautifulSoup


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
    for i in range(len(urls)):

        try:
            # set timeout and turnoff ssl
            r = requests.get(urls[i], headers=request_hearders, timeout=2)
            if r.status_code == 200:

                html_doc = r.content[2:]

                soup = BeautifulSoup(html_doc, 'html.parser')

                html_content = soup.get_text

                b_content = soup.find('div', id='content_left')

                list1 = b_content.find_all('a', href=True)

                for elem in list1:
                    url = elem['href']
                    if url.startswith('https') or url.startswith('http'):
                        removed_invalid_url.append(url)

        except (requests.exceptions.ConnectionError, ReadTimeout):
            print('get Baidu information timeout!')
            continue

    return removed_invalid_url


def separater_direct_indirect_list(removed_invalid_url):
    # remove same elements
    removed_invalid_url_set = set(removed_invalid_url)
    url_direct_list = []
    url_redirect_list = []
    for url in removed_invalid_url:
        if "link?url=" in url:
            url_redirect_list.append(url)
        else:
            url_direct_list.append(url)
    return url_direct_list, url_redirect_list


def generate_html_list(url_direct_list, url_redirect_list):
    html_list = []

    # opearte respectively
    for url in url_direct_list:
        try:
            response = requests.get(url, headers=request_hearders, timeout=2)
        except (requests.exceptions.ConnectionError, ReadTimeout):
            print("Direct connection is timeout!")
            continue
        html_list.append(response.content)

    for url in url_redirect_list:

        # turn off redirect function
        try:
            res = requests.get(url=url, allow_redirects=False, headers=request_hearders, timeout=2)
        except (requests.exceptions.ConnectionError, ReadTimeout):
            print("Redirect is failure!")
            continue

        if (res.status_code == 302):
            direct_url = res.headers['location']
        else:
            continue

        try:
            response = requests.get(direct_url, allow_redirects=False, headers=request_hearders, timeout=2)
        except (requests.exceptions.ConnectionError, ReadTimeout):
            print("Reptile original website is failure!")
            continue

        if (res.status_code == 200):
            html_list.append(response.content)

    return html_list


# main function
if __name__ == '__main__':

    file_path = '/users/geekye/Desktop/keywords.txt'
    # generate urls of request of baidu from txt file
    urls, request_hearders = generate_request_baidu_url(file_path)

    removed_invalid_url = get_urls_in_baidu(urls, request_hearders)

    if len(removed_invalid_url) < 1:
        raise Exception('there is nothing in removed_invalid_url')

    # separater_direct_indirect_list
    url_direct_list, url_redirect_list = separater_direct_indirect_list(removed_invalid_url)

    html_list = generate_html_list(url_direct_list, url_redirect_list)

    # test
    for html in html_list:
        print(html)

    print("the length of html list:" + str(len(html_list)))
