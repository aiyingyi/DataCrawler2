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
from bs4 import BeautifulSoup
from utils.spiderUtils import utils
import parsePage

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}


def gh_data_spider():
    try:
        sbbh_list = ['2f49162e9858baffd9bacf8baab6bf3992dd0d0138e43b98']
        # 请求每个页面
        for sbbh in sbbh_list:
            detail_url = 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=' + sbbh + '&isprotect=false'
            print(detail_url)
            # 处理不能爬取的数据
            try:
                page_text = requests.get(detail_url, headers=headers).text
                soup = BeautifulSoup(page_text, 'html.parser')
                # 获取车辆类别
                h1_text = soup.find('h1').text
                vehicle_type = ''.join(
                    [char for char in list(h1_text) if
                     (char != ' ' and char != '\n' and char != '\r' and char != '\t')])
                if vehicle_type == '重型柴油车环保信息':
                    record = parsePage.parse_paeg_zxcyc(soup)
                elif vehicle_type == '轻型汽油车环保信息':
                    record = parsePage.parse_paeg_qxqyc(soup)
                elif vehicle_type == '重型燃气车环保信息':
                    record = parsePage.parse_paeg_zxrqc(soup)
                elif vehicle_type == '摩托车环保信息':
                    record = parsePage.parse_paeg_motor(soup)
                elif vehicle_type == '轻型汽车混合动力车环保信息':
                    record = parsePage.parse_paeg_qxqchhdl(soup)
                elif vehicle_type == '非道路移动机械(柴油)环保信息':
                    record = parsePage.parse_paeg_fdlydjx_cy(soup)
                elif vehicle_type == '轻型两用燃料车环保信息':
                    record = parsePage.parse_paeg_qxlyrlc(soup)
                elif vehicle_type == '电动车环保信息':
                    record = parsePage.parse_paeg_ddc(soup)
                elif vehicle_type == '轻型柴油车环保信息':
                    record = parsePage.parse_paeg_qxcyc(soup)
                elif vehicle_type == '轻便摩托车环保信息':
                    record = parsePage.parse_paeg_qbmotor(soup)
                elif vehicle_type == '重型柴油混合动力车环保信息':
                    record = parsePage.parse_paeg_zxcyhhdlc(soup)
                elif vehicle_type == '环保信息':
                    record = parsePage.parse_paeg_hb(soup)
                elif vehicle_type == '重型汽油车环保信息':
                    record = parsePage.parse_paeg_zxqyc(soup)
                elif vehicle_type == '重型甲醇燃料汽车环保信息':
                    record = parsePage.parse_paeg_zxjcrlqc(soup)
                elif vehicle_type == '城市车辆重型柴油车环保信息':
                    record = parsePage.parse_paeg_csclzxcyc(soup)
                elif vehicle_type == '非道路移动机械柴油机环保信息':
                    record = parsePage.parse_paeg_fdlydjx_cyj(soup)
                elif vehicle_type == '轻型燃气车环保信息':
                    record = parsePage.parse_paeg_qxrqc(soup)
                elif vehicle_type == '重型燃气混合动力车环保信息':
                    record = parsePage.parse_paeg_zxrqhhdlc(soup)
                elif vehicle_type == '轻型混合动力环保信息':
                    record = parsePage.parse_paeg_qxhhdl(soup)
                else:
                    raise Exception('新的车辆类型')

                record['CLLB'] = vehicle_type
                print(record)

            except Exception as e:
                print('无法读取:', detail_url)
                print(e)

        # 每一页结束之后写入文件
    except Exception as e:
        print(e)


if __name__ == '__main__':
    gh_data_spider()
