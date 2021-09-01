# 简介

**[点击查看《提问的智慧》。](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)**

**对于非常小白(google/baidu有答案)的issue, 一律直接close!**

- python版本:3.7.*

## 安裝

### 本地运行

- `pip install virtualenv`
- `git clone https://github.com/ClassmateLin/jd_scripts.git`
- `cd jd_scripts`
- `virtualenv venv && source ./venv/bin/activate`
- `pip install -r requirements.txt`
- `mkdir conf && cp .config.yaml ./conf/`

### 使用docker

- docker一键安装: 
  - x86:  `docker run -d --name jd classmatelin/hhl:latest`,
  - arm: `docker run -d --name jd classmatelin/hhl-n1:latest`。`
- docker-compose配置自行编写, 映射logs和conf目录即可。


## 更新

- `docker exec -it jd /bin/docker-entrypoint`

### 

## 使用

- 进入容器: `docker exec -it jd bash`


- 获取JD_COOKIES: `python get_jd_cookies.py`, 扫描登录成功后控制台会打印JD_COOKIES.

- vim /scripts/conf/config.yaml, 填入上一步获取的JD_COOKIES， `pt_pin=xxx;pt_key=xxx;`和`pt_key=xxx;pt_pin=xxx;`是一样的。

    ```yaml
    debug: true
    
    # JD_COOKIES配置, 一行一个, -符号是必须的。
    jd_cookies: 
      - 使用pt_key: pt_pin=jd_78b;pt_key=AAJgyqEMOsFQr5a0ucVzJepxU;
      - 使用ws_key: pt_pin=jd_78b;ws_key=AAJgyqEMOsFQr5a0ucVzJepxU;
      
      # 如需给cookie添加备注, 可在其后面添加: `remark=账号1;`, 例如:`pt_pin=jd_78b;pt_key=AAJgyqEMOsFQr5a0ucVzJepxU;remark=账号1;`
      - pt_pin=jd_78b;pt_key=AAJgyqEMOsFQr5a0ucVzJepxU;remarl=账号1;
    # 此处省略更多配置
    ```

- 配置好JD_COOKIES, 随便运行一个脚本检查配置, 如: `python jd_bean_change.py`.

- 内置定时任务, 配好JD_COOKIES自动会执行脚本。

- 消息通知, 配置config.yaml中的notify块
  - TG机器人: 配置tg_bot_token和tg_user_id
  - pushplus: 一对一只需要配置push_plus_token, 一对多还需要配置push_plus_group
  - 企业微信应用消息：配置qywx_am  （依次填上corpid的值,corpsecret的值,touser的值,agentid,media_id的值，注意用,号隔开。）
  - server酱: 配置server_send_key

## 配置说明

- 请查看/scripts/conf/config.yaml中的配置项。


## 注意

- 所有活动优先内部账号助力, 如有剩余助力次数，将会助力作者和助力池。
- 助力码自动提交助力池。

- 如果我的项目对你有帮助:

![](./static/imgs/wechat.jpg?width=80)


## 特别声明: 

* 本仓库发布的jd_scripts项目中涉及的任何解锁和解密分析脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断.

* 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。

* ClassmateLin对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.

* 间接使用脚本的任何用户在某些行为违反国家/地区法律或相关法规的情况下进行传播, ClassmateLin对于由此引起的任何隐私泄漏或其他后果概不负责.

* 请勿将jd_scripts项目的任何内容用于商业或非法目的，否则后果自负.

* 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，本人将在收到认证文件后删除相关脚本.

* 以任何方式查看此项目的人或直接或间接使用该jd_scripts项目的任何脚本的使用者都应仔细阅读此声明。ClassmateLin保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或jd_scripts项目的规则，则视为您已接受此免责声明.

**您必须在下载后的24小时内从计算机或手机中完全删除以上内容.**  </br>
***您使用或者复制了本仓库且本人制作的任何脚本，则视为`已接受`此声明，请仔细阅读*** 

































































## 脚本列表

- **脚本总数: 65**

|脚本名称|脚本描述|
|:---:|:---:|
|batch_run.py| 批量运行当前目录下的所有以jd, jr, jx, dj开头的活动脚本。|
|check_cookies.py| 检查cookies是否过期, 过期则发送通知|
|clean_log.py| 清除日志, 默认保留三天, 可在配置中修改|
|dj_bean.py| 京东APP->京东到家->签到->所有任务|
|dj_bean_manor.py| 京东APP->京东到家->签到->鲜豆庄园|
|dj_bean_manor_water.py| 京东APP->京东到家->签到->鲜豆庄园, 定时领水滴/浇水|
|dj_fruit.py| 京东APP->京东到家->免费水果|
|dj_fruit_collect.py| 京东APP->京东到家->免费水果, 定时领水滴/浇水|
|get_jd_cookies.py| 京东APP扫码登录获取cookies|
|jd_5g_box.py| 京东APP->营业厅->领京豆, 5G盲盒做任务抽奖|
|jd_5g_box_collect.py|  京东APP->营业厅->领京豆, 5G盲盒每3小时收取信号值|
|jd_amusement_post.py| 京东APP->签到领豆->边玩边赚->京小鸽游乐寄|
|jd_bean_change.py| 京豆红包变动通知|
|jd_bean_home.py| 京东APP->我的->签到领京豆->领额外奖励|
|jd_bean_indiana.py| 京豆APP首页->领京豆->摇京豆->左上角京豆夺宝|
|jd_big_winner.py| 京东急速版APP->我的->发财大赢家|
|jd_cash.py| 京东APP->搜索领现金进入|
|jd_collar_bean.py| 京东APP首页->领京豆->升级赚京豆|
|jd_cool_summer.py| 清凉一夏|
|jd_crazy_joy.py| 京东APP-签到领豆-疯狂的JOY|
|jd_cute_pet.py| 京东APP->我的->东东萌宠|
|jd_earn.py| 微信小程序->京东赚赚|
|jd_earn_bean.py| 赚京豆(微信小程序)-赚京豆-签到领京豆|
|jd_factory.py| 京东APP->京东电器->东东工厂|
|jd_factory_collect.py| 京东APP->京东电器->东东工厂, 定时收电量|
|jd_farm.py| 京东APP-我的->东东农场|
|jd_flash_sale_box.py| 京东APP->品牌闪购->闪购盲盒|
|jd_gold_creator.py| 京东APP->排行榜->金榜创造营|
|jd_good_morning.py| 京东APP首页->领京豆->早起福利|
|jd_health.py| 京东APP->我的->签到领豆->边玩边赚->东东健康社区|
|jd_health_collect.py| 京东APP->我的->签到领豆->边玩边赚->东东健康社区, 定时收能量|
|jd_joy.py| 京东APP->我的->宠汪汪|
|jd_joy_exchange.py| 京东APP->我的->宠汪汪, 兑换京豆, 优先兑换500, 兑换失败则兑换20.|
|jd_joy_feed.py| 京东APP->我的->宠汪汪, 定时喂狗|
|jd_koi_red_packet.py| 京东APP-签到领豆-边玩边赚-玩锦鲤红包|
|jd_lottery_bean.py| 京东APP->签到领京豆->抽京豆|
|jd_lucky_turntable.py| 幸运大转盘, 入口忘了在哪|
|jd_planting_bean.py| 京东APP->我的->签到领豆->种豆得豆|
|jd_planting_bean_collect.py| 京东APP->我的->签到领豆->种豆得豆, 定时收取营养液|
|jd_polite.py| 小鸽有礼|
|jd_puzzle_sign.py| 京东APP->拼图签到合集|
|jd_ranking_list.py| 今日王牌, 入口忘了在哪。|
|jd_school_charging.py| 京东APP->我的->签到领豆->边玩边赚->开学充电站|
|jd_second_coin.py| 京东APP首页->京东秒杀->立即签到->赚秒秒币|
|jd_shark_bean.py| 京东APP->我的->签到领豆->摇京豆|
|jd_shop.py| 京东APP首页->领京豆->进店领豆|
|jd_sign.py| 京东签到合集|
|jd_smash_golden_egg.py| 京东APP-每日特价-疯狂砸金蛋|
|jd_super_brand.py| 特务Z|
|jd_supermarket.py| 京东APP首页->京东超市->游戏|
|jd_try.py| 京东APP->我的->更多工具->新品试用|
|jd_unsubscribe.py| 取消商品关注和店铺关注|
|jd_wishing_pool.py| 京东APP首页->京东众筹->众筹许愿池|
|jd_women_box.py| 女装盲盒|
|jd_wonderful_lottery.py| 京东APP->签到领豆->边玩边赚->每日抽奖|
|jr_daily_take_goose.py| 京东金融APP->天天提鹅|
|jr_daily_take_goose_collect.py| 京东金融APP->天天提鹅， 定时收鹅蛋|
|jr_money_tree.py| 京东APP->我的->摇钱树|
|jr_money_tree_collect.py| 京东APP->我的->摇钱树, 定时收金果|
|jr_pet_pig.py| 京东金融APP->我的->养猪猪|
|jx_factory.py| 京喜App->我的->京喜工厂|
|jx_factory_collect.py| 京喜App->我的->京喜工厂, 定时收电量|
|jx_pasture.py| 京喜APP->京喜牧场->日常任务|
|jx_pasture_collect.py| 京喜APP->京喜牧场->定时收金币/割草/投喂小鸡|
|jx_sign.py| 京喜APP->首页->签到领红包|
