#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/8/16 3:04 下午
# @File    : update_config.py
# @Project : jd_scripts
# @Desc    :
import os
import shutil
import sys
import yaml


def read_conf(conf_path):
    """
    读取yaml配置文件
    :param conf_path:
    :return:
    """
    try:
        # 加载配置文件
        with open(conf_path, 'r', encoding='utf-8-sig') as f:
            cfg = yaml.safe_load(f)
        return cfg
    except Exception as e:
        print('读取配置文件:{}失败, {}'.format(conf_path, e.args))
        return dict()


class Config:
    """
    配置更新操作
    """
    conf_desc_map = {
        'debug': '控制台输出: true/false',
        'log_days': '日志保留天数, 默认3天',
        'process_num': '脚本默认开启进程数量',
        'joy_process_num': '宠汪汪脚本开启进程数',
        'jd_cookies': '京东cookies, 包含pt_key=xx;pt_pin=xx;即可, 中间不能有空格, 分号不能少。如需给cookie添加备注, 可在其后面添加: `remark=账号1;`, 例如:`pt_pin=jd_78b;pt_key=AAJgyqEMOxU;remark=账号1;`',
        'jd_farm_bean_card': '东东农场是否使用水滴换豆卡, 100水滴可以换20京豆, 默认不兑换',
        'jd_farm_retain_water': '东东农场每天保留多少水滴, 用于明天的十次浇水任务',
        'notify': '消息通知配置项, TG机器人通知需要宿主机有qiang。',
        'tg_bot_token': 'TG机器人TOKEN',
        'tg_user_id': 'TG机器人用户ID',
        'push_plus_token': 'pushplus消息通知Token, https://www.pushplus.plus/',
        'push_plus_group': 'pushplus一对多通知组编号, 一对一不需要填',
        'qywx_am': '企业微信通知, 依次填上corpid的值,corpsecret的值,touser的值,agentid,media_id的值，注意用英文,号隔开。',
        'crontab_exclude_scripts': '在此列表中的脚本, 将不会加入到定时任务中, 如需立即生效, 请手动执行命令: docker-entrypoint',
        'jd_puzzle_process_num': '拼图签到默认进程数量',
        'jd_try_cid_list': '京东试用商品分类, 英文逗号分隔, 可选列表: 全部商品,家用电器,手机数码,电脑办公,家居家装,美妆护肤,服饰鞋包,母婴玩具,生鲜美食,图书音像,钟表奢品,个人护理,家庭清洁,食品饮料.更多惊喜',
        'jd_try_type_list': '京东试用类型, 英文逗号分隔, 可选列表: 全部试用,普通试用,闪电试用,30天试用',
        'jd_try_min_price': '京东试用商品最低价格',
        'jd_try_goods_count': '京东试用商品提供商品最大数量, 商品提供量多的是辣鸡商品',
        'jd_try_filter_keywords': '京东试用商品过滤关键词, 用@分隔',
        'chrome_path': 'chromium路径, 默认不需要修改，除非你是本地运行或者进行开发。',
        'joy_feed_count': '宠汪汪喂食狗粮克数',
        'server_send_key': 'server酱通知key',
        'tg_bot_api': 'TG代理'
    }

    def __init__(self):

        pwd = os.path.split(os.path.abspath(sys.argv[0]))[0].replace('tools', '')
        self.conf_name = os.path.join(pwd, 'conf/config.yaml')  # 当前配置文件
        self.conf_bak_name = os.path.join(pwd, 'conf/config.yaml.bak')  # 备份配置文件
        self.sample_conf_name = os.path.join(pwd, '.config.yaml')  # 示例配置文件

    def merge(self, cur_conf, sample_conf):
        """
        合并示例配置文件和当前使用的配置文件
        :param cur_conf:
        :param sample_conf:
        :return:
        """
        res = dict()
        for ck, cv in cur_conf.items():
            if type(cv) == dict:
                res[ck] = self.merge(cv, sample_conf.get(ck, dict()))
                continue
            if ck == 'push_p_token':
                res['push_plus_token'] = cv
            if ck not in sample_conf:  # 示例配置文件已经取消的选项
                continue
            res[ck] = cv
        for sk, sv in sample_conf.items():
            if sk not in res:
                res[sk] = sv

        return res

    def update_conf(self, conf):
        """
        更新配置文件
        :param conf:
        :param path:
        :return:
        """
        try:
            result = ['# 脚本配置文件 \n\n']
            with open(self.conf_name, 'w', encoding='utf-8-sig') as f:
                yaml.safe_dump(conf, f, allow_unicode=True)

            with open(self.conf_name, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    tmp = line.split(':')
                    if len(tmp) > 1:
                        result.append('\n{}# {}\n'.format(' ' * tmp[0].count(' '), self.conf_desc_map[tmp[0].strip()]))
                        result.append(line)
                    else:
                        result.append(line)

            with open(self.conf_name, 'w', encoding='utf-8-sig') as f:
                for r in result:
                    f.write(r)
        except Exception as e:
            print('写入配置文件:{}失败, {}'.format(self.conf_name, e.args))

    def run(self):
        """
        :return:
        """
        print(f'备份配置文件:{self.conf_name}至:{self.conf_bak_name}...')
        shutil.copy(self.conf_name, self.conf_bak_name)
        cur_conf = read_conf(self.conf_name)
        sample_conf = read_conf(self.sample_conf_name)
        if not cur_conf or not sample_conf:
            return
        res_conf = self.merge(cur_conf, sample_conf)

        print(f'更新配置文件:{self.conf_name}...')
        self.update_conf(res_conf)


if __name__ == '__main__':
    app = Config()
    app.run()
