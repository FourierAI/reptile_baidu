#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

keywords = []
file_keyword = open('/users/geekye/Desktop/keywords.txt')

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

# valid url list
removed_invalid_url = []

# get information from baidu
for i in range(len(urls)):

    # set timeout and turnoff ssl
    r = requests.get(urls[i], headers=request_hearders, timeout=0.8, verify=True)

    if r.status_code == 200:

        html_doc = r.content[2:]

        soup = BeautifulSoup(html_doc, 'html.parser')

        html_content = soup.get_text;

        b_content = soup.find('div', id='content_left')

        list1 = b_content.find_all('a', href=True)

        for elem in list1:
            url = elem['href']
            if url.startswith('https') or url.startswith('http'):
                removed_invalid_url.append(url)

if len(removed_invalid_url) < 1:
    raise Exception('there is nothing in removed_invalid_url')

# remove same elements
removed_invalid_url_set = set(removed_invalid_url)

url_direct_list = []
url_redirect_list = []

for url in removed_invalid_url:
    if "link?url=" in url:
        url_redirect_list.append(url)
    else:
        url_direct_list.append(url)

html_list = []

# opearte respectively
for url in url_direct_list:
    response = requests.get(url, headers=request_hearders, timeout=0.8, verify=True)
    html_list.append(response.content)

for url in url_redirect_list:
    # turn off redirect function
    res = requests.get(url=url, allow_redirects=False, headers=request_hearders, timeout=0.8, verify=True)
    direct_url = res.headers['location']

    response = requests.get(direct_url, allow_redirects=False, headers=request_hearders, timeout=0.8, verify=True)
    html_list.append(response.content)

print(len(html_list))
print('hello html')
