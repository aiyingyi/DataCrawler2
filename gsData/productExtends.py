#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 9:55
# @Author  : aiyingyi
# @FileName: productExtends.py
# @Software: PyCharm

from utils.spiderUtils import utils
import json
from bs4 import BeautifulSoup
import ast

'''
    产品变更扩展数据爬取
'''

# 定义变更项名称与数据库表中字段名的映射关系
key_map = {
    '防抱死制动系统': 'FBSZD',
    '排放依据标准': 'YJBZ',
    '半挂车鞍座最大允许承载质量': 'BGAZ',
    '前轮距': 'QLJ',
    '反光标识商标': 'BSSB',
    '发动机功率': 'FGL',
    '底盘型号': 'DPXH',
    '发动机': 'FDJ',
    '准拖挂车总质量': 'GCZL',
    '其它': 'QT',
    '整备质量': 'ZBZL',
    '后轮距': 'HLJ',
    '反光标识生产企业': 'BSQY',
    '轴数': 'ZHSH',
    '燃料种类': 'RLZL',
    '宽': 'KAUN',
    '发动机排量': 'FPL',
    '底盘标识': 'DPID',
    '轮胎规格': 'LTGG',
    '额定质量': 'EDZL',
    '驾驶室准乘人数': 'QPCK',
    '高': 'GAO',
    '货箱长': 'HXC',
    '总质量': 'ZZL',
    '底盘企业': 'DPXHANDQY',
    '货箱宽': 'HXK',
    '长': 'CHANG',
    '底盘类别': 'DPLB',
    '反光标识型号': 'BSXH',
    '最高车速': 'ZGCS',
    '弹簧片数': 'THPS',
    '载质量利用系数': 'ZZHL',
    '轮胎数': 'LTS',
    '前悬后悬': 'QXHX',
    '接近离去角': 'JJLQJ',
    '额定载客含驾驶员座位数': 'EDZK',
    '货箱高': 'HXG',
    '制动方式前轮': 'QLZDFS',
    '发动机企业': 'FQY',
    '识别代号': 'SBDH',
    '制动方式后轮': 'HLZDFS',
    '轴距': 'ZHJ'
}

# 每次爬取时，用以爬取变更项目的具体名称，从而完善 key_map
key_set = set()


# 返回一个数据模板对象,用以指定保存到excel中的数据模板
def get_dict_model():
    return {'CPXH': '', 'CPMC': '', 'CPSB': '', 'QYMC': '', 'PC': '', 'CHANG': '',
            'KUAN': '', 'GAO': '', 'RLZL': '', 'YJBZ': '', 'FPL': '',
            'FGL': '', 'ZXXS': '', 'HXC': '', 'HXK': '', 'HXG': '', 'ZHSH': '',
            'ZHJ': '', 'THPS': '', 'LTGG': '', 'LTS': '', 'QLJ': '', 'HLJ': '', 'ZZL': '', 'ZHH': '', 'EDZL': '',
            'ZBZL': '', 'GCZL': '', 'ZZHL': '', 'BGAZ': '', 'EDZK': '', 'QPCK': '', 'JJLQJ': '', 'QXHX': '',
            'ZGCS': '', 'FDJ': '', 'FQY': '', 'DPID': '', 'DPXH': '', 'DPLB': '', 'DPMC': '', 'YH': '',
            'SBDH': '', 'QT': '', 'FBSZD': '', 'BSQY': '', 'BSSB': '', 'BSXH': '', 'FBRQ': '', 'SCDZ': '',
            'CLXH': '', 'DPXHANDQY': '', 'SFMJ': '', 'TCRQ': '', 'TSRQ': '', 'EDZDZZL': '', 'QLZDFS': '', 'HLZDFS': '',
            'QLZDCZFS': '', 'HLZDCZFS': '', 'FDJSB': '', 'BDZS': '', 'CPH': ''}


def get_count(page_text):
    if page_text is not None:
        # 将页面内容转换成json
        page_dict = json.loads(page_text)
        # 获取响应的html代码
        html = page_dict['data']['html']
        # 解析页面
        soup = BeautifulSoup(html, 'html.parser')
        # 获取总条数以及总页码
        query_data = soup.find('div', id='autUDB_pagination').get('querydata')
        # 转换成dict
        count = ast.literal_eval(query_data)
        return count


# 解析详情页数据
def parse_detail_page(page_text):
    data = get_dict_model()
    # 提取基本信息
    soup = BeautifulSoup(page_text, 'html.parser')
    table_base_info = soup.select('.w_table')[0]
    tds = table_base_info.findAll('td')
    data['CPSB'] = tds[0].text
    data['CPXH'] = tds[1].text
    data['CPMC'] = tds[2].text
    data['QYMC'] = tds[3].text

    # 提取变更信息
    '''
      class属性有空格。空格为分隔符，表示该标签有多个class
      选择拥有多个class属性的标签中的子标签：soup.select('table.w_table.w_table2 > tbody > tr')
    '''
    trs = soup.select('table.w_table.w_table2 > tbody > tr')
    # 判断变更扩展项是否是爬取对象，去掉表头
    for index in range(1, len(trs)):
        tds = trs[index].findAll('td')
        key = get_key(tds[0].text)
        if key is not None:
            data[key] = tds[2].text
    return data


# 根据变更项的名字匹配数据库中对应的字段
def get_key(td_text):
    # 完善 key_map
    # key_set.add(td_text)
    if td_text in key_map.keys():
        return key_map[td_text]
    else:
        return None


def extends_spider():
    # 获取首次请求的完整url
    url = utils.get_config('extend_url')
    page_size = int(utils.get_config('pageSize'))
    # 获取url的前缀和后缀，用于将pageNo替换掉更换url
    prefix = utils.get_config('extend_url_prefix')
    suffix = utils.get_config('extend_url_suffix')
    # 获取批次信息
    pc = utils.get_config('pc')

    # 获取总的数据条数
    count = int(get_count(utils.get_page_by_singlesession(url))['count'])

    # 计算出总页数
    pageCount = int(count / page_size) + 1

    # 爬取数据
    for pageNo in range(1, pageCount + 1):
        # 获取当前列表页连接集合
        print('页码：', pageNo, '总页码：', pageCount)
        link_list = utils.parse_list_page(utils.get_page_by_singlesession(prefix + str(pageNo) + suffix))

        result = []
        for link in link_list:
            print(link)
            data = parse_detail_page(utils.get_page_by_singlesession('https://www.miit.gov.cn' + link))
            data['PC'] = pc
            data['report_type'] = '变更扩展'
            print(data)
            result.append(data)
        utils.saveData(result, 'F:/产品准入公示数据_变更扩展_第' + pc + '批.xls')

    '''
     write_to_excel是将字典的key值取出来作为excel表头，这就要求所有的字典对象都必须有相同的key
    '''
    # utils.write_to_excel(result, 'E:/产品准入公示数据_变更扩展_第' + pc + '批.xls')


if __name__ == '__main__':
    extends_spider()
