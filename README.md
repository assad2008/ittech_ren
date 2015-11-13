## 访问

<http://ittech.ren>

## Web Server

**Nginx**，使用淘宝的Nginx,地址：<http://tengine.taobao.org/>

## Python

**PyPy**，PyPy 2.5.0 with GCC 4.6.3 built on Ubuntu，地址：<http://pypy.org/>

## Python web framework

**Tornado**，地址：<http://www.tornadoweb.org/en/stable/>

## Markdown

**Markdown**，地址：<https://github.com/trentm/python-markdown2>

## Theme

**Light**，<https://github.com/hexojs/hexo-theme-light>

## Nginx配置

	log_format  yx  '$remote_addr - $remote_user [$time_local] "$request" '
				 '$status $body_bytes_sent "$http_referer" '
				 '"$http_user_agent" $http_x_forwarded_for';
				 
	upstream mdblogserver
		{
			server 127.0.0.1:8899;
		}

	server
		{
			listen       80;
			server_name itnote.it;
			index index.html index.htm;
			
			location ^~ /static/ {
				root /data0/mdblog;
			}
			
			location / {
				proxy_read_timeout 1800;
				proxy_pass_header Server;
				proxy_set_header Host $http_host;
				proxy_redirect off;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Scheme $scheme;
				proxy_pass http://mdblogserver;
			}

			location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
			{
				expires      30d;
			}

			location ~ .*\.(js|css)?$
			{
				expires      12h;
			}
			access_log  /home/wwwlogs/mdblog.log  yx;
		}
