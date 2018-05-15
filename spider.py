# -*- coding: utf-8 -*-

# @File    : spider.py
# @Date    : 2018-05-15

# 通过爬虫自动获取网站信息

import requests
from requests.exceptions import Timeout
from pyquery import PyQuery


def get_website_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    }
    try:
        response = requests.get(url, headers=headers, timeout=3)
    except Timeout as e:
        pass

    doc = PyQuery(response.text)
    title = doc("title").text()
    icon = doc("link").attr("rel", "shortcut icon").attr("href")

    return {"title": title, "icon": icon}

if __name__ == "__main__":
    url = "https://www.baidu.com/"
    ret = get_website_info(url)
    print(ret["title"])
    print(ret["icon"])