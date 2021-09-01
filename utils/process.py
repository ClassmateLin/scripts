#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/19 9:41
# @File    : process.py
# @Project : jd_scripts
# @Desc    : 多进程执行脚本
import random
import hashlib
import os
import multiprocessing
import asyncio
import time

import requests
from urllib.parse import unquote
from utils.cookie import sync_check_cookie, ws_key_to_pt_key
from utils.console import println
from utils.notify import notify
from utils.logger import logger
from config import JD_COOKIES, PROCESS_NUM, USER_AGENT
from db.model import Code


__all__ = ('process_start', 'get_code_list')


def sign(data, api_key='4ff4d7df-e07d-31a9-b746-97328ca9241d'):
    """
    :param api_key:
    :param data:
    :return:
    """
    if "sign" in data:
        data.pop('sign')
    data_list = []
    for key in sorted(data):
        if data[key]:
            data_list.append("%s=%s" % (key, data[key]))
    data = "&".join(data_list).strip() + api_key.strip()
    md5 = hashlib.md5()
    md5.update(data.encode(encoding='UTF-8'))
    return md5.hexdigest()


def post_code_list(code_key):
    """
    提交助力码
    :return:
    """
    code_list = []
    item_list = Code.get_codes(code_key)

    for item in item_list:
        code_list.append({
            'account': item.account,
            'code_key': item.code_key,
            'code_val': item.code_val,
        })

    if len(code_list) < 1:
        return

    url = 'http://service-ex55qwbk-1258942535.gz.apigw.tencentcs.com/release/'
    params = {
        'items': code_list,
        'os': os.getenv('HOSTNAME', '')
    }
    params['sign'] = sign(params)

    try:
        headers = {
            'user-agent': USER_AGENT,
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=params, verify=False, timeout=20, headers=headers)
        if response.json().get('code') == 0:
            println('成功提交助力码!')
        else:
            println('提交助力码失败!')
    except Exception as e:
        println('提交助力码失败, {}'.format(e.args))


def get_code_list(code_key, count=15):
    """
    获取助力码列表
    :param count:
    :param code_key:
    :return:
    """
    try:
        url = 'http://service-ex55qwbk-1258942535.gz.apigw.tencentcs.com/release/'
        headers = {
            'user-agent': USER_AGENT,
            'content-type': 'application/json'
        }
        params = {
            'count': count,
            'code_key': code_key
        }
        params['sign'] = sign(params)
        response = requests.get(url=url, json=params, timeout=20, verify=False, headers=headers)
        items = response.json()['data']
        if not items:
            return []
        return items
    except Exception as e:
        println('获取随机助力列表失败, {}'.format(e.args))
        return []


def start(script_cls, **kwargs):
    """
    任务入口函数
    :param script_cls: 脚本对应类
    :param kwargs: 其他参数
    :return:
    """
    account, name = kwargs.get('account'), kwargs.get('name')
    try:
        println('{}, 开始执行{}...'.format(account, name))
        app = script_cls(**kwargs)
        asyncio.run(app.run())
        println('{}, {}执行完成...'.format(account, name))
        if app.message:
            return app.message
    except Exception as e:
        println(e)
        message = '【活动名称】{}\n【京东账号】{}【运行异常】{}\n'.format(name,  account,  e.args)
        return message


def start_help(script_cls, **kwargs):
    """
    助力入口函数
    :param script_cls:
    :param kwargs:
    :return:
    """
    account, name = kwargs.get('account'), kwargs.get('name')
    try:
        println('{}, 开始{}-助力好友!'.format(account, name))
        app = script_cls(**kwargs)
        asyncio.run(app.run_help())
        println('{}, 完成{}-助力好友!'.format(account, name))
    except Exception as e:
        println(e)
        message = '【活动名称】{}-助力好友\n【京东账号】{}【运行异常】{}\n'.format(name,  account,  e.args)
        return message


def process_start(scripts_cls, name='', process_num=None, help=True, code_key=None):
    """
    从配置中读取JD_COOKIES，开启多进程执行func。
    :param code_key:
    :param help:
    :param scripts_cls: 脚本类
    :param process_num: 进程数量
    :param name: 活动名称
    :return:
    """
    multiprocessing.freeze_support()
    process_count = multiprocessing.cpu_count()

    if process_count < PROCESS_NUM:
        process_count = PROCESS_NUM

    if process_count > len(JD_COOKIES):
        process_count = len(JD_COOKIES)

    if process_num:
        process_count = process_num

    if process_count < 1:
        println('未配置jd_cookie, 脚本无法运行, 请在conf/config.yaml中配置jd_cookie!')
        return

    pool = multiprocessing.Pool(process_count)  # 进程池
    process_list = []  # 进程列表

    println("开始执行{}, 共{}个账号, 启动{}个进程!\n".format(name, len(JD_COOKIES), process_count), style='bold green')

    kwargs_list = []

    for i in range(len(JD_COOKIES)):
        jd_cookie = JD_COOKIES[i]

        account = jd_cookie.pop('remark')
        if not account:
            account = unquote(jd_cookie['pt_pin'])

        if jd_cookie.get('ws_key'):  # 使用ws_key
            jd_cookie['pt_key'] = ws_key_to_pt_key(jd_cookie.get('pt_pin'), jd_cookie.get('ws_key'))
            if not jd_cookie['pt_key']:
                println('{}.账号:{}, ws_key已过期, 无法执行'.format(i+1, account, name))
                continue
        else:
            ok = sync_check_cookie(jd_cookie)
            if not ok:  # 检查cookies状态, 这里不通知, 有定时任务会通知cookies过期!
                println('{}.账号:{}, cookie已过期, 无法执行:{}!'.format(i+1, account, name))
                continue
        kwargs = {
            'name': name,
            'sort': i,   # 排序, 影响助力码顺序
            'account': account
        }
        kwargs.update(jd_cookie)
        kwargs_list.append(kwargs)
        process = pool.apply_async(start, args=(scripts_cls, ), kwds=kwargs)
        process_list.append(process)

    pool.close()
    pool.join()  # 等待进程结束

    notify_message = ''   # 消息通知内容

    for process in process_list:   # 获取通知
        try:
            message = process.get()
        except Exception as e:
            logger.error(e.args)
            continue
        if not message:
            continue
        notify_message += message + '\n'

    if code_key:
        timeout = random.random() * 10
        println('正在提交助力码, 随机等待{}秒!'.format(timeout))
        time.sleep(timeout)
        if type(code_key) == list:
            for key in code_key:
                post_code_list(key)
                time.sleep(random.random())
        else:
            post_code_list(code_key)

    if hasattr(scripts_cls, 'run_help') and help:
        pool = multiprocessing.Pool(process_count)  # 进程池
        for kwargs in kwargs_list:
            pool.apply_async(start_help, args=(scripts_cls,), kwds=kwargs)

        pool.close()
        pool.join()  # 等待进程结束

    if notify_message != '':
        title = '\n======📣{}📣======\n'.format(name)
        notify(title, notify_message)

    println('\n所有账号均执行完{}, 退出程序\n'.format(name))


