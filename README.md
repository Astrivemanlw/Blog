# Blog
ubuntu18.04 
flask1.1.2+bootstrap4+python3.7+ngnix1.14+gunicorn 个人博客系统

# 环境变量
vi ~/.bashrc <br> 
export PYTHONPATH="your project root path" <br>
export PATH=$PYTHONPATH:$PATH <br>

# 启停脚本
cd $HOME/Flask_bird/bin && ./stop.sh ./start.sh

# nginx 安装
sudo agt-get install nginx

# 编写配置文件
vi /etc/nginx/site_enabled/blog

