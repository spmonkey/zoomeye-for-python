#!/usr/bin/python3
import requests, tqdm
import re, os, shutil

headers = {'API-KEY': '输入您自己的API-KEY'}
search_info_num = []
# 用户
'''
search : 剩余赠送额度
interval : 额度更新周期
remain_free_quota : 剩余赠送额度
remain_total_quota : 剩余总额度
'''
def user_info():
    url_info = 'https://api.zoomeye.org/resources-info'  # 获取资源信息：用户基本信息及可用额度
    resources_info = requests.get(url=url_info, headers=headers)
    search_info = re.findall('"remain_total_quota": (.+).+.+', resources_info.text)  # 获取总额度
    for remain in search_info:
        search_info_num.append(remain)
        return 'remain_total_quota: ' + remain

# 资产搜集
'''
query : 查询关键词
page ： 页数
facets ： 统计项
支持的统计项：webapp(web应用),component(web容器),framework(web框架),frontend(前端组件),server(web服务器),waf(web防火墙),os(操作系统),country(国家),city(城市)
'''
def webscan():
    user_info()
    remain_total_quota = int(search_info_num[0])
    if remain_total_quota > 0:
        print(remain_total_quota)
        print("可以进行下一步操作！")
        page = int(input("请输入需要爬取的页数："))
        web_scan = 'https://api.zoomeye.org/web/search?'
        query = 'query=' + input("""
请输入查询关键词(例子 : app:"DedeCMS" +country:"CN")：
        """)
        facets = 'facets=' + input("""
        请输入统计项(用,隔开，例子：webapp,os)：
                    """)
        for i in range(1, page+1):
            pages = 'page=' + str(i)
            urls = web_scan + query + '&' + pages + '&' + facets
            webscan = requests.get(url=urls,headers=headers)
            webscan.encoding = 'utf-8'
            isExists_dir = os.path.exists('webscan')
            isExists_file = os.path.exists('webscan/webscan{0}.json'.format(i))
            if isExists_dir == True:
                if isExists_file == True:
                    os.remove('webscan/webscan{0}.json'.format(i))
                pass
            else:
                os.mkdir('webscan')
            with open('webscan/webscan{0}.json'.format(i), 'a+', encoding='utf-8') as w:
                w.write(webscan.text)
        return "web资产收集完成！请开始您的渗透之旅吧~"
    else:
        return "您的额度不够，请充值或更换账号！"
        pass
'''
域名 / IP 关联查询
'''
def domain():
    user_info()
    remain_total_quota = int(search_info_num[0])
    if int(remain_total_quota) > 0:
        print("可以进行下一步操作！")
        page = int(input("请输入需要爬取的页数："))
        domain_scan = 'https://api.zoomeye.org/domain/search?'
        q = 'q=' + input("""
请输入查询关键字(例子：baidu.com)：
        """)
        type = 'type=' + input("""
请输入类型(默认为 0 )：
                            """)
        for i in range(1, page+1):
            page = 'page=' + str(i)
            urls = domain_scan + q + '&' + page + '&' + type
            domainscan = requests.get(url=urls,headers=headers)
            isExists_dir = os.path.exists('domainscan')
            isExists_file = os.path.exists('domainscan/domainscan{0}.json'.format(i))
            if isExists_dir == True:
                if isExists_file == True:
                    os.remove('domainscan/domainscan{0}.json'.format(i))
                pass
            else:
                os.mkdir('domainscan')
            with open('domainscan/domainscan{0}.json'.format(i), 'a+', encoding='utf-8') as w:
                w.write(domainscan.text)
        return "域名 / IP资产收集完成！请开始您的渗透之旅吧~"
    else:
        return "您的额度不够，请充值或更换账号！"
        pass
    
