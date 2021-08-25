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

start_date = '2000-07-01 00:00:00.0'

data = {
    'page': 1,
    'scqy': '公司',
    'x': 81,
    'y': 25
}


# 定义数据模板
def get_data_model():
    return {
        'CLLB': '',
        'XXGKBH': '',
        'CNSM': '',
        'CLXH': '',
        'BRAND': '',
        'QCFL': '',
        'MTCLB': '',
        'QBMTCLB': '',
        'PFJD': '',
        'CXSBFF_WZ': '',
        'CLMPWZ': '',
        'OBDJKWZ': '',
        'JZZL': '',
        'PQGKWZ': '',
        'PQGKCX': '',
        'CLZZSMC': '',
        'SCCDZ': '',
        'FDJXH': '',
        'FDJZZSMC': '',
        'FDJSCCDZ': '',
        'FDJCP': '',
        'FDJXZMC': '',
        'XSJYXX': '',
        'DDJXH_SCC': '',
        'FDJXH_SCQY': '',
        'ZCKZQXH_BB_SCC': '',
        'CNZZXH_SCC': '',
        'DCRL_XHLC': '',
        'CHZHQXH_SCQY': '',
        'CHZHQTC_ZT_FZSCQY': '',
        'KLBZQ_CGPF_XH_SCQY': '',
        'KLBZQ_CGPF_TC_ZT_FZSCQY': '',
        'TGXH_SCQY': '',
        'YCGQXH_SCQY': '',
        'QZXPFKZZZXH_SCQY': '',
        'EGRXH_SCQY': '',
        'OBDXYGYS': '',
        'ECUXH_SCQY': '',
        'BSQXS_DWS': '',
        'XSQXH_SCQY': '',
        'ZYQXH_SCQY': '',
        'ZLQXS': '',
        'ZDJGL_ZS': '',
        'EDGL_ZS': '',
        'ZDJNJ_ZS': '',
        'RLGJXTXS': '',
        'PYBXH_SCQY': '',
        'PYQXH_SCQY': '',
        'GGGXH_SCQY': '',
        'PQHCLXTXS': '',
        'CHZHQ_DOC_XH_SCQY': '',
        'CHZHQ_DOC_FZ_ZT_TCSCQY': '',
        'CHZHQ_SCR_XH_SCQY': '',
        'CHZHQ_SCR_FZ_ZT_TCSCQY': '',
        'CHZHQ_ASC_XH_SCQY': '',
        'CHZHQ_ASC_FZ_ZT_TCSCQY': '',
        'CHZHQ_LNT_XH_SCQY': '',
        'CHZHQ_LNT_FZ_ZT_TCSCQY': '',
        'KLBZQ_DPF_XH_SCQY': '',
        'KLBZQ_DPF_TC_ZT_FZSCQY': '',
        'ZFQHYLTJQXH_SCQY': '',
        'HHZHXH_SCQY': '',
        'PSQXH_SCQY': '',
        'PQXSQXH_SCQY': '',
        'CHZHQ_SY_XH_SCQY': '',
        'CHZHQ_SY_FZ_ZT_TCSCQY': '',
        'DJXH_SCQY': '',
        'NLCCZZXH_SCQY': '',
        'DCRL_CLCDXHLC': '',
        'DYHWZHQXH_SCQY': '',
        'DYHWZHQFZ_ZT_TCSCQY': '',
        'DCRL_CLCDDXSLC': '',
        'KLBZQXH_SCQY': '',
        'KLBZQTC_ZT_FZSCQY': '',
        'PSB_YLTJQXH_SCQY': '',
        'PSQXH_SCC': '',
        'ECUXH_BB_SCC': '',
        'RYZFWRWXH_SCC': '',
        'KQLQQXH_SCC': '',
        'JQXSQXH_SCC': '',
        'KQPSZZXH_SCC': '',
        'RYZFZZXH_SCC': '',
        'FQZXHZZXH_SCC': '',
        'ZSXTLX_SCC': '',
        'XZXCHZHQSCRXH_SCC': '',
        'XRDYHWBJQXH_SCC': '',
        'WRKZJSXXBZ': '',
        'FRDB': '',
        'ADDRESS': '',
        'LXDH': '',
        'XXGKSJ': ''
    }
# 定义中文字段和数据库字段的映射
attribute_map = {
    '车辆类别':'CLLB',
    '信息公开编号':'XXGKBH',
    '承诺声明':'CNSM',
    '车辆型号':'',
    '商标':'',
    '车辆铭牌位置':'',
    '汽车分类':'',
    '车型的识别方法和位置':'',
    '车辆识别方法和位置':'',
    'OBD接口位置':'',
    '排放阶段':'',
    '排气管口位置':'',
    '车辆制造商名称':'',
    '排气管口朝向':'',
    '发动机型号':'',
    '制造商名称':'',
    '系族名称':'',
    '厂牌':'',
    '最大净功率/转速（kW/r/min）':'',
    '最大净扭矩/转速（Nm/r/min）':'',
    '燃料供给系统型式':'',
    '催化转换器型号/生产厂':'',
    '催化转化器型号/生产厂':'',
    '氧传感器型号/生产厂':'',
    '喷射泵或压力调节器型号/生产厂':'',
    '喷射器型号/生产厂':'',
    '增压器型号/生产厂':'',
    '中冷器型式':'',
    'ECU型号/版本号/生产厂':'',
    'OBD型号/生产厂':'',
    'EGR型号/生产厂':'',
    '曲轴箱污染物排放控制装置型号/生产厂':'',
    '燃油蒸发污染物排放控制装置型号/生产厂':'',
    '燃油蒸发装置型号/生产厂':'',
    '空气滤清器型号/生产厂':'',
    '进气消声器型号/生产厂':'',
    '排气消声器型号/生产厂':'',
    '消声器型号/生产厂':'',
    '废气再循环装置型号/生产厂':'',
    '摩托车类别':'',
    '颗粒捕集器型号/生产厂':'',
    '发动机型号/生产厂':'',
    '发动机型号/生产企业':'',
    '喷油器型号/生产厂':'',
    '再生系统类型/生产厂':'',
    '选择性催化转化器SCR型号/生产厂':'',
    '稀燃氮氧化物捕集器型号/生产厂':'',
    '电动机型号/生产厂':'',
    '整车控制器型号/版本号/生产厂':'',
    '储能装置型号/生产厂':'',
    '电池容量/续航里程':'',
    '基准质量':'',


}


# 时间字符串的比较
def compare_time(time1, time2):
    s_time = time.mktime(time.strptime(time1, '%Y-%m-%d'))
    e_time = time.mktime(time.strptime(time2, '%Y-%m-%d'))
    return int(s_time) - int(e_time)


# 去掉字符串的\n,\t,空格,\r
def trim_str(s):
    if s != None:
        return ''.join(
            [char for char in list(s) if (char != ' ' and char != '\n' and char != '\r' and char != '\t')])


# 根据bbh信息，解析对应的页面
def parse_detail(sbbh):
    url = 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=' + sbbh + '&isprotect=false'
    page_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page_text, 'html.parser')
    h1_text = soup.find('h1').text
    vehicle_category = trim_str(h1_text)


# 解析第一种模板内容,以重型汽油车为例  http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=9ea2156a81d7d5b389d4de5a447dab1befd519426e7bb918&isprotect=false
def parse_paeg_model1(soup):
    res = get_data_model();
    res['XXGKBH'] = trim_str(soup.select('.talignc')[0].text.split(':')[1])
    res['CNSM'] = trim_str(soup.select('p')[1].text)
    tables = soup.select('.list-table.tab')

    # 1. 车辆信息
    tds = tables[0].findAll('td')
    res['CLXH'] = tds[1].text
    res['BRAND'] = tds[3].text
    res['QCFL'] = tds[5].text
    res['PFJD'] = tds[7].text
    res['CXSBFF_WZ'] = tds[9].text
    res['CLZZSMC'] = tds[11].text
    res['SCCDZ'] = tds[13].text

    # 2. 发动机信息
    tds = tables[1].findAll('td')
    res['FDJXH'] = tds[1].text
    res['FDJZZSMC'] = tds[3].text
    res['FDJXZMC'] = tds[5].text
    location = tds[7].text
    res['FDJSCCDZ'] = trim_str(location)
    res['FDJCP'] = tds[9].text

    # 3. 型式信息检验
    trs = tables[2].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 4. 污染控制技术信息
    tds = tables[3].findAll('td')
    res['ZDJGL_ZS'] = tds[1].text
    res['ZDJNJ_ZS'] = tds[3].text
    res['RLGJXTXS'] = tds[5].text
    res['CHZHQXH_SCQY'] = tds[7].text
    res['CHZHQTC_ZT_FZSCQY'] = tds[9].text
    res['YCGQXH_SCQY'] = tds[11].text
    res['PSB_YLTJQXH_SCQY'] = tds[13].text
    res['PSQXH_SCC'] = tds[15].text
    res['ZYQXH_SCQY'] = tds[17].text
    res['ZLQXS'] = tds[19].text
    res['ECUXH_BB_SCC'] = tds[21].text
    # res[''] = tds[23].text     # OBD生产厂
    res['EGRXH_SCQY'] = tds[25].text
    res['QZXPFKZZZXH_SCQY'] = tds[27].text
    res['RYZFWRWXH_SCC'] = tds[29].text
    res['KQLQQXH_SCC'] = tds[31].text
    res['JQXSQXH_SCC'] = tds[33].text
    res['PQXSQXH_SCQY'] = tds[35].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]
    return res

def gh_data_spider():
    url = 'https://www.cn-truck.com/gonggao/listhbres'
    data['limit'] = 1
    resp_json = json.loads(requests.post(url, headers=headers, data=data).text)
    # 获取页面大小
    count = int(resp_json.get('count'))
    pageCount = int(count / pageSize) + 1
    data['limit'] = pageSize

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
        for sbbh in sbbh_list[0:10]:
            print(sbbh)
            res = parse_detail(sbbh)
        # 每一页结束之后写入文件
        # utils.saveData(result, 'E:/车辆类别信息.xls')

if __name__ == '__main__':
    pass
