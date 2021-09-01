#!/bin/bash
echo "######开始执行更新脚本######"

if [ -z $CODE_DIR ]; then
  CODE_DIR=/scripts
fi

if [ -z $REPO_URL ]; then
  REPO_URL=https://github.com/ClassmateLin/jd_scripts.git
fi

if [ ! -f "/root/.ssh/id_rsa" ]; then
  echo -e "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA18ht1+0SbjGfPGpIf//nkQDatLRBrpcMKPehR/tdotn00ar/\nKWOqisZtWAyPMmm1KLYHEWe0Nzunm43W4YQpM2o1HOFghwaSCYGYZUuebipB/3jM\n6bSdYtHJIKDsJBZ2J/AJu3NnPjQLxkjzWKySb+f8ZkLhYzmdkx0Lu2Vi0jXVqnwn\nqDOhaZy8BYeFWHFluDjzC1Cmcbkrn5Hj2hKwdyIsRdDGxbYau1T8TVyAPGzmoL1O\nZlzsPAfXxtMesOKbLhOgYzU73lEmC4SUbVzg0kU2CfAc9z4+sYd9gTCFR8L7L6lr\ng7zjvSIvPEYK0ordwHXefJPL1XbP8+n/HmNzgQIDAQABAoIBAQCFtOMjdfoCn+rc\ng7sS3V3+wrnCWSON7HiTdgXQ1ZgKzeVeegeL/P7y6MteUMH2afvgExLEHS9VPji4\nMaahrMPe4QOyNpEaed7J1yy4L6gm+TZV9+N5OPqA/h8TgcNxBR4H1zwgk/y4VYWq\nQw/OtXgzsVr7fpusYUobm1bmsocOWzt03cBJ3YXcu0KVhK2NxsB8cOPEAgaLDZzO\nSx/zk7tAaOlDgrJpauq/o823ckKQy56zVpV2oaQWncvwYmX+FDzIUAt+MTVO73zz\nn0AjPaKQgbMC2DtejrGzEvDub7ydfMAvwN3LJa57z6iiDO36J+H6mxfBvB57cqj6\nV/Q1lIABAoGBAPsr+VSYKJSOlzyt0RUa4kKCpgmqY+YO7q/0jff30CPHHl88E2sR\nZSzlgDijBvb64hHTwSUNS0Cmfl2RzHdmS981pKYIgrCQlyaVA3ctOFF40rOFMXtw\nD/VirmA8MYuybktq5JW88z0nkvOB8rD58eOM1iTPywoiq2jo3ZGT+fsBAoGBANvu\nTiQKTSfpKru5VCojCuCk1mUW4Qw6pV2q8+UiVGjxX7jP5Ow5K9qi0mEQBkG3t2Du\n3gktWZg3cAflKh4Wbyb1dYdv0Vrk5fTgtPj/1KOIs1mIXJOt8AHfTpiWHkSMoQLt\nl+i+x1IQJyUSsRqsRl5c+LeFIfhDL++1QFGxQ/iBAoGBAIApyxr4XVSYgeFrjBGp\n2yQ3CERMVpdQrUjJkBukruditkPAIuRyRt8m6Et+HJKwJ+US2S5v3yNJEZfrSpru\nbu6hr7ctBorT7Ny6Er+gKmmgLlt+LmafIvWCehoO/PUcgh0nmSYy+ScOZ3SrrUvS\n7jO/bJHyGde9IxvwHwcmq9sBAoGADLcZY3IJBe6wHsxXNlxyS4ycLJoHBtr5JpI0\nqaGzeaHC4/94/8NKasiRGzV+9xu1CXCl+6fYjzldS8ePCNBJOtpkIiFv3C5xsRew\nvtijpZTIsbt1hsA+qQ0NETtUoqfywyWTa8xj37W5XaZYAO/G3bvIUWvsC9tukRBM\nmKyD/oECgYBghlogdkPHkZjT/J4KHAbNlHu2u378LE6obw1PU5U+Bn/KxgbumAQy\nGJiWCbZ6tf/3eSKThWE1SihHv9P0qUis+z4uvctNMRZ3ttnEGoDvNbOBRWW3xxSu\nAble5o/TFwAEtTfESt3gzx+BTjya+kdUckAuZDiN0xXw9dkRJqj+5w==\n-----END RSA PRIVATE KEY-----" >> /root/.ssh/id_rsa;
  chmod 600 /root/.ssh/id_rsa;
  ssh-keyscan gitee.com > /root/.ssh/known_hosts;
fi

if [ ! -d $CODE_DIR/.git ]; then
  echo "代码目录为空, 开始clone代码...";
  cd $CODE_DIR;
  git init;
  git branch -M master;
  git remote add origin $REPO_URL;
  git pull origin master;
  git branch --set-upstream-to=origin/master master;
fi

if ! type ps >/dev/null 2>&1; then
  echo "正在安装procps..."
  apt -y install procps
  apt clean;
else
    echo "procps 已安装";
fi

if ! type node >/dev/null 2>&1; then
  echo "正在安装nodejs...";
  apt -y install nodejs;
  apt clean;
else
    echo "nodejs 已安装";
fi

if ! type chromium >/dev/null 2>&1; then
    echo "开始安装chromium...";
    apt -y install chromium;
    apt clean;
    rm -f /root/.local/share/pyppeteer;
else
    echo 'chromium 已安装';
fi

if [ ! -d $CODE_DIR/conf ]; then
  echo "配置文件目录不存在, 创建目录...";
  mkdir -p $CODE_DIR/conf;
fi

if [ ! -d $CODE_DIR/logs ]; then
  echo "日志目录不存在, 创建目录...";
  mkdir -p $CODE_DIR/logs;
fi

if [ ! -f "$CODE_DIR/conf/config.yaml" ]; then
  echo "脚本配置文件不存在, 复制配置文件...";
  cp $CODE_DIR/.config.yaml $CODE_DIR/conf/config.yaml;
fi



if [ ! -f "$CODE_DIR/conf/crontab.sh" ]; then
  echo "自定义cron配置文件不存在, 复制配置文件..."
  cp $CODE_DIR/.crontab.sh $CODE_DIR/conf/crontab.sh;
fi


echo "git pull拉取最新代码...";
cd $CODE_DIR && git reset --hard && git pull;
echo "pip install 安装最新依赖...";
pip install -r $CODE_DIR/requirements.txt;
echo "更新docker-entrypoint...";
cp $CODE_DIR/shell/docker-entrypoint.sh /bin/docker-entrypoint;
chmod a+x /bin/docker-entrypoint;
chmod a+x /scripts/*.py;

echo "更新cron任务..."
crontab -r;
python $CODE_DIR/tools/update_config.py;
python $CODE_DIR/tools/update_default_crontab.py;
cat $CODE_DIR/shell/default_crontab.sh > /tmp/crontab;
echo -e "\n" >> /tmp/crontab;

cat $CODE_DIR/conf/crontab.sh >> /tmp/crontab;

crontab /tmp/crontab;

rm /tmp/crontab;

echo "重启cron进程...";

/etc/init.d/cron restart;

rm -rf $CODE_DIR/sqlite.db;

echo "######更新脚本执行完毕######";

# 保证容器不退出
tail -f /dev/null;
