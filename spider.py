# -*- coding: utf-8 -*-

# @File    : spider.py
# @Date    : 2018-05-15

# 通过爬虫自动获取网站信息

import requests
from requests.exceptions import Timeout, MissingSchema
from requests.exceptions import ConnectionError
from lxml.etree import ParserError
from urllib.parse import urljoin, urlparse
from pyquery import PyQuery
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    print("get_website_info-url:", url)
    # 默认图标链接
    result = urlparse(url)
    default_icon = urljoin(result.scheme+"://"+result.netloc, "favicon.ico")
    print("default-ico:", default_icon)
    
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
        try:
            doc = PyQuery(response.text)
            title = doc("title").text().strip()
            icon = doc('link[rel="shortcut icon"]').attr("href")
            if icon==None:
                icon = doc('link[rel="SHORTCUT ICON"]').attr("href")
            print("parse-ico:", icon)
        except ParserError:
            print("Document is empty")
            pass

        if icon == None or icon=="":
            icon = default_icon

        if icon.startswith("//"):
            icon = "http:"+ icon
        if not icon.startswith("http"):
            icon = urljoin(url, icon)

        print("get_website_info-icon:", icon)
        print("get_website_info-title:", title)

    dct = {"title": title, "icon": icon}
    print(dct)

    return dct

# 下载图标
def download_icon(url):
    dirname = os.path.join("static", "ico")   #  保存文件夹
    savedir = os.path.join(BASE_DIR, dirname)  # 保存绝对路径

    # 测试路径
    test_path = os.path.join(BASE_DIR, url)
    print("test_path:", test_path)

    # 已存在则不需要下载
    if os.path.isfile(test_path) and os.path.exists(test_path):
        return url

    print("url:", url)
    # 默认图标
    icon_path = "static/images/favicon.ico"

    # 解析出文件保存的文件路径
    result = urlparse(url)
    print(result)
    ext = os.path.splitext(result.path)[-1]
    print(ext)
    domain = result.netloc.replace("www.", "")
    file = domain + ext      # 文件名
    filename= os.path.join(dirname, file)     # 返回的路径
    fullname = os.path.join(savedir, file)    # 文件绝对路径

    # 下载图片
    try:
        response = requests.get(url, headers=headers, timeout=3)
        print(response)
    except Timeout as e:
        print("下载超时：", url)
    except ConnectionError as e:
        print("链接错误：", url)
    except MissingSchema:
        print("模式错误：", url)
    else:
        if response.status_code == 200:
            # 文件夹不存在则创建
            if not os.path.isdir(savedir):
                os.makedirs(savedir)

            with open(fullname, "wb") as f:
                f.write(response.content)

            print(filename)
            icon_path = filename

    return icon_path


def move_tag():
    # TODO：用于从原网站迁移数据
    url = "https://www.pengshiyu.com/hao.html"
    response = requests.get(url)
    print(response)
    doc=PyQuery(response.text)
    a_all = doc("a")

    count =0
    for a in a_all.items():
        title = a.text()
        url = a.attr("href")
        if url.startswith("#"):
            continue
        data = {
            "title": title,
            "url": url,
            "classify": 1,
            "uid":"",
            "ico": "",
            "description":"",
            "weight":""
        }
        print(data)
        count += 1
        ret = requests.post("http://127.0.0.1:5000/edit", data=data)
        print(ret)
    print("count:", count)

if __name__ == "__main__":
    # url = "https://music.163.com/"
    # url = "https://www.dy2018.com/"
    # ret = get_website_info(url)
    # print(ret["title"])
    # print(ret["icon"])
    # ret = download_icon("http://s1.music/stylefavicon.ico?v20180307")
    # print(ret)
    move_tag()