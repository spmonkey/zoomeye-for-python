import requests, re

with open("../webscan/phpMyAdmin/url1.txt", "r+") as r:
    urls = r.readlines()
    for url in urls:
        url_text = url.split("\n")
        version = "/README"
        url_ver = "http://" + url_text[0] + version
        # url_ver = "http://" + url
        ver = requests.get(url=url_ver)
        print(url_ver)