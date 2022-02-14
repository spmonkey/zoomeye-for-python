import re, requests, random
from get_user_agent import get_user_agent

def get_ip():
    urls = "https://www.kuaidaili.com/free/inha/1/"
    str_html = requests.get(urls, headers=get_user_agent())
    str_text = str_html.text
    # print(str_text)
    regex = re.compile('<td data-title="IP">(.*)</td>')
    ips = regex.findall(str_text)
    port_regex = re.compile('<td data-title="PORT">(.*)</td>')
    ports = port_regex.findall(str_text)
    ip_arr = {ips[key]: ports[key] for key in range(len(ips))}

    # keys = random.choice(list(ip_arr))
    # print(ip_arr[keys])
    # port_str = keys + ':' + ip_arr[keys]
    # proxies = {
    #     'http': port_str,
    #     'https': port_str
    # }
    # print(proxies)
    # res = requests.get('http://www.baidu.com', proxies=proxies)
    # print(res)

    ip_list = ip_arr
    return ip_list
#     print(ip_list[keys])
# get_ip()