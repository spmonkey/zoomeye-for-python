#!/usr/bin/python3
import sys
import lib.zoomeye

def main_user(user):
    print(user)

def main_web(web):
    print(web)

def main_domain(domain):
    print(domain)

def main_host(host):
    print(host)

if __name__ == '__main__':
    headers = {'API-KEY': input("请输入您的API-KEY：")}
    try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            raise SystemExit("""
usage : python {0}
    -h --help      View the user manual
    -w --webscan   Web Application Search
    -d --domain    Associated query of domain names and IP addresses
    -u --user_info Check the user's total quota
    --host         Host Device Search
    """.format(sys.argv[0]))
        elif sys.argv[1] == "-u" or sys.argv[1] == "--user_info":
            main_user(lib.zoomeye.user_info(headers))
        elif sys.argv[1] == "-w" or sys.argv[1] == "--webscan":
            main_web(lib.zoomeye.webscan(headers))
        elif sys.argv[1] == "-d" or sys.argv[1] == "--domain":
            main_domain(lib.zoomeye.domain(headers))
        elif sys.argv[1] == "--host":
            main_host(lib.zoomeye.host(headers))
    except IndexError:
        print("""
usage : python {0}
    -h --help      View the user manual
    -w --webscan   Performing Web asset Collection
    -d --domain    Performing Host asset Collection
    -u --user_info Check the user's total quota
    --host         Host Device Search
    """.format(sys.argv[0]))
