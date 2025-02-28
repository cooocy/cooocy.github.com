---
title: nginx 配置
categories: developer
tags: [Nginx]
keywords: Nginx
cover: https://bk-5lian.oss-cn-shanghai.aliyuncs.com/timg-1569042620771.jpeg
date: 2019-09-21 13:10:30
---

```blog.conf``` 配置文件
```
worker_processes  1;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;

    keepalive_timeout  65;
	
	include		  myconf/*.conf;
	
	client_max_body_size 2048m;
	charset		  utf-8;

}
```

```blog.conf``` 配置文件
```
# 多个server，端口相同，server_name不同。
# 依据server_name，逐个向下匹配server，如果匹配不到，使用第一个server。

# http请求默认80端口

# 默认
server {
	listen 		80;
	location / {
		root   /projects/web/blog/default;
		index  index.html index.htm;
	}
	error_page   500 502 503 504  /50x.html;
	location = /50x.html {
		root   html;
	}
}

# 个人主页
server {
	listen       80;
	server_name  blog.5lian.ink;
	
	# 重定向到https
	return		 301 https://$server_name$request_uri; 
}	


# demo
server {
	listen 		80;
	server_name demo.blog.5lian.ink;
	location / {
		root   /projects/web/blog/demo;
		index  index.html index.htm;
	}
	error_page   500 502 503 504  /50x.html;
	location = /50x.html {
		root   html;
	}
}

# https请求默认443端口
server {
	listen       			443 ssl;
	server_name  			blog.5lian.ink;
	

	ssl_certificate      	../cert/blog.5lian.ink.pem;
	ssl_certificate_key  	../cert/blog.5lian.ink.key;

	ssl_session_cache    	shared:SSL:1m;
	ssl_session_timeout  	5m;

	ssl_ciphers  			ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
	ssl_protocols 			TLSv1 TLSv1.1 TLSv1.2;
	ssl_prefer_server_ciphers  on;

	location / {
		root   /projects/web/blog/5lian;
		index  index.html index.htm;
		# 如果直接访问域名，即以".com"结尾(https://*.mh.chaoxing.com)，跳转到/wiselib_web/html/index.html	
		# if ($request_uri ~* "^/$") {
		#	rewrite ^ https://$host/blog/index.html permanent;
		# }
	}
	
	# 反向代理到后端
	location /api/blog {
		proxy_redirect    off;
		rewrite  ^/api/blog/(.*)$ /$1 break;
		proxy_pass   https://127.0.0.1:8101;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	}
	
}
```