# -*- coding: utf-8 -*-
# @Time    : 2021/7/14 17:33
# @Author  : aiyingyi
# @file_name: spiderUtils.py
# @Software: PyCharm

import requests
import base64
import zlib
from configparser import RawConfigParser
import os
import re
import execjs
import json
import hashlib
from requests.utils import add_dict_to_cookiejar
import xlwt
from xlutils.copy import copy
import xlrd
import os.path
from bs4 import BeautifulSoup
from pathlib import Path

"""
    工具类
"""


class utils:
    # 定义session
    single_session = None
    # 定义请求头
    headers = {
        'Host': 'www.miit.gov.cn',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.miit.gov.cn/datainfo/dljdclscqyjcpgg/xcpgs346/index.html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    # 将数据先经过deflate压缩，然后使用base64编码
    @classmethod
    def encode(cls, data):
        res = base64.b64encode(zlib.compress(data.encode()))
        return str(res)[2:-1]

    # 将数据先经过base64解码然后再解压缩
    @classmethod
    def decode(cls, data):
        return zlib.decompress(base64.b64decode(data))

    # 加载配置文件，配置文件与执行的py文件在同一目录下
    @classmethod
    def get_config(cls, config_name):
        conn = RawConfigParser()
        file_path = os.path.join(os.path.abspath('.'), 'config.ini')
        if not os.path.exists(file_path):
            raise FileNotFoundError("文件不存在")
        conn.read(file_path, encoding='utf-8')
        value = conn.get('api', config_name)
        return value

    @classmethod
    def getCookie(cls, data):
        """
        通过加密对比得到正确cookie参数,用以生成jsl_clearance_s函数
        :param data: 参数
        :return: 返回正确cookie参数
        """
        chars = len(data['chars'])
        for i in range(chars):
            for j in range(chars):
                clearance = data['bts'][0] + data['chars'][i] + data['chars'][j] + data['bts'][1]
                encrypt = None
                if data['ha'] == 'md5':
                    encrypt = hashlib.md5()
                elif data['ha'] == 'sha1':
                    encrypt = hashlib.sha1()
                elif data['ha'] == 'sha256':
                    encrypt = hashlib.sha256()
                encrypt.update(clearance.encode())
                result = encrypt.hexdigest()
                if result == data['ct']:
                    return clearance

    # 返回请求页面的内容，使用单例session

    @classmethod
    def get_page_by_singlesession(cls, url):
        if utils.single_session is None:
            # 使用session保持会话
            utils.single_session = requests.session()
            res1 = utils.single_session.get(url, headers=utils.headers)
            jsl_clearance_s = re.findall(r'cookie=(.*?);location', res1.text)[0]
            # 执行js代码
            jsl_clearance_s = str(execjs.eval(jsl_clearance_s)).split('=')[1].split(';')[0]
            # add_dict_to_cookiejar方法添加cookie
            add_dict_to_cookiejar(utils.single_session.cookies, {'__jsl_clearance_s': jsl_clearance_s})
            res2 = utils.single_session.get(url, headers=utils.headers)
            # 提取go方法中的参数
            data = json.loads(re.findall(r';go\((.*?)\)', res2.text)[0])
            jsl_clearance_s = utils.getCookie(data)
            # 修改cookie
            add_dict_to_cookiejar(utils.single_session.cookies, {'__jsl_clearance_s': jsl_clearance_s})
        return utils.single_session.get(url, headers=utils.headers).text

    # 返回页面内容,这里面每次请求都会生成一个session
    @classmethod
    def get_page(cls, url):

        # 使用session保持会话
        session = requests.session()
        res1 = session.get(url, headers=utils.headers)
        jsl_clearance_s = re.findall(r'cookie=(.*?);location', res1.text)[0]
        # 执行js代码
        jsl_clearance_s = str(execjs.eval(jsl_clearance_s)).split('=')[1].split(';')[0]
        # add_dict_to_cookiejar方法添加cookie
        add_dict_to_cookiejar(session.cookies, {'__jsl_clearance_s': jsl_clearance_s})
        res2 = session.get(url, headers=utils.headers)
        # 提取go方法中的参数
        data = json.loads(re.findall(r';go\((.*?)\)', res2.text)[0])
        jsl_clearance_s = utils.getCookie(data)
        # 修改cookie
        add_dict_to_cookiejar(session.cookies, {'__jsl_clearance_s': jsl_clearance_s})
        return session.get(url, headers=utils.headers).text

    '''
         获取公示数据新产品以及变更扩展的列表页的连接
    '''

    @classmethod
    # 处理列表页，获取详情页对应的连接
    def parse_list_page(page_text):
        if page_text is not None:
            # 将页面内容转换成json
            page_dict = json.loads(page_text)
            # 获取响应的html代码
            html = page_dict['data']['html']
            # 解析页面，获取当前页面的所有详情页连接
            soup = BeautifulSoup(html, 'html.parser')
            href_list = soup.findAll('a')
            result = []
            if href_list is not None and len(href_list) != 0:
                # 去除重复的内容，并获取href属性
                count = int(len(href_list) / 5)
                for i in range(0, count):
                    result.append(href_list[i * 5]['href'])
            return result

    # 新增Excel并添加数据
    @classmethod
    def write_to_excel(cls, result, file_name):
        '''
        将数据存储到excel中。
        :param result: 保存数据的list    [{},{}]格式
        :return:
        '''
        try:
            # 1、创建工作薄
            work_book = xlwt.Workbook(encoding='utf-8')
            # 2、创建sheet表单
            sheet = work_book.add_sheet("sheet1")
            # 3、写表头
            head = []
            for k in result[0].keys():
                head.append(k)

            for i in range(len(head)):
                sheet.write(0, i, head[i])
            # 4、添加内容
            # 行号
            i = 1
            for item in result:
                for j in range(len(head)):
                    sheet.write(i, j, item[head[j]])
                # 写完一行，将行号+1
                i += 1
            # 保存
            work_book.save(file_name)
            print('写入excel成功！')
        except Exception as e:
            print(e)
            print('写入excel失败！', e)

    # 追加内容到Excel
    @classmethod
    def append_to_excel(self, result, file_name):
        '''
        追加数据到excel
        :param result: 【item】 [{},{}]格式
        :param file_name: 文件名
        :return:
        '''
        try:
            workbook = xlrd.open_workbook(file_name)  # 打开工作簿
            sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
            worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
            rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
            new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
            new_worksheet = new_workbook.get_sheet(0)
            # 获取表头信息
            heads = worksheet.row_values(0)
            i = rows_old
            for item in result:
                for j in range(len(heads)):
                    new_worksheet.write(i, j, item[heads[j]])
                i += 1
            new_workbook.save(file_name)
            print('追加成功！')
        except Exception as e:
            print('追加失败！', e)

    # 判断文件是否存在
    @classmethod
    def checkFile(cls, file_name):
        if Path(file_name).exists():
            return '1'
        else:
            return '0'

    # 数据保存到Excel
    @classmethod
    def saveData(cls, data_list, file_name):
        # 判断文件是否存在，不存在就创建创建
        myfile = Path(file_name)
        if myfile.exists():
            utils.append_to_excel(data_list, file_name)
        else:
            utils.write_to_excel(data_list, file_name)
