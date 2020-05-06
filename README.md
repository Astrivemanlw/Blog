# Blog 个人博客系统
环境:ubuntu18.04
组件: flask1.1.2+bootstrap4+python3.7+nginx1.14+gunicorn

# 环境变量
vi ~/.bashrc <br> 
export PYTHONPATH="your project root path" <br>
export PATH=$PYTHONPATH:$PATH <br>

# nginx 安装
sudo agt-get install nginx

# nginx 配置文件
touch /etc/nginx/site_enabled/aweblog.conf

# pycharm创建虚拟环境

# 启停脚本
cd Flask_bird/bin <br>
停: stop.sh <br>
启: start.sh <br>

# admin 账号
username:admin   <br>
password:admin123 <br>