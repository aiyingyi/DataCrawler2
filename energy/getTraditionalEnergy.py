#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 9:21
# @Author  : aiyingyi
# @FileName: getEnergy.py
# @Software: PyCharm


"""
 爬取网站链接  https://yhgscx.miit.gov.cn/fuel-consumption-web/mainPage
 传统能源能耗数据爬取
"""

import requests

from tkinter import messagebox

import xlrd
import xlwt
from pathlib import Path
from xlutils.copy import copy


class WorkInformation():

    fileName = "D:/油耗-传统能源.xls"
    totalPage = 7000# 抓取数据的总页码数
    pageSize = 10
    searchText = ""
    reportType = 1  # 指定是获取新能源还是传统能源  1 传统能源汽车油耗数据
    columnName = ['driveType', 'maximumDesignMass', 'peakPower', 'vehicleQuality',
                  'comprehensiveConditionsFuelConsumptionBelowLimit', 'leadingValue', 'limitValue',
                  'comprehensiveConditions', 'otherInfo', 'uniqId']

    def __init__(self):
        # 获取列表的查询条件地址
        self.query_url = "https://yhgscx.miit.gov.cn/fuel-consumption-center/fcSearchCtr/queryList"
        self.query_Detail_Url = 'https://yhgscx.miit.gov.cn/fuel-consumption-center/fcSearchCtr/queryDetail'
        self.header = {
            "Content-Type": "application/json;charset=UTF-8",
            'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        }

    # 新增Excel并添加数据
    def write_to_excel(self, result, file_name):
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
                if k != 'workConditionVos':
                    head.append(k)
            for i in range(len(head)):
                sheet.write(0, i, head[i])
            # 4、添加内容
            # 行号
            i = 1
            for item in result:
                # 删除多余的字段
                del item['workConditionVos']
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
    def checkFile(cls, file_name):
        if Path(file_name).exists():
            return '1'
        else:
            return '0'

    # 数据保存到Excel
    def saveData(self, data_list, file_name):
        # 判断文件是否存在，不存在就创建创建
        myfile = Path(file_name)
        if myfile.exists():
            self.append_to_excel(data_list, file_name)
        else:
            self.write_to_excel(data_list, file_name)

    # 获取分页获取的信息
    def getDataList(self, pageNo):
        data = {
            "currentPage": pageNo,
            "position": "right",
            "reportType": self.reportType,
            "searchText": self.searchText,
            "pageSize": self.pageSize
        }
        resp = requests.post(self.query_url, json=data, headers=self.header)
        # 解析返回的结果
        obj = resp.json()
        if (obj["result"] == 1):
            return obj["info"]["list"]
        else:
            # 获取失败就提示，然后退出程序
            messagebox.showinfo("提示", obj["info"])
            return
        return ""

    # 获取详细信息
    def getDataDetail(self, item, data1):
        dict = {}
        req = requests.post(self.query_Detail_Url, json=data1, headers=self.header)
        resp = req.json()
        objDetail = resp["info"]
        # key是索引位置，value是原来的key
        for key, value in enumerate(objDetail):
            dict[value] = objDetail[value]
            item.update(dict)
        print("详情获取完成！")

    def getdata(self):
        for pageNo in range(1477, self.totalPage):
            # 获取分页数据
            oriListData = self.getDataList(pageNo)
            listData = []

            # 过滤掉有问题的数据
            for item in oriListData:
                if item['oversrasName'] != '去除不爬取的公司':
                    listData.append(item)

            for item in listData:
                data1 = {
                    "applyId": item["applyId"]
                }
                # 获取详细数据
                self.getDataDetail(item, data1)


            # 保存数据
            self.saveData(listData, self.fileName)
            print('第',pageNo,'页写入完成')


if __name__ == "__main__":
    dpf = WorkInformation()
    dpf.getdata()
