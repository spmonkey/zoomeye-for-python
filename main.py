#!/usr/bin/python3
import sys
import lib.zoomeye

def main_user(user):
    print(user)

def main_web(web):
    print(web)

def main_domain(domain):
    print(domain)


if __name__ == '__main__':
#     try:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            raise SystemExit("""
    {0} usage : python main.py
        -h --help      View the user manual
        -w --webscan   Performing Web asset Collection
        -d --domain    Performing Host asset Collection
        -u --user_info Check the user's total quota
        """.format(sys.argv[0]))
        elif sys.argv[1] == "-u" or sys.argv[1] == "--user_info":
            main_user(lib.zoomeye.user_info())
        elif sys.argv[1] == "-w" or sys.argv[1] == "--webscan":
            main_web(lib.zoomeye.webscan())
        elif sys.argv[1] == "-d" or sys.argv[1] == "--domain":
            main_domain(lib.zoomeye.domain())
#     except:
#         print("""
# {0} usage : python main.py
#     -h --help      View the user manual
#     -w --webscan   Performing Web asset Collection
#     -d --domain    Performing Host asset Collection
#     -u --user_info Check the user's total quota
#     """.format(sys.argv[0]))
