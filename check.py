# -*- coding: utf-8 -*-
"""
@Filename	:	check.py
@Created 	:	2024/04/07  14:51
@Updated	:	2024/04/07  14:51
@Author 	:	goonhope@gmail.com; Teddy; Zhuhai
@Function	:	Master-Mind-007/Auto-Parse-Proxy https stocks5 前100测试
@Process 	:	Flow
@WitNote	:	备注
@Reference	:	引用
"""
from faker import Faker
import requests, threading, os, time, platform


def google_hder(host=None, o=True):
    """'google search url headers"""
    google_hders = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': f'https://www.{"google.com.hk" if o else "qq.com"}',
        'Upgrade-insecure-requests': '1',
        'User-Agent': Faker("zh_CN").chrome()} # fr..user_agent()
    if host and isinstance(host,(str,dict)):
        google_hders.update(host if isinstance(host,dict) else dict(Host=host))
    return google_hders


def get_(url="", hdrs=None, data=None, proxy=None, j=False,ky=""):
    """get optional json"""
    furl = f"https://raw.githubusercontent.com/Master-Mind-007/Auto-Parse-Proxy/main/{ky}.txt" if ky else url
    url_headers, goal = google_hder(furl.split("/")[2]), None
    if hdrs and isinstance(data, dict): url_headers.update(hdrs)
    url_data = requests.get(furl, headers=url_headers, params=data, timeout=5, proxies=proxy, verify=False)
    if url_data.status_code == 200: goal = url_data.json() if j else set(url_data.text.strip().split()[:100])
    return goal


def err(func):
    """错误时返回函数名称"""
    def inner(*args,**kwargs):
        intime = time.strftime("%Y/%m/%d %H:%M:%S")
        try: return func(*args,**kwargs)
        except Exception as e:
            return print(f"@ERROR: {intime}->{func.__name__}\nDetail: {e}!")
    return inner


@err
def process(i, type):
    ip, port = i.split(":")
    requests.get("https://icanhazip.com/", proxies={type: f"{type}://{i}"}, timeout=3)
    if info := get_(f"http://ip-api.com/json/{ip}", j=True):
        info.update(dict(port=i,type=type))
        with open("all.txt", "a+") as f:
            f.write(str(info) + "\n")


def go():
    hold = "https stock5".split()
    for ty in hold:
        if data := get_(ky=ty):
            process(i, type)
            # for i in data:
            #     while threading.active_count() > 7000:
            #         time.sleep(3)
            #     threading.Thread(target=process, args=(i,ty)).start()
            # while threading.active_count() > 1:
            #     time.sleep(1)
        time.sleep(1.314)

if __name__ == '__main__':
    go()
