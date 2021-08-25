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
import parsePage

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

pageSize = 100

start_date = '2000-07-01 00:00:00.0'

data = {
    'page': 1,
    'scqy': '公司',
    'x': 81,
    'y': 25
}




def gh_data_spider():
    url = 'https://www.cn-truck.com/gonggao/listhbres'
    data['limit'] = 1
    resp_json = json.loads(requests.post(url, headers=headers, data=data).text)
    # 获取页面大小
    count = int(resp_json.get('count'))
    pageCount = int(count / pageSize) + 1
    data['limit'] = pageSize
    result_dict = {
        '重型柴油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=e90a899e2f7d6ebcc4336603a2793d0692dd0d0138e43b98&isprotect=false',
        '轻型汽油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=eed447b627eeee8bed21c88ab001bbd5a8f5badb78f6ab6c&isprotect=false',
        '重型燃气车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=6cbb1e3d2733d167c11dede505c3ae30233d60ed912a811d&isprotect=false',
        '摩托车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=85b7de1045e7d255cc90660e36a3f06d233d60ed912a811d&isprotect=false',
        '轻型汽车混合动力车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=01ec3d09b319c59d8f743c5910e38d9d233d60ed912a811d&isprotect=false',
        '非道路移动机械(柴油)环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=85031b741b2935b218b45efd3668c509ce49eb8f8b9f6995&isprotect=false',
        '轻型两用燃料车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=62bb2bd377151dfbdfe18e66126cf157efd519426e7bb918&isprotect=false',
        '电动车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=d014505829f36ba0a23ef2c857f41e4bb21c5ae6f07f61d4&isprotect=false',
        '轻型柴油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=43a99bcf18efd9f7a872340e0f4cdcb8dc50418b9e7f4cb5&isprotect=false',
        '轻便摩托车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=d8b0b83d804dc12ccd70fd45b1ebb6b6a8f5badb78f6ab6c&isprotect=false',
        '重型柴油混合动力车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=e90a899e2f7d6ebcfde507f500890de54746ecf1a9fe7019&isprotect=false',
        '环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=216a53fa21daa2ac50f31bded5d02ff8233d60ed912a811d&isprotect=false',
        '重型汽油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=9ea2156a81d7d5b389d4de5a447dab1befd519426e7bb918&isprotect=false'
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
        # # 请求每个页面
        # for sbbh in sbbh_list[0:10]:
        #     print(sbbh)
        #     # res = parse_detail(sbbh)
        #     result_dict[res.get('车辆类别')] = res.get('url')
        # print(result_dict)
        # # 每一页结束之后写入文件
        # # utils.saveData(result, 'E:/车辆类别信息.xls')

if __name__ == '__main__':

    url = 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=43a99bcf18efd9f7bcace8cdcb3da312dc50418b9e7f4cb5&isprotect=false'
    page_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page_text, 'html.parser')
    print(parsePage.parse_paeg_qxcyc(soup))