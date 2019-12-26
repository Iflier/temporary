# -*- codinh:utf-8 -*-
"""
Dec: 暂时无法容易地获取指数信息，抓取部分涨幅高的基金名称
Author: Iflier
Created on: 2019.12.24
"""
import re
import sys
import time
import json
import random
import string

import chardet
import requests
from scrapy.selector import Selector

browserHeader = {
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    "Accept-encoding": 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    "Host": "hq.sinajs.cn",
    "Referer": "http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
}

urlTemp = string.Template("https://hq.sinajs.cn/?_=${randomNum}&list=sh000001")

resp = requests.get(urlTemp.substitute(randomNum=random.random()) , headers=browserHeader, timeout=60, allow_redirects=False)
if resp.status_code != 200:
    print("[ERROR] Failed to get response !")
    sys.exit(0)
# resp.encoding = "utf-8"
try:
    content = re.search(r"\".*\"", resp.text, re.I).group()
    elements = content.split(',')[:6]
    print(elements)
except Exception as err:
    print("[ERROR] {0}".format(err))

print("Done.")
