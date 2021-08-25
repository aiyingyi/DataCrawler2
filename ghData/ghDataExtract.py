#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/8/20 11:42
# @Author  : aiyingyi
# @FileName: ghDataExtract.py
# @Software: PyCharm

'''
国环数据爬取
'''

import requests
import json
import time
from bs4 import BeautifulSoup
from utils.spiderUtils import utils

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

pageSize = 100
# start_date = '2000-01-01'
start_date = '2000-07-01 00:00:00.0'

data = {
    'page': 1,
    'scqy': '公司',
    'x': 81,
    'y': 25
}


# 时间字符串的比较
def compare_time(time1, time2):
    s_time = time.mktime(time.strptime(time1, '%Y-%m-%d'))
    e_time = time.mktime(time.strptime(time2, '%Y-%m-%d'))
    return int(s_time) - int(e_time)


# 根据bbh信息，解析对应的页面
def parse_detail(sbbh):
    url = 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=' + sbbh + '&isprotect=false'
    page_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page_text, 'html.parser')
    res = {}
    h1_text = soup.find('h1').text
    res['车辆类别'] = ''.join(
        [char for char in list(h1_text) if (char != ' ' and char != '\n' and char != '\r' and char != '\t')])
    res['url'] = url
    return res


def gh_data_spider():
    url = 'https://www.cn-truck.com/gonggao/listhbres'
    data['limit'] = 1
    resp_json = json.loads(requests.post(url, headers=headers, data=data).text)
    # 获取页面大小
    count = int(resp_json.get('count'))
    pageCount = int(count / pageSize) + 1
    data['limit'] = pageSize

    # result_dict = {
    # }
    result_dict = {
        '重型柴油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=e90a899e2f7d6ebc62b14c077490fce9b21c5ae6f07f61d4&isprotect=false',
        '轻型汽油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=eed447b627eeee8be2c60bada95574bddc50418b9e7f4cb5&isprotect=false',
        '重型燃气车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=6cbb1e3d2733d167397c249255b6dbdbb21c5ae6f07f61d4&isprotect=false',
        '摩托车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=55421520374d810f36cfb8290c2b0485dc50418b9e7f4cb5&isprotect=false',
        '轻型汽车混合动力车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=01ec3d09b319c59d1d250e7b9bb1190ace49eb8f8b9f6995&isprotect=false',
        '非道路移动机械(柴油)环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=5b325145d52fac33109c9019ab78a59aa8f5badb78f6ab6c&isprotect=false',
        '轻型两用燃料车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=62bb2bd377151dfbdfe18e66126cf157efd519426e7bb918&isprotect=false',
        '电动车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=d014505829f36ba0ac0a5e71b4e375cba8f5badb78f6ab6c&isprotect=false',
        '轻型柴油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=43a99bcf18efd9f79ed190b529857eac4746ecf1a9fe7019&isprotect=false',
        '轻便摩托车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=d8b0b83d804dc12ccc956731b3d07f2aefd519426e7bb918&isprotect=false',
        '重型柴油混合动力车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=e90a899e2f7d6ebcfe5d812a5927545c4746ecf1a9fe7019&isprotect=false',
        '环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=216a53fa21daa2aca11920eb5290357bd12db3aadc7c433f&isprotect=false',
        '重型汽油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=9ea2156a81d7d5b3130af09eaea23008dc50418b9e7f4cb5&isprotect=false',
        '重型甲醇燃料汽车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=4b4a1e490ac0963bcd06f9ba6b0accd092dd0d0138e43b98&isprotect=false',
        '城市车辆重型柴油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=216a53fa21daa2acee3964cb89ac2c4fb21c5ae6f07f61d4&isprotect=false',
        '非道路移动机械柴油机环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=05befd3ebc372ef8297bc7dc905f60f8d12db3aadc7c433f&isprotect=false',
        '轻型燃气车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=84b207a9d7706e8692b7c85e2536083ddc50418b9e7f4cb5&isprotect=false',
        '重型燃气混合动力车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=6cbb1e3d2733d167f18c5e6d09993c26bf646bf7da6e187c&isprotect=false'
    }

    for pageNo in range(100, pageCount):
        print('正在解析第%d页，共%d页' % (pageNo, pageCount))
        # result = []
        data['page'] = pageNo
        resp_json = json.loads(requests.post(url, headers=headers, data=data).text)
        data_list = resp_json.get('data')
        # 过滤掉之前发布的信息
        # sbbh_list = [ele.get('sbbh') for ele in data_list if ele.get('date') > start_date]
        sbbh_list = [ele.get('sbbh') for ele in data_list if ele.get('gksj') > start_date]
        # 请求每个页面
        for sbbh in sbbh_list[70:80]:
            print(sbbh)
            res = parse_detail(sbbh)
            result_dict[res.get('车辆类别')] = res.get('url')
        print(result_dict)
        # 每一页结束之后写入文件
        # utils.saveData(result, 'E:/车辆类别信息.xls')


if __name__ == '__main__':
    gh_data_spider()
