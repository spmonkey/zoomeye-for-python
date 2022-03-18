#!/usr/bin/python3
import requests
import re, os, time
from tqdm import tqdm


search_info_num = []
# 用户
'''
search : 剩余赠送额度
interval : 额度更新周期
remain_free_quota : 剩余赠送额度
remain_total_quota : 剩余总额度
'''
def user_info(headers):
    url_info = 'https://api.zoomeye.org/resources-info'  # 获取资源信息：用户基本信息及可用额度
    resources_info = requests.get(url=url_info, headers=headers)
    if resources_info.status_code == 200:
        # print(resources_info.text)
        search_info = re.findall('"remain_total_quota": (.+).+.+', resources_info.text)  # 获取总额度
        for remain in search_info:
            search_info_num.append(remain)
            return 'remain_total_quota: ' + remain
    elif resources_info.status_code == 401:
        return '请您先登录! '

'''
资产收集
支持的统计项：webapp(web应用),component(web容器),framework(web框架),frontend(前端组件),server(web服务器),waf(web防火墙),os(操作系统),country(国家),city(城市)
'''
def webscan(headers):
    user_info(headers)
    remain_total_quota = int(search_info_num[0])
    if remain_total_quota > 0:
        print("\n欢迎使用spmonkey的资产收集工具\n")
        print("可以进行下一步操作！")
        page = input("请输入需要爬取的页数(可选，默认为 1)：")
        if page == '':
            page = 1
        else:
            page = page
        web_scan = 'https://api.zoomeye.org/web/search?'
        facets = 'facets=' + input("""
支持的统计项：webapp(web应用),component(web容器),framework(web框架),frontend(前端组件),server(web服务器),waf(web防火墙),os(操作系统),country(国家),city(城市)
请输入统计项(可选，用,隔开，例子：app,os)：""")
        print("")
        if facets == '':
            facets = ''
        else:
            facets = facets
        query = input("""
请输入搜索关键词(必填，例子:app:"DedeCMS")：""")
        while True:
                if query == '':
                    query = input("""
请输入搜索关键词(必填，例子:app:"DedeCMS")：""")
                else:
                    break
        r = re.findall('app:"(.+?)"', query)
        if r == []:
            if query == '"/seller.php?s=/Public/login"':
                isExists_dir = os.path.exists('webscan')
                isExists_dir_dir = os.path.exists('webscan/lionfishcms')
                if isExists_dir == True:
                    if isExists_dir_dir == True:
                        for x in os.listdir('webscan/lionfishcms'):
                            file_data = 'webscan/lionfishcms' + '\\' + x
                            if os.path.isfile(file_data) == True:
                                os.remove(file_data)
                        else:
                            pass
                    else:
                        if query == '"/seller.php?s=/Public/login"':
                            os.mkdir('./webscan/lionfishcms')
                else:
                    os.mkdir('webscan')
                print("正在收集{0}的资产，并整理URL！".format(query))
                for i in range(1, int(page) + 1):
                    page = str(i)
                    urls = web_scan + 'query=' + query + '&' + 'page=' + page + '&' + facets
                    webscan = requests.get(url=urls,headers=headers)
                    webscan.encoding = 'utf-8'
                    if webscan.status_code == 200:
                        web = re.sub('"raw_data": "(.+?)", ', "", webscan.text)
                        urls = re.findall('"url": "(.+?)",', web)
                        with open('webscan/lionfishcms/lionfishcms{0}.json'.format(i), 'a+', encoding='utf-8') as w:
                            time.sleep(0.1)
                            w.write(web)
                        time.sleep(0.5)
                        if urls == []:
                            with open('webscan/lionfishcms/lionfishcms{0}.json'.format(i), 'r+', encoding='utf-8') as f:
                                for file in f.readlines():
                                    ips = re.findall('"ip": \["(.+?)"],', file)
                                    for x in tqdm(range(len(ips))):
                                        with open('webscan/lionfishcms/url{0}.txt'.format(i), 'a+', encoding='utf-8') as w_f:
                                                w_f.write("{0}\n".format(ips[x]))
                        else:
                                with open('webscan/lionfishcms/lionfishcms{0}.json'.format(i), 'r+', encoding='utf-8') as f:
                                    for file in f.readlines():
                                        url_list = re.findall('"url": "(.+?)",', file)
                                        for x in tqdm(range(len(url_list))):
                                            with open('webscan/lionfishcms/url{0}.txt'.format(i), 'a+', encoding='utf-8') as w_f:
                                                w_f.write("{0}\n".format(url_list[x]))
                        print("")
            else:
                for i in range(1, int(page) + 1):
                    isExists_dir = os.path.exists('webscan')
                    isExists_dir_dir = os.path.exists('./webscan/{0}'.format(query))
                    isExists_file = os.path.exists('./webscan/{0}/{0}{1}.json'.format(query, i))
                    isExists_txt = os.path.exists('./webscan/{0}/url{1}.txt'.format(query, i))
                    if isExists_dir == True:
                        if isExists_dir_dir == True:
                            if isExists_file == True and isExists_txt == True:
                                os.remove('webscan/{0}/{0}{1}.json'.format(query, i))
                                os.remove('webscan/{0}/url{0}{1}.txt'.format(query, i))
                            elif isExists_file == True and isExists_txt == False:
                                os.remove('webscan/{0}/{0}{1}.json'.format(query, i))
                            else:
                                pass
                        else:
                                os.mkdir('./webscan/{0}'.format(query))
                    else:
                        os.mkdir('webscan')
                    print("正在收集{0}的资产，并整理URL！".format(query))
                    page = str(i)
                    urls = web_scan + 'query=' + query + '&' + 'page=' + page + '&' + facets
                    webscan = requests.get(url=urls, headers=headers)
                    webscan.encoding = 'utf-8'
                    if webscan.status_code == 200:
                        web = re.sub('"raw_data": "(.+?)", ', "", webscan.text)
                        urls = re.findall('"url": "(.+?)",', web)
                        with open('webscan/{0}/{0}{1}.json'.format(query, i), 'a+', encoding='utf-8') as w:
                            time.sleep(0.1)
                            w.write(web)
                        time.sleep(0.5)
                        if urls == []:
                            with open('webscan/{0}/{0}{1}.json'.format(query, i), 'r+', encoding='utf-8') as f:
                                for file in f.readlines():
                                    ips = re.findall('"ip": \["(.+?)"],', file)
                                    for x in tqdm(range(len(ips))):
                                        with open('webscan/{0}/url{1}.txt'.format(query, i), 'a+',
                                                  encoding='utf-8') as w_f:
                                            w_f.write("{0}\n".format(ips[x]))
                        else:
                            with open('webscan/{0}/{0}{1}.json'.format(query, i), 'r+', encoding='utf-8') as f:
                                for file in f.readlines():
                                    url_list = re.findall('"url": "(.+?)",', file)
                                    for x in tqdm(range(len(url_list))):
                                        with open('webscan/{0}/url{1}.txt'.format(query, i), 'a+',
                                                  encoding='utf-8') as w_f:
                                            w_f.write("{0}\n".format(url_list[x]))
                        print("")
                else:
                    return "缺少参数哦！"
        else:
            print("正在收集{0}的资产，并整理URL！".format(r[0]))
        # with open("./lib/cms.txt", "r", encoding="utf-8") as file:
        #     for files in file.readlines():
        #         cms = files.split("\n")
        #         query = 'query={0}'.format(cms[0])
        #         print("正在收集{0}的资产，并整理URL！".format(cms[0]))
            for i in range(1, int(page) + 1):
                page = str(i)
                urls = web_scan + 'query=' + query + '&' + 'page=' + page + '&' + facets
                webscan = requests.get(url=urls,headers=headers)
                webscan.encoding = 'utf-8'
                if webscan.status_code == 200:
                    web = re.sub('"raw_data": "(.+?)", ', "", webscan.text)
                    urls = re.findall('"url": "(.+?)",', web)
                    isExists_dir = os.path.exists('webscan')
                    isExists_dir_dir = os.path.exists('./webscan/{0}'.format(r[0]))
                    if isExists_dir == True:
                        if isExists_dir_dir == True:
                            for x in os.listdir('webscan/{0}'.format(r[0])):
                                file_data = 'webscan/{0}'.format(r[0]) + '\\' + x
                                if os.path.isfile(file_data) == True:
                                    os.remove(file_data)
                            else:
                                pass
                        else:
                            os.mkdir('./webscan/{0}'.format(r[0]))
                    else:
                        os.mkdir('webscan')
                    with open('webscan/{0}/{0}{1}.json'.format(r[0], i), 'a+', encoding='utf-8') as w:
                        time.sleep(0.1)
                        w.write(web)
                    time.sleep(0.5)
                    if urls == []:
                        with open('webscan/{0}/{0}{1}.json'.format(r[0], i), 'r+', encoding='utf-8') as f:
                            for file in f.readlines():
                                ips = re.findall('"ip": \["(.+?)"],', file)
                                for x in tqdm(range(len(ips))):
                                    with open('webscan/{0}/url{1}.txt'.format(r[0], i), 'a+', encoding='utf-8') as w_f:
                                            w_f.write("{0}\n".format(ips[x]))
                    else:
                            with open('webscan/{0}/{0}{1}.json'.format(r[0], i), 'r+', encoding='utf-8') as f:
                                for file in f.readlines():
                                    url_list = re.findall('"url": "(.+?)",', file)
                                    for x in tqdm(range(len(url_list))):
                                        with open('webscan/{0}/url{1}.txt'.format(r[0], i), 'a+', encoding='utf-8') as w_f:
                                            w_f.write("{0}\n".format(url_list[x]))
                    print("")
                else:
                    return "缺少参数哦！"
        return "web资产收集完成！请开始您的渗透之旅吧~"
    else:
        return "您的额度不够，请充值或更换账号！"
        pass

'''
域名 / IP 关联查询
'''
def domain(headers):
    user_info(headers)
    remain_total_quota = int(search_info_num[0])
    if int(remain_total_quota) > 0:
        print(remain_total_quota)
        print("可以进行下一步操作！")
        page = input("请输入需要爬取的页数(可选，默认为 1)：")
        if page == '':
            page = 1
        else:
            page = page
        domain_scan = 'https://api.zoomeye.org/domain/search?'
        with open("./lib/edu.txt", "r", encoding="utf-8") as file:
            for files in file.readlines():
                edu = files.split("\n")
                q = 'q=' + edu[0]
        type = 'type=' + input("""
0：搜索关联域名，1：搜索子域名
请输入类型(必填，类型有：0 或 1)：""")
        while True:
            if type == 'type=':
                type = 'type=' + input("""
0：搜索关联域名，1：搜索子域名
请输入类型(必填，类型有：0 或 1)：""")
            else:
                break
        for i in range(1, int(page) + 1):
            page = str(i)
            urls = domain_scan + q + '&' + 'page=' + page + '&' + type
            domainscan = requests.get(url=urls,headers=headers)
            domain = re.findall('"name"', domainscan.text)
            # print(len(domain))
            domainscan.encoding = "utf-8"
            isExists_dir = os.path.exists('domainscan')
            isExists_file = os.path.exists('domainscan/domainscan{0}.json'.format(i))
            if isExists_dir == True:
                if isExists_file == True:
                    os.remove('domainscan/domainscan{0}.json'.format(i))
                pass
            else:
                os.mkdir('domainscan')
            # for j in tqdm(range(len(domain))):
            with open('domainscan/domainscan{0}.json'.format(i), 'a+', encoding='utf-8') as w:
                time.sleep(0.1)
                w.write(domainscan.text)
            with open('domainscan/domainscan{0}.json'.format(i), 'r+', encoding='utf-8') as f:
                for file in f.readlines():
                    ips = re.findall('"name": "(.+?)",', file)
                    for x in tqdm(range(len(domain))):
                        with open('domainscan/url{0}.txt'.format(i), 'a+', encoding='utf-8') as w_f:
                            w_f.write("{0}\n".format(ips[x]))
            print("")
        return "域名 / IP资产收集完成！请开始您的渗透之旅吧~"
    else:
        return "您的额度不够，请充值或更换账号！"
        pass

'''
主机设备收集
支持的统计项：app(应用),device(设备类型),service(服务类型),port(端口号),os(操作系统),country(国家),city(城市)
'''
def host(headers):
    user_info(headers)
    remain_total_quota = int(search_info_num[0])
    if int(remain_total_quota) > 0:
        print(remain_total_quota)
        print("可以进行下一步操作！")
        page = input("请输入需要爬取的页数(可选，默认为 1)：")
        if page == '':
            page = 1
        else:
            page = page
        hostscan_scan = 'https://api.zoomeye.org/host/search?'
        query = 'query=' + input("""
请输入查询关键字(必填，例子：port:80 nginx)：""")
        while True:
            if query == 'query=':
                query = 'query=' + input("""
请输入查询关键字(必填，例子：port:80 nginx)：""")
            else:
                break
        facets = 'facets=' + input("""
支持的统计项：app(应用),device(设备类型),service(服务类型),port(端口号),os(操作系统),country(国家),city(城市)
请输入统计项(可选，用,隔开，例子：app,os)：""")
        if facets == '':
            facets = ''
        else:
            facets = facets
        sub_type = input("""
数据类型：ipv4,ipv6
请输入数据类型(可选，例子：sub_type:v4): """)
        if sub_type == '':
            sub_types = 'sub_type:v4,v6'
        else:
            sub_types = sub_type
        for i in range(1, int(page) + 1):
            page = str(i)
            urls = hostscan_scan + query + '&' + 'page=' + page + '&' + facets + '&' + sub_types
            hostscan = requests.get(url=urls, headers=headers)
            hostscan.encoding = "utf-8"
            if hostscan.status_code == 200:
                isExists_dir = os.path.exists('hostscan')
                isExists_file = os.path.exists('hostscan/hostscan{0}.json'.format(i))
                if isExists_dir == True:
                    if isExists_file == True:
                        os.remove('hostscan/hostscan{0}.json'.format(i))
                    pass
                else:
                    os.mkdir('hostscan')
                for j in tqdm(range(100)):
                    with open('hostscan/hostscan{0}.json'.format(i), 'a+', encoding='utf-8') as w:
                        time.sleep(0.1)
                        w.write(hostscan.text)
                print("")
            elif hostscan.status_code == 500:
                errors = re.findall('"error": "(.+?)"',hostscan.text)
                for error in errors:
                    return error
            else:
                return '缺少参数哦! '

        return "主机设备资产收集完成！请开始您的渗透之旅吧~"
    else:
        return "您的额度不够，请充值或更换账号！"
        pass
