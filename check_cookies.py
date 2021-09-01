#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/21 2:17 下午
# @File    : check_cookies.py
# @Project : jd_scripts
# @Cron    : 0 */2 * * *
# @Desc    : 检查cookies是否过期, 过期则发送通知
import asyncio
from urllib.parse import unquote
from config import JD_COOKIES
from utils.console import println
from utils.cookie import async_check_cookie
from utils.notify import notify


async def check_cookies():
    """
    检查配置中的cookies是否已过期, 过期则发送通知
    :return:
    """
    println('开始检查账号cookies状态, 共{}个!'.format(len(JD_COOKIES)))
    title = '\n======📣【过期cookies列表】📣======\n'
    message = ''
    need_notify = False
    for cookies in JD_COOKIES:
        account = cookies.pop('remark')
        if not account:
            account = unquote(cookies['pt_pin'])

        if cookies.get('ws_key', None):
            continue
        ok = await async_check_cookie(cookies)
        if not ok:
            message += ' ' * 6 + account + '\n'
            println('{}, cookies已过期!'.format(account))
            need_notify = True
        else:
            println('{}, cookies正常!'.format(account))
    if need_notify:
        notify(title=title, content=message)


if __name__ == '__main__':
    asyncio.run(check_cookies())
