#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/30 4:59 下午
# @File    : cookie.py
# @Project : jd_scripts
# @Desc    :
import json
from urllib.parse import urlencode

import aiohttp
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def ws_key_to_pt_key(pt_pin, ws_key):
    """
    ws_key换pt_key
    :return:
    """
    cookies = {
        'pin': pt_pin,
        'wskey': ws_key,
    }
    headers = {
        'user-agent': 'okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1080x2293;os/11;network/wifi;',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    url = 'https://api.m.jd.com/client.action?functionId=genToken&clientVersion=10.1.2&build=89743&client=android' \
          '&d_brand=&d_model=&osVersion=&screen=&partner=&oaid=&openudid=a27b83d3d1dba1cc&eid=&sdkVersion=30&lang' \
          '=zh_CN&uuid=a27b83d3d1dba1cc&aid=a27b83d3d1dba1cc&area=19_1601_36953_50397&networkType=wifi&wifiBssid=&uts' \
          '=&uemps=0-2&harmonyOs=0&st=1630413012009&sign=ca712dabc123eadd584ce93f63e00207&sv=121'
    body = 'body=%7B%22to%22%3A%22https%253a%252f%252fplogin.m.jd.com%252fjd-mlogin%252fstatic%252fhtml' \
           '%252fappjmp_blank.html%22%7D&'
    response = requests.post(url, data=body, headers=headers, cookies=cookies, verify=False)
    data = json.loads(response.text)
    if data.get('code') != '0':
        return None
    token = data.get('tokenKey')
    url = data.get('url')
    session = requests.session()
    params = {
        'tokenKey': token,
        'to': 'https://plogin.m.jd.com/jd-mlogin/static/html/appjmp_blank.html'
    }
    url += '?' + urlencode(params)
    session.get(url, allow_redirects=True)
    for k, v in session.cookies.items():
        if k == 'pt_key':
            return v
    return None


async def async_check_cookie(cookies):
    """
    检测cookies是否过期
    :return:
    """
    try:
        url = 'https://api.m.jd.com/client.action?functionId=newUserInfo&clientVersion=10.0.9&client=android&openudid' \
              '=a27b83d3d1dba1cc&uuid=a27b83d3d1dba1cc&aid=a27b83d3d1dba1cc&area=19_1601_36953_50397&st' \
              '=1626848394828&sign=447ffd52c08f0c8cca47ebce71579283&sv=101&body=%7B%22flag%22%3A%22nickname%22%2C' \
              '%22fromSource%22%3A1%2C%22sourceLevel%22%3A1%7D&'
        headers = {
            'user-agent': 'okhttp/3.12.1;jdmall;android;version/10.0.9;build/89099;screen/1080x2293;os/11;network/wifi;'
        }
        async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
            response = await session.post(url=url, headers=headers)
            text = await response.text()
            data = json.loads(text)
            if data['code'] != '0':
                return False
            else:
                return True
    except Exception as e:
        print(e.args)
        return False


def sync_check_cookie(cookies):
    """
    检测cookies是否过期
    :param cookies:
    :return:
    """
    try:
        url = 'https://api.m.jd.com/client.action?functionId=newUserInfo&clientVersion=10.0.9&client=android&openudid' \
              '=a27b83d3d1dba1cc&uuid=a27b83d3d1dba1cc&aid=a27b83d3d1dba1cc&area=19_1601_36953_50397&st' \
              '=1626848394828&sign=447ffd52c08f0c8cca47ebce71579283&sv=101&body=%7B%22flag%22%3A%22nickname%22%2C' \
              '%22fromSource%22%3A1%2C%22sourceLevel%22%3A1%7D&'
        headers = {
            'user-agent': 'okhttp/3.12.1;jdmall;android;version/10.0.9;build/89099;screen/1080x2293;os/11;network/wifi;'
        }
        response = requests.post(url=url, headers=headers, cookies=cookies, verify=False)
        data = response.json()
        if data['code'] != '0':
            return False
        else:
            return True
    except Exception as e:
        print(e.args)
        return False

