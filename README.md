# Blog 个人博客系统
环境:Ubuntu18.04  pycharm 2018.1.2 <br>
框架语言: flask1.1.2+bootstrap4+python3.7+nginx1.14+gunicorn <br>

# 环境变量
vi ~/.bashrc <br> 
export PYTHONPATH="your project root path" <br>
export PATH=$PYTHONPATH:$PATH <br>

# nginx 安装
sudo apt-get install nginx

# nginx 配置文件
touch /etc/nginx/site_enabled/aweblog.conf
# 生成虚拟数据
flask gen-fake-data --cn 10
# 启停脚本
cd Flask_bird/bin <br>
停: stop.sh <br>
启: start.sh <br>

# admin 账号
username:admin   <br>
password:admin123 <br>

# 项目展示
评论列表<br>
![comments.png](https://github.com/Astrivemanlw/Blog/blob/master/comments.png)  <br>
文章编辑<br>
![edit_post.png](https://github.com/Astrivemanlw/Blog/blob/master/edit_post.png) <br>
主页<br>
![home.png](https://github.com/Astrivemanlw/Blog/blob/master/home.png) <br>
登陆界面<br>
![login.png](https://github.com/Astrivemanlw/Blog/blob/master/login.png) <br>
文章管理<br>
![post_manage.png](https://github.com/Astrivemanlw/Blog/blob/master/post_manage.png) <br>

#github图片访问过慢或报错解决办法

```
# 访问https://www.ipaddress.com  根据域名获取ip地址
140.82.113.3	github.com
199.232.5.194	github.global.ssl.fastly.net

192.30.253.119    gist.github.com
151.101.184.133    assets-cdn.github.com
151.101.184.133    raw.githubusercontent.com
151.101.184.133    gist.githubusercontent.com
151.101.184.133    cloud.githubusercontent.com
151.101.184.133    camo.githubusercontent.com
151.101.184.133    avatars0.githubusercontent.com
151.101.184.133    avatars1.githubusercontent.com
151.101.184.133    avatars2.githubusercontent.com
151.101.184.133    avatars3.githubusercontent.com
151.101.184.133    avatars4.githubusercontent.com
151.101.184.133    avatars5.githubusercontent.com
151.101.184.133    avatars6.githubusercontent.com
151.101.184.133    avatars7.githubusercontent.com
151.101.184.133    avatars8.githubusercontent.com
```