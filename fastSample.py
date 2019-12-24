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
import string
import argparse

import pandas
import requests


ap = argparse.ArgumentParser()
ap.add_argument('-n', '--number', type=int, default=15, help="指定打印前几项")
args = vars(ap.parse_args())

dataList = list()
browserHeader = {
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    "Accept-encoding": 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
urlTemp = string.Template("http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page=1,200&dt=${timestamp}&atfc=&onlySale=0")

resp = requests.get(urlTemp.substitute(timestamp=round(time.time(), 3) * 1000), headers=browserHeader, timeout=60, allow_redirects=False)
if resp.status_code != 200:
    print("[ERROR] Failed to get response !")
    sys.exit(0)
resp.encoding = "utf-8"
try:
    contentStr = re.search(r"\[\[.*\]\]", resp.text, re.I).group()
    contentList = json.loads(contentStr, encoding='utf-8')
except Exception as err:
    print('[ERROR] {0}'.format(err))
    sys.exit(0)

for elem in contentList:
    content = dict()
    content["fundCode"] = elem[0]
    content["fundName"] = elem[1]
    content["latestUnitNet"] = elem[3]
    content["latestAccNet"] = elem[4]
    content['lastUnitNet'] = elem[5]
    content['lastAccNet'] = elem[6]
    content['dailyGrowth'] = elem[7]
    content['dailyGrowthRatio'] = elem[8]
    dataList.append(content)
print(pandas.DataFrame(dataList)[:args['number']])
print("Done.")
