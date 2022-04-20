#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/8/25 10:18
# @Author  : aiyingyi
# @FileName: parsePage.py
# @Software: PyCharm


import requests
import time
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
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


# 1. 重型汽油车
def parse_paeg_zxqyc(soup):
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


# 2. 摩托车
def parse_paeg_motor(soup):
    res = get_data_model();
    res['XXGKBH'] = trim_str(soup.select('.talignc')[0].text.split(':')[1])
    res['CNSM'] = trim_str(soup.select('p')[1].text)
    tables = soup.select('.list-table.tab')

    # 1. 车辆信息
    tds = tables[0].findAll('td')
    res['CLXH'] = tds[1].text
    res['BRAND'] = tds[3].text

    res['MTCLB'] = tds[5].text
    res['PFJD'] = tds[7].text
    res['CXSBFF_WZ'] = tds[9].text
    res['CLZZSMC'] = tds[11].text
    res['SCCDZ'] = tds[13].text

    # 2. 型式信息检验
    trs = tables[1].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 3. 污染控制技术信息
    tds = tables[2].findAll('td')
    res['FDJXH_SCQY'] = tds[1].text
    res['PYQXH_SCQY'] = tds[3].text
    res['ECUXH_BB_SCC'] = tds[5].text
    res['YCGQXH_SCQY'] = tds[9].text
    res['CHZHQXH_SCQY'] = tds[11].text
    res['CHZHQTC_ZT_FZSCQY'] = tds[13].text
    res['KQPSZZXH_SCC'] = tds[15].text
    res['RYZFZZXH_SCC'] = tds[17].text
    res['KQLQQXH_SCC'] = tds[19].text
    res['JQXSQXH_SCC'] = tds[21].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[len(ptags) - 5].text.split(':')[1]
    res['ADDRESS'] = ptags[len(ptags) - 4].text.split(':')[1]
    res['LXDH'] = ptags[len(ptags) - 3].text.split(':')[1]
    h6Tages = soup.select('h6')
    res['XXGKSJ'] = h6Tages[len(h6Tages) - 1].text.split('：')[1]
    return res


# 3. 电动车环保信息
def parse_paeg_ddc(soup):
    res = get_data_model();
    res['XXGKBH'] = trim_str(soup.select('.talignc')[0].text.split(':')[1])
    res['CNSM'] = trim_str(soup.select('p')[1].text)
    tables = soup.select('.list-table.tab')

    # 1. 车辆信息
    tds = tables[0].findAll('td')
    res['CLXH'] = tds[1].text
    res['BRAND'] = tds[3].text
    res['QCFL'] = tds[5].text

    res['CXSBFF_WZ'] = tds[7].text
    res['CLZZSMC'] = tds[9].text

    res['SCCDZ'] = tds[11].text

    # 2. 型式信息检验
    trs = tables[1].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 3. 污染控制技术信息
    tds = tables[2].findAll('td')
    res['DDJXH_SCC'] = tds[1].text
    res['ZCKZQXH_BB_SCC'] = tds[3].text
    res['CNZZXH_SCC'] = tds[5].text
    res['DCRL_XHLC'] = tds[7].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[9].text.split('：')[1]
    return res


# 4. 轻型汽车混合动力车环保信息
def parse_paeg_qxqchhdl(soup):
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
    res['JZZL'] = tds[15].text

    # 2. 型式信息检验
    trs = tables[1].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 3. 污染控制技术信息
    tds = tables[2].findAll('td')
    res['FDJXH_SCQY'] = tds[1].text
    res['DDJXH_SCC'] = tds[3].text
    res['NLCCZZXH_SCQY'] = tds[5].text
    res['DCRL_CLCDDXSLC'] = trim_str(tds[7].text)
    res['CHZHQXH_SCQY'] = tds[9].text
    res['CHZHQTC_ZT_FZSCQY'] = tds[11].text
    res['KLBZQ_CGPF_XH_SCQY'] = tds[13].text
    res['KLBZQ_CGPF_TC_ZT_FZSCQY'] = tds[15].text
    res['TGXH_SCQY'] = tds[17].text
    res['YCGQXH_SCQY'] = tds[19].text
    res['QZXPFKZZZXH_SCQY'] = tds[21].text
    res['EGRXH_SCQY'] = tds[23].text
    res['OBDXYGYS'] = tds[25].text
    res['ECUXH_SCQY'] = tds[27].text
    res['BSQXS_DWS'] = tds[29].text
    res['XSQXH_SCQY'] = tds[31].text
    res['ZYQXH_SCQY'] = tds[33].text
    res['ZLQXS'] = tds[35].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[2].text.split(':')[1]
    res['ADDRESS'] = ptags[3].text.split(':')[1]
    res['LXDH'] = ptags[4].text.split(':')[1]
    res['XXGKSJ'] = ptags[19].text.split('：')[1]
    return res


# 5. 重型柴油车
def parse_paeg_zxcyc(soup):
    res = get_data_model();
    res['XXGKBH'] = trim_str(soup.select('.talignc')[0].text.split(':')[1])
    res['CNSM'] = trim_str(soup.select('p')[1].text)
    tables = soup.select('.list-table.tab')

    # 1. 车辆信息
    tds = tables[0].findAll('td')
    res['CLXH'] = tds[1].text
    res['SCCDZ'] = tds[3].text
    res['BRAND'] = tds[5].text
    res['CLMPWZ'] = tds[7].text
    res['QCFL'] = tds[9].text
    res['OBDJKWZ'] = tds[11].text
    res['PFJD'] = tds[13].text
    res['PQGKWZ'] = tds[15].text

    res['CLZZSMC'] = tds[17].text
    res['PQGKCX'] = tds[19].text

    # 2. 发动机信息
    tds = tables[1].findAll('td')
    res['FDJXH'] = tds[1].text
    res['FDJZZSMC'] = tds[3].text
    res['FDJSCCDZ'] = tds[5].text
    res['FDJCP'] = tds[7].text
    res['FDJXZMC'] = tds[9].text

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
    res['EDGL_ZS'] = tds[3].text
    res['ZDJNJ_ZS'] = tds[5].text
    res['RLGJXTXS'] = tds[7].text
    res['PYBXH_SCQY'] = tds[9].text
    res['PYQXH_SCQY'] = tds[11].text
    res['GGGXH_SCQY'] = tds[13].text
    res['ZYQXH_SCQY'] = tds[15].text
    res['ZLQXS'] = tds[17].text
    res['EGRXH_SCQY'] = tds[19].text
    res['QZXPFKZZZXH_SCQY'] = tds[21].text
    res['ECUXH_SCQY'] = tds[23].text
    res['OBDXYGYS'] = tds[25].text
    res['PQHCLXTXS'] = tds[27].text
    res['CHZHQ_DOC_XH_SCQY'] = tds[29].text
    res['CHZHQ_DOC_FZ_ZT_TCSCQY'] = trim_str(tds[31].text)

    res['CHZHQ_SCR_XH_SCQY'] = tds[33].text
    res['CHZHQ_SCR_FZ_ZT_TCSCQY'] = trim_str(tds[35].text)

    res['CHZHQ_ASC_XH_SCQY'] = tds[37].text
    res['CHZHQ_ASC_FZ_ZT_TCSCQY'] = trim_str(tds[39].text)
    res['CHZHQ_LNT_XH_SCQY'] = tds[41].text
    res['CHZHQ_LNT_FZ_ZT_TCSCQY'] = trim_str(tds[43].text)

    res['KLBZQ_DPF_XH_SCQY'] = tds[45].text
    res['CHZHQ_LNT_FZ_ZT_TCSCQY'] = trim_str(tds[47].text)
    res['PQXSQXH_SCQY'] = tds[49].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]
    return res


# 6. 环保信息
def parse_paeg_hb(soup):
    url = 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=' + '216a53fa21daa2ac838d0c0c89b2ba9ed12db3aadc7c433f' + '&isprotect=false'
    page_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(page_text, 'html.parser')

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
    res['PYBXH_SCQY'] = tds[7].text
    res['PYQXH_SCQY'] = tds[9].text
    res['ZYQXH_SCQY'] = tds[11].text
    res['ZLQXS'] = tds[13].text

    res['EGRXH_SCQY'] = tds[17].text
    res['ECUXH_BB_SCC'] = tds[19].text

    res['PQHCLXTXS'] = tds[25].text
    res['KQLQQXH_SCC'] = tds[27].text
    res['JQXSQXH_SCC'] = tds[29].text
    res['PQXSQXH_SCQY'] = tds[31].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]
    return res


# 7. 轻型汽油车环保信息
def parse_paeg_qxqyc(soup):
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
    res['CLMPWZ'] = tds[9].text
    res['CLZZSMC'] = tds[11].text
    res['SCCDZ'] = tds[13].text

    # 2. 型式信息检验
    trs = tables[1].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 3. 污染控制技术信息
    tds = tables[2].findAll('td')
    res['FDJXH_SCQY'] = tds[1].text
    res['CHZHQXH_SCQY'] = tds[3].text

    res['CHZHQTC_ZT_FZSCQY'] = tds[5].text

    res['RYZFWRWXH_SCC'] = trim_str(tds[7].text)
    res['YCGQXH_SCQY'] = tds[9].text
    res['QZXPFKZZZXH_SCQY'] = tds[11].text
    res['EGRXH_SCQY'] = tds[13].text
    res['OBDXYGYS'] = tds[15].text
    res['ECUXH_SCQY'] = tds[19].text
    res['BSQXS_DWS'] = tds[21].text
    res['XSQXH_SCQY'] = tds[23].text

    res['ZYQXH_SCQY'] = tds[25].text
    res['ZLQXS'] = tds[27].text



    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]
    return res


# 8. 重型燃气车环保信息
def parse_paeg_zxrqc(soup):
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
    res['FDJSCCDZ'] = tds[7].text
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
    res['YCGQXH_SCQY'] = tds[7].text
    res['ZFQHYLTJQXH_SCQY'] = tds[9].text
    res['HHZHXH_SCQY'] = tds[11].text
    res['PSQXH_SCQY'] = tds[13].text
    res['EGRXH_SCQY'] = tds[15].text
    res['ZYQXH_SCQY'] = tds[17].text
    res['ZLQXS'] = tds[19].text
    res['ECUXH_SCQY'] = tds[21].text
    res['QZXPFKZZZXH_SCQY'] = tds[25].text

    res['KQLQQXH_SCC'] = tds[27].text
    res['JQXSQXH_SCC'] = tds[29].text
    res['PQXSQXH_SCQY'] = tds[31].text
    res['PQHCLXTXS'] = tds[33].text
    res['PQHCLXTXS'] = tds[35].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]

    return res


# 9. 轻型两用燃料车环保信息
def parse_paeg_qxlyrlc(soup):
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
    res['OBDJKWZ'] = tds[15].text
    res['JZZL'] = tds[17].text

    # 2. 型式信息检验
    trs = tables[1].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 3. 污染控制技术信息
    tds = tables[2].findAll('td')
    res['FDJXH_SCQY'] = tds[1].text
    res['HHZHXH_SCQY'] = tds[3].text

    res['CHZHQXH_SCQY'] = tds[5].text
    res['CHZHQTC_ZT_FZSCQY'] = tds[7].text

    res['KLBZQXH_SCQY'] = trim_str(tds[9].text)
    res['KLBZQTC_ZT_FZSCQY'] = tds[11].text

    res['TGXH_SCQY'] = tds[13].text
    res['YCGQXH_SCQY'] = tds[15].text
    res['QZXPFKZZZXH_SCQY'] = tds[17].text
    res['EGRXH_SCQY'] = tds[19].text
    res['OBDXYGYS'] = tds[21].text
    res['ECUXH_SCQY'] = tds[23].text
    res['BSQXS_DWS'] = tds[25].text
    res['XSQXH_SCQY'] = tds[27].text
    res['ZYQXH_SCQY'] = tds[29].text
    res['ZLQXS'] = tds[31].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[2].text.split(':')[1]
    res['ADDRESS'] = ptags[3].text.split(':')[1]
    res['LXDH'] = ptags[4].text.split(':')[1]
    res['XXGKSJ'] = ptags[19].text.split('：')[1]
    return res


# 10. 轻型柴油车环保信息
def parse_paeg_qxcyc(soup):
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
    res['CLZZSMC'] = tds[9].text
    res['SCCDZ'] = tds[11].text
    res['CLMPWZ'] = tds[13].text
    res['OBDJKWZ'] = tds[15].text
    res['JZZL'] = tds[17].text

    # 2. 型式信息检验
    trs = tables[1].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 3. 污染控制技术信息
    tds = tables[2].findAll('td')
    res['RLGJXTXS'] = tds[1].text
    res['FDJXH_SCQY'] = tds[3].text
    res['PSBXH_SCQY'] = tds[5].text
    res['PSQXH_SCQY'] = tds[7].text
    res['ZYQXH_SCQY'] = tds[9].text
    res['ZLQXS'] = tds[11].text
    res['EGRXH_SCQY'] = tds[13].text
    res['QZXPFKZZZXH_SCQY'] = tds[15].text
    res['ECUXH_SCQY'] = tds[17].text
    res['ZFQHYLTJQXH_SCQY'] = tds[9].text
    res['HHZHXH_SCQY'] = tds[11].text
    res['PSQXH_SCQY'] = tds[13].text
    res['OBDXYGYS'] = tds[15].text
    res['CHZHQ_DOC_XH_SCQY'] = trim_str(tds[17].text)
    res['CHZHQ_DOC_FZ_ZT_TCSCQY'] = tds[19].text
    res['CHZHQ_SCR_XH_SCQY'] = trim_str(tds[21].text)
    res['CHZHQ_SCR_FZ_ZT_TCSCQY'] = tds[23].text
    res['DYHWZHQXH_SCQY'] = tds[25].text
    res['DYHWZHQFZ_ZT_TCSCQY'] = trim_str(tds[27].text)
    res['CHZHQ_ASC_XH_SCQY'] = trim_str(tds[29].text)
    res['CHZHQ_ASC_FZ_ZT_TCSCQY'] = trim_str(tds[31].text)
    res['KLBZQ_DPF_XH_SCQY'] = tds[33].text
    res['KLBZQ_DPF_TC_ZT_FZSCQY'] = tds[35].text
    res['XSQXH_SCQY'] = trim_str(tds[37].text)
    res['BSQXS_DWS'] = tds[39].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[2].text.split(':')[1]
    res['ADDRESS'] = ptags[3].text.split(':')[1]
    res['LXDH'] = ptags[4].text.split(':')[1]
    res['XXGKSJ'] = ptags[19].text.split('：')[1]
    return res


# 11. 轻便摩托车环保信息
def parse_paeg_qbmotor(soup):
    res = get_data_model();
    res['XXGKBH'] = trim_str(soup.select('.talignc')[0].text.split(':')[1])
    res['CNSM'] = trim_str(soup.select('p')[1].text)
    tables = soup.select('.list-table.tab')

    # 1. 车辆信息
    tds = tables[0].findAll('td')
    res['CLXH'] = tds[1].text
    res['BRAND'] = tds[3].text
    res['PFJD'] = tds[5].text
    res['CXSBFF_WZ'] = tds[7].text
    res['CLZZSMC'] = tds[9].text
    res['SCCDZ'] = tds[11].text

    # 2. 型式信息检验
    trs = tables[1].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 3. 污染控制技术信息
    tds = tables[2].findAll('td')
    res['FDJXH_SCQY'] = tds[1].text
    res['PYQXH_SCQY'] = tds[3].text
    res['ECUXH_BB_SCC'] = tds[5].text
    res['YCGQXH_SCQY'] = tds[9].text
    res['CHZHQXH_SCQY'] = tds[11].text
    res['CHZHQTC_ZT_FZSCQY'] = tds[13].text

    res['KQPSZZXH_SCC'] = tds[15].text
    res['RYZFZZXH_SCC'] = tds[17].text
    res['KQLQQXH_SCC'] = tds[19].text
    res['XSQXH_SCQY'] = tds[21].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = soup.select('h6')[2].text.split('：')[1]
    return res


# 12. 重型柴油混合动力车环保信息
def parse_paeg_zxcyhhdlc(soup):
    res = get_data_model();
    res['XXGKBH'] = trim_str(soup.select('.talignc')[0].text.split(':')[1])
    res['CNSM'] = trim_str(soup.select('p')[1].text)
    tables = soup.select('.list-table.tab')

    # 1. 车辆信息
    tds = tables[0].findAll('td')
    res['CLXH'] = tds[1].text
    res['SCCDZ'] = tds[3].text
    res['BRAND'] = tds[5].text
    res['CLMPWZ'] = tds[7].text
    res['QCFL'] = tds[9].text
    res['OBDJKWZ'] = tds[11].text
    res['PFJD'] = tds[13].text
    res['PQGKWZ'] = tds[15].text

    res['CLZZSMC'] = tds[17].text
    res['PQGKCX'] = tds[19].text

    # 2. 发动机信息
    tds = tables[1].findAll('td')
    res['FDJXH'] = tds[1].text
    res['FDJZZSMC'] = tds[3].text
    res['FDJSCCDZ'] = tds[5].text
    res['FDJCP'] = tds[7].text
    res['FDJXZMC'] = tds[9].text

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
    res['EDGL_ZS'] = tds[3].text
    res['ZDJNJ_ZS'] = tds[5].text
    res['DJXH_SCQY'] = tds[7].text
    res['NLCCZZXH_SCQY'] = tds[9].text
    res['DCRL_CLCDXHLC'] = tds[11].text
    res['RLGJXTXS'] = tds[13].text
    res['PYBXH_SCQY'] = tds[15].text
    res['PYQXH_SCQY'] = tds[17].text
    res['GGGXH_SCQY'] = tds[19].text
    res['ZYQXH_SCQY'] = tds[21].text
    res['ZLQXS'] = tds[23].text
    res['EGRXH_SCQY'] = tds[25].text
    res['QZXPFKZZZXH_SCQY'] = tds[27].text
    res['ECUXH_SCQY'] = tds[29].text
    res['OBDXYGYS'] = trim_str(tds[31].text)
    res['PQHCLXTXS'] = tds[33].text

    res['CHZHQ_DOC_XH_SCQY'] = trim_str(tds[35].text)
    res['CHZHQ_DOC_FZ_ZT_TCSCQY'] = tds[37].text

    res['CHZHQ_SCR_XH_SCQY'] = trim_str(tds[39].text)
    res['CHZHQ_SCR_FZ_ZT_TCSCQY'] = tds[41].text

    res['CHZHQ_ASC_XH_SCQY'] = trim_str(tds[43].text)
    res['CHZHQ_ASC_FZ_ZT_TCSCQY'] = tds[45].text

    res['CHZHQ_LNT_XH_SCQY'] = trim_str(tds[47].text)
    res['CHZHQ_LNT_FZ_ZT_TCSCQY'] = tds[49].text

    res['KLBZQ_DPF_XH_SCQY'] = tds[51].text
    res['KLBZQ_DPF_TC_ZT_FZSCQY'] = tds[53].text

    res['PQXSQXH_SCQY'] = tds[55].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]
    return res


# 13. 重型甲醇燃料汽车环保信息
def parse_paeg_zxjcrlqc(soup):
    res = get_data_model();
    res['XXGKBH'] = trim_str(soup.select('.talignc')[0].text.split(':')[1])
    res['CNSM'] = trim_str(soup.select('p')[1].text)
    tables = soup.select('.list-table.tab')

    # 1. 车辆信息
    tds = tables[0].findAll('td')
    res['CLXH'] = tds[1].text
    res['CXSBFF_WZ'] = tds[3].text
    res['BRAND'] = tds[5].text
    res['OBDJKWZ'] = tds[7].text
    res['QCFL'] = tds[9].text
    res['PQGKWZ'] = tds[11].text
    res['PFJD'] = tds[13].text
    res['PQGKCX'] = tds[15].text
    res['CLZZSMC'] = tds[17].text
    res['SCCDZ'] = tds[19].text

    # 2. 发动机信息
    tds = tables[1].findAll('td')
    res['FDJXH'] = tds[1].text
    res['FDJCP'] = tds[3].text

    res['FDJZZSMC'] = tds[5].text
    res['FDJXZMC'] = tds[7].text
    location = tds[9].text
    res['FDJSCCDZ'] = trim_str(location)

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
    res['RLGJXTXS'] = tds[1].text
    res['TGXH_SCQY'] = tds[3].text
    res['YCGQXH_SCQY'] = tds[5].text
    res['PYQXH_SCQY'] = tds[7].text
    res['ZYQXH_SCQY'] = tds[9].text
    res['EGRXH_SCQY'] = tds[11].text
    res['ECUXH_BB_SCC'] = tds[13].text
    res['OBDXYGYS'] = tds[15].text
    res['PQHCLXTXS'] = tds[17].text
    res['CHZHQ_SY_XH_SCQY'] = tds[19].text
    res['CHZHQ_SY_FZ_ZT_TCSCQY'] = tds[21].text

    res['CHZHQ_SCR_XH_SCQY'] = tds[23].text
    res['CHZHQ_SCR_FZ_ZT_TCSCQY'] = tds[25].text

    res['CHZHQ_ASC_XH_SCQY'] = tds[27].text
    res['CHZHQ_ASC_FZ_ZT_TCSCQY'] = tds[29].text
    res['PQXSQXH_SCQY'] = tds[31].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]
    return res


# 14. 城市车辆重型柴油车环保信息
def parse_paeg_csclzxcyc(soup):
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
    res['FDJSCCDZ'] = tds[7].text
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
    res['PYBXH_SCQY'] = tds[7].text
    res['PYQXH_SCQY'] = tds[9].text
    res['ZYQXH_SCQY'] = tds[11].text
    res['ZLQXS'] = tds[13].text

    res['EGRXH_SCQY'] = tds[17].text
    res['ECUXH_BB_SCC'] = tds[19].text

    res['PQHCLXTXS'] = tds[25].text
    res['KQLQQXH_SCC'] = tds[27].text
    res['JQXSQXH_SCC'] = tds[29].text
    res['PQXSQXH_SCQY'] = tds[31].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]
    return res


# 15. 非道路移动机械(柴油)环保信息
def parse_paeg_fdlydjx_cy(soup):
    res = get_data_model();
    res['XXGKBH'] = trim_str(soup.select('.talignc')[0].text.split(':')[1])
    res['CNSM'] = trim_str(soup.select('p')[1].text)
    tables = soup.select('.list-table.tab')

    # 1. 车辆信息
    tds = tables[0].findAll('td')
    res['CLXH'] = tds[1].text
    res['BRAND'] = tds[5].text
    res['QCFL'] = tds[7].text
    res['PFJD'] = tds[9].text
    res['CXSBFF_WZ'] = tds[11].text

    res['CLZZSMC'] = tds[17].text
    res['SCCDZ'] = tds[19].text

    # 2. 发动机信息
    tds = tables[1].findAll('td')
    res['FDJXH'] = tds[1].text
    res['FDJZZSMC'] = tds[3].text
    res['FDJXZMC'] = tds[5].text
    res['FDJSCCDZ'] = tds[9].text
    res['FDJCP'] = tds[11].text

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
    res['EDGL_ZS'] = tds[1].text
    res['ZDJNJ_ZS'] = tds[3].text
    res['RLGJXTXS'] = tds[5].text
    res['PYBXH_SCQY'] = tds[7].text
    res['PYQXH_SCQY'] = tds[9].text
    res['ZYQXH_SCQY'] = tds[11].text
    res['ZLQXS'] = tds[13].text
    res['EGRXH_SCQY'] = tds[15].text
    res['ECUXH_BB_SCC'] = tds[17].text

    res['PQHCLXTXS'] = tds[23].text
    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]
    return res


# 16. 非道路移动机械柴油机环保信息
def parse_paeg_fdlydjx_cyj(soup):
    res = get_data_model();
    res['XXGKBH'] = trim_str(soup.select('.talignc')[0].text.split(':')[1])
    res['CNSM'] = trim_str(soup.select('p')[1].text)
    tables = soup.select('.list-table.tab')

    # 1. 发动机信息
    tds = tables[0].findAll('td')
    res['FDJXH'] = tds[1].text
    res['FDJXZMC'] = tds[3].text
    res['FDJCP'] = tds[5].text
    res['PFJD'] = tds[7].text

    res['FDJZZSMC'] = tds[11].text
    res['FDJSCCDZ'] = tds[13].text

    # 2. 型式信息检验
    trs = tables[1].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 3. 污染控制技术信息
    tds = tables[2].findAll('td')
    res['EDGL_ZS'] = tds[1].text
    res['ZDJNJ_ZS'] = tds[3].text
    res['RLGJXTXS'] = tds[5].text
    res['PYBXH_SCQY'] = tds[7].text
    res['PYQXH_SCQY'] = tds[9].text
    res['ZYQXH_SCQY'] = tds[11].text
    res['ZLQXS'] = tds[13].text
    res['EGRXH_SCQY'] = tds[15].text
    res['ECUXH_BB_SCC'] = tds[17].text
    res['PQHCLXTXS'] = tds[19].text
    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]
    return res


# 17. 轻型燃气车环保信息
def parse_paeg_qxrqc(soup):
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
    res['CLZZSMC'] = tds[9].text
    res['SCCDZ'] = tds[11].text
    res['CLMPWZ'] = tds[13].text
    res['OBDJKWZ'] = tds[15].text
    res['JZZL'] = tds[17].text

    # 2. 型式信息检验
    trs = tables[1].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 3. 污染控制技术信息
    tds = tables[2].findAll('td')
    res['FDJXH_SCQY'] = tds[1].text
    res['HHZHXH_SCQY'] = tds[3].text

    res['CHZHQXH_SCQY'] = tds[5].text
    res['CHZHQTC_ZT_FZSCQY'] = tds[7].text

    res['KLBZQXH_SCQY'] = trim_str(tds[9].text)
    res['KLBZQTC_ZT_FZSCQY'] = tds[11].text

    res['YCGQXH_SCQY'] = tds[13].text
    res['QZXPFKZZZXH_SCQY'] = tds[15].text
    res['EGRXH_SCQY'] = tds[17].text
    res['OBDXYGYS'] = tds[19].text
    res['ECUXH_SCQY'] = tds[21].text
    res['BSQXS_DWS'] = tds[23].text
    res['XSQXH_SCQY'] = tds[25].text
    res['ZYQXH_SCQY'] = tds[27].text
    res['ZLQXS'] = tds[29].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[2].text.split(':')[1]
    res['ADDRESS'] = ptags[3].text.split(':')[1]
    res['LXDH'] = ptags[4].text.split(':')[1]
    res['XXGKSJ'] = ptags[19].text.split('：')[1]
    return res


# 18. 重型燃气混合动力车环保信息
def parse_paeg_zxrqhhdlc(soup):
    res = get_data_model();
    res['XXGKBH'] = trim_str(soup.select('.talignc')[0].text.split(':')[1])
    res['CNSM'] = trim_str(soup.select('p')[1].text)
    tables = soup.select('.list-table.tab')

    # 1. 车辆信息
    tds = tables[0].findAll('td')
    res['CLXH'] = tds[1].text
    res['SCCDZ'] = tds[3].text
    res['BRAND'] = tds[5].text
    res['CLMPWZ'] = tds[7].text
    res['QCFL'] = tds[9].text
    res['OBDJKWZ'] = tds[11].text
    res['PFJD'] = tds[13].text
    res['PQGKWZ'] = tds[15].text

    res['CLZZSMC'] = tds[17].text
    res['PQGKCX'] = tds[19].text

    # 2. 发动机信息
    tds = tables[1].findAll('td')
    res['FDJXH'] = tds[1].text
    res['FDJZZSMC'] = tds[3].text
    res['FDJSCCDZ'] = tds[5].text
    res['FDJCP'] = tds[7].text
    res['FDJXZMC'] = tds[9].text

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
    res['EDGL_ZS'] = tds[3].text
    res['ZDJNJ_ZS'] = tds[5].text
    res['DJXH_SCQY'] = tds[7].text
    res['NLCCZZXH_SCQY'] = tds[9].text
    res['DCRL_CLCDXHLC'] = tds[11].text

    res['RLGJXTXS'] = tds[13].text

    res['ZFQHYLTJQXH_SCQY'] = tds[15].text
    res['HHZHXH_SCQY'] = tds[17].text
    res['PSQXH_SCQY'] = tds[19].text

    res['EGRXH_SCQY'] = tds[21].text
    res['ZYQXH_SCQY'] = tds[23].text
    res['ZLQXS'] = tds[25].text

    res['QZXPFKZZZXH_SCQY'] = tds[27].text
    res['ECUXH_SCQY'] = tds[29].text
    res['OBDXYGYS'] = tds[31].text
    res['YCGQXH_SCQY'] = tds[33].text
    res['PQHCLXTXS'] = tds[35].text
    res['CHZHQ_SY_XH_SCQY'] = trim_str(tds[37].text)
    res['CHZHQ_SY_FZ_ZT_TCSCQY'] = tds[39].text

    res['CHZHQ_SCR_XH_SCQY'] = trim_str(tds[41].text)
    res['CHZHQ_SCR_FZ_ZT_TCSCQY'] = tds[43].text

    res['CHZHQ_ASC_XH_SCQY'] = trim_str(tds[45].text)
    res['CHZHQ_ASC_FZ_ZT_TCSCQY'] = trim_str(tds[47].text)
    res['CHZHQ_LNT_XH_SCQY'] = tds[49].text
    res['CHZHQ_LNT_FZ_ZT_TCSCQY'] = trim_str(tds[51].text)
    res['PQXSQXH_SCQY'] = tds[53].text

    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]

    return res

# 19. 轻型混合动力环保信息
def parse_paeg_qxhhdl(soup):
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

    # 2. 型式信息检验
    trs = tables[1].findAll('tr')
    info = ''
    for index in range(1, len(trs)):
        tds = trs[index].select('td')
        info = info + ('依据标准' + str(index) + ':' + trim_str(tds[0].text) + ',')
        info = info + ('检测机构' + str(index) + ':' + trim_str(tds[1].text) + ',')
        info = info + ('检测结论' + str(index) + ':' + trim_str(tds[2].text) + ';')
    res['XSJYXX'] = info

    # 3. 污染控制技术信息
    tds = tables[2].findAll('td')
    res['FDJXH_SCQY'] = tds[1].text
    res['DDJXH_SCC'] = tds[3].text
    res['CNZZXH_SCC'] = tds[5].text
    res['DCRL_XHLC'] = tds[7].text
    res['CHZHQXH_SCQY'] = tds[9].text
    res['CHZHQTC_ZT_FZSCQY'] = tds[11].text
    res['RYZFZZXH_SCC'] = tds[13].text
    res['YCGQXH_SCQY'] = tds[15].text
    res['QZXPFKZZZXH_SCQY'] = tds[17].text
    res['EGRXH_SCQY'] = tds[19].text
    # res[''] = tds[21].text
    # res[''] = tds[23].text
    res['ECUXH_BB_SCC'] = tds[25].text
    res['BSQXS_DWS'] = tds[27].text
    res['XSQXH_SCQY'] = tds[29].text
    res['ZYQXH_SCQY'] = tds[31].text
    res['ZLQXS'] = tds[33].text


    # 联系信息
    ptags = soup.select('p')
    res['FRDB'] = ptags[3].text.split(':')[1]
    res['ADDRESS'] = ptags[4].text.split(':')[1]
    res['LXDH'] = ptags[5].text.split(':')[1]
    res['XXGKSJ'] = ptags[10].text.split('：')[1]
    return res


'''
{
	'重型柴油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=e90a899e2f7d6ebc72be5ec17cc7a40192dd0d0138e43b98&isprotect=false',
	'轻型汽油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=eed447b627eeee8bfddacdbcdcf78de892dd0d0138e43b98&isprotect=false',
	'重型燃气车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=6cbb1e3d2733d1670650d8480e763d01bf646bf7da6e187c&isprotect=false',
	'摩托车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=85b7de1045e7d2550aaa3491037c30eca8f5badb78f6ab6c&isprotect=false',
	'轻型汽车混合动力车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=01ec3d09b319c59d6cafd191d80333284746ecf1a9fe7019&isprotect=false',
	'非道路移动机械(柴油)环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=85031b741b2935b232c9ab279c448c4cbf646bf7da6e187c&isprotect=false',
	'轻型两用燃料车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=62bb2bd377151dfbdfe18e66126cf157efd519426e7bb918&isprotect=false',
	'电动车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=d014505829f36ba06e8020c2731e09b4efd519426e7bb918&isprotect=false',
	'轻型柴油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=43a99bcf18efd9f7bcace8cdcb3da312dc50418b9e7f4cb5&isprotect=false',
	'轻便摩托车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=d8b0b83d804dc12c6b600291a4e69976d12db3aadc7c433f&isprotect=false',
	'重型柴油混合动力车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=e90a899e2f7d6ebcfe5d812a5927545c4746ecf1a9fe7019&isprotect=false',
	'环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=216a53fa21daa2ac1f1f97bd3dcd3566d12db3aadc7c433f&isprotect=false',
	'重型汽油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=9ea2156a81d7d5b30847fbc0c5ee428f92dd0d0138e43b98&isprotect=false',
	'重型甲醇燃料汽车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=4b4a1e490ac0963bcd06f9ba6b0accd092dd0d0138e43b98&isprotect=false',
	'城市车辆重型柴油车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=216a53fa21daa2ac9c97351714a351f3b21c5ae6f07f61d4&isprotect=false',
	'非道路移动机械柴油机环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=05befd3ebc372ef8297bc7dc905f60f8d12db3aadc7c433f&isprotect=false',
	'轻型燃气车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=84b207a9d7706e8697a5d2e59616753bdc50418b9e7f4cb5&isprotect=false',
	'重型燃气混合动力车环保信息': 'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=6cbb1e3d2733d167f18c5e6d09993c26bf646bf7da6e187c&isprotect=false',
	'轻型混合动力环保信息':'http://gk.vecc.org.cn/ergs/o3/infoOpen/preview?sbbh=7e344a77e3a81e5ad8b3e19c9f4d7214dc50418b9e7f4cb5&isprotect=false'
}
'''
