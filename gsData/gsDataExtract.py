# -*- coding: utf-8 -*-

'''
  公示数据新产品爬取
'''

import ast
import json
from bs4 import BeautifulSoup
import re
from utils.spiderUtils import utils


# 解析第一次请求的列表页，获取数据总条数
def get_count(page_text):
    if page_text is not None:
        # 将页面内容转换成json
        page_dict = json.loads(page_text)
        # 获取响应的html代码
        html = page_dict['data']['html']
        # 解析页面
        soup = BeautifulSoup(html, 'html.parser')
        # 获取总条数以及总页码
        query_data = soup.find('div', id='WsyOZQ_pagination').get('querydata')
        # 转换成dict
        count = ast.literal_eval(query_data)
        return count


# 解析详情页数据
def parse_detail_page(page_text):
    data = {}
    soup = BeautifulSoup(page_text, 'html.parser')
    tbody_list = soup.find('div', id='zoom').find_all('tbody')
    # 解析第一个tbody标签
    td_list = tbody_list[0].findAll('td')
    data['CPSB'] = td_list[0].text
    data['CPXH'] = td_list[1].text
    data['CPMC'] = td_list[2].text
    data['QYMC'] = td_list[3].text
    data['SCDZ'] = td_list[6].text
    # 解析第二个tbody
    td_list = tbody_list[1].findAll('td')
    # 解析尺寸
    size = re.split('[长宽高]：', td_list[0].text)[1:4]
    data['CHANG'] = size[0]
    data['KUAN'] = size[1]
    data['GAO'] = size[2]
    # 解析货厢长宽高
    size = re.split('[长宽高]：', td_list[1].text)[1:4]

    data['HXC'] = size[0]
    data['HXK'] = size[1]
    data['HXG'] = size[2]

    data['YJBZ'] = td_list[2].text
    data['RLZL'] = td_list[3].text

    data['ZZHL'] = td_list[6].text
    data['EDZL'] = td_list[7].text
    data['ZXXS'] = td_list[8].text
    data['ZBZL'] = td_list[9].text

    data['ZHSH'] = td_list[10].text
    data['GCZL'] = td_list[11].text

    data['ZHJ'] = td_list[12].text

    data['LTGG'] = td_list[13].text
    data['THPS'] = td_list[14].text
    data['BGAZ'] = td_list[15].text
    data['LTS'] = td_list[16].text
    data['QPCK'] = td_list[17].text
    data['EDZK'] = td_list[18].text

    # 提取轮距文本的数字
    qlj = ''
    hlj = ''
    arr = td_list[19].text.split(':')
    if len(arr) == 3:
        hlj = arr[2]
    elif len(arr) == 2:
        qlj_number = re.findall(r"\d+\.?\d*", arr[1])
        if len(qlj_number) == 1:
            qlj = qlj_number[0]
    # axle_track = re.findall(r"\d+\.?\d*", td_list[19].text)
    data['QLJ'] = qlj
    data['HLJ'] = hlj
    data['JJLQJ'] = td_list[20].text
    data['BSQY'] = td_list[21].text
    data['BSXH'] = td_list[22].text
    data['BSSB'] = td_list[23].text
    data['FBSZD'] = td_list[24].text
    data['SBDH'] = td_list[25].text
    data['QXHX'] = td_list[26].text
    data['QT'] = td_list[27].text

    td_list = tbody_list[2].findAll('td')
    data['DPID'] = td_list[1].text
    data['DPXH'] = td_list[2].text
    data['DPLB'] = td_list[4].text

    td_list = tbody_list[3].findAll('td')
    data['FDJ'] = td_list[0].text
    data['FQY'] = td_list[1].text
    data['FPL'] = td_list[2].text
    data['FGL'] = td_list[3].text
    data['YH'] = td_list[4].text
    return data


# 爬取公示数据新产品到excel
def new_product_spider():
    # 获取首次请求的完整url
    url = utils.get_config('new_product_url')
    page_size = int(utils.get_config('pageSize'))
    # 获取url的前缀和后缀，用于将pageNo替换掉更换url
    prefix = utils.get_config('new_product_url_prefix')
    suffix = utils.get_config('new_product_url_suffix')
    # 获取批次信息
    pc = utils.get_config('pc')
    # 获取总的数据条数
    count = int(get_count(utils.get_page(url))['count'])
    # 计算出总页数
    pageCount = int(count / page_size) + 1

    for pageNo in range(1, pageCount + 1):
        # 获取当前列表页连接集合
        print("第%d页,共%d页" % (pageNo, pageCount))
        page_text = utils.get_page(prefix + str(pageNo) + suffix)
        print(page_text)
        link_list = utils.parse_list_page(page_text)

        result = []
        for link in link_list:
            print(link)
            data = parse_detail_page(utils.get_page('https://www.miit.gov.cn' + link))
            data['pc'] = pc
            result.append(data)
        utils.saveData(result, 'E:/产品准入公示数据_新产品_第' + pc + '批.xls')

    # utils.write_to_excel(result, 'E:/产品准入公示数据_新产品_第' + pc + '批.xls')


if __name__ == '__main__':
    new_product_spider()
