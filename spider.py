# -*- coding: utf-8 -*-

# @File    : spider.py
# @Date    : 2018-05-15

# 通过爬虫自动获取网站信息

import requests
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from urllib.parse import urljoin, urlparse
from pyquery import PyQuery
import os

# BASE_DIR = path.basename(path.dirname(path.abspath(__file__)))

headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    }

# 获取网站信息
def get_website_info(url):
    title = ""
    icon = ""

    try:
        response = requests.get(url, headers=headers, timeout=3)
        print(response)
    except Timeout as e:
        pass
    except ConnectionError as e:
        pass
    else:
        response.encoding = response.apparent_encoding
        doc = PyQuery(response.text)
        title = doc("title").text().strip()
        icon = doc("link[rel='shortcut icon']").attr("href")
        if icon == None:
            icon = urljoin(url, "favicon.ico")
        print("icon", icon)
        if icon.startswith("//"):
            icon = "http:"+ icon
        if not icon.startswith("http"):
            icon = urljoin(url, icon)
        icon = download_icon(icon)
    return {"title": title, "icon": icon}

# 下载图标
def download_icon(url):
    print("url:", url)
    # 默认图标
    icon_path = "static/images/favicon.ico"

    # 解析出文件保存的文件路径
    result = urlparse(url)
    domain = result.netloc.replace("www.", "")
    dirname = "static\ico"  # 保存路径
    file = domain + ".ico"  # 文件名
    filename = os.path.join(dirname, file)  # 文件路径

    # 先判断是否存在,不存在则请求下载
    if os.path.exists(filename):
        icon_path = filename

    else:
        try:
            response = requests.get(url, headers=headers, timeout=3)
            print(response)
        except Timeout as e:
            pass
        except ConnectionError as e:
            pass
        else:
            if response.status_code == 200:
                # 不存在则创建
                if not os.path.isdir(dirname): os.makedirs(dirname)

                with open(filename, "wb") as f:
                    f.write(response.content)

                print(filename)
                icon_path = filename
    return icon_path

if __name__ == "__main__":
    # url = "https://music.163.com/"
    # url = "https://www.dy2018.com/"
    # ret = get_website_info(url)
    # print(ret["title"])
    # print(ret["icon"])
    ret = download_icon("http://s1.music/stylefavicon.ico?v20180307")
    print(ret)