# rancid_back
#Pour installer le back
#Il faut installer python2.7
#pip install -r requirement.txt
#installer nginx

#creer un virtualenv
#virtualenv .venv (par exemple)

#Avec runit creer un service rancidgui
#lancer uwsgi en tant que rancid grace à ce script en modifiant apres --ini par le chemin du fichier .ini
#!/bin/sh
#exec sudo -u rancid /usr/local/bin/uwsgi --ini /opt/wui/var/conf/uwsgi/rancid.ini 2>&1

####Conf uwsgi:
#[uwsgi]
#socket = 127.0.0.1:5000
#master = true
#processes = 1
#enable-threads = true
#buffer-size = 8192
#need-app = true
#listen = 100
#log-syslog = uwsgi.wui
#chdir = /opt/wui/var/www/api
#virtualenv = /opt/wui/var/www/api/.venv
#module = python2.7
#file = run.py
#callable = app
#uid = rancid

#conf nginx:
#server {
#
#        listen 80;
#        server_name staging.wui.nx;
#
#        access_log /opt/wui/var/log/access.log ;
#        error_log  /opt/wui/var/log/error.log error;
#
#        root /opt/wui/var/www/wui/;
#        index index.php;
#
#        location ~* \.(?:jpg|jpeg|gif|png|ico|cur|gz|svg|svgz|mp4|ogg|ogv|webm|htc)$ {
#                expires 1M;
#                access_log off;
#                add_header Access-Control-Allow-Origin "$http_origin";
#                #add_header Cache-Control "public";
#        }
#
#
#        location / {
#                try_files $uri/ $uri index.js index.php /index.html;
#        }
#
#        location /index.html {
#                if_modified_since off;
#                etag off;
#                expires -1;
#        }
#        location ~ \.php$ {
#         include snippets/fastcgi-php.conf;
#
#         # # With php5-cgi alone:
#         # fastcgi_pass 127.0.0.1:9000;
#         # With php5-fpm:
#         fastcgi_pass unix:/var/run/php5-fpm.sock;
#         }
#
#        uwsgi_connect_timeout 5;
#        uwsgi_read_timeout 15;
#        uwsgi_send_timeout 15;
#        uwsgi_ignore_client_abort on;
#
#
#        location /api {
#                        add_header Access-Control-Allow-Origin "$http_origin";
#        		include uwsgi_params;
#                        uwsgi_pass 127.0.0.1:5000;
#                }
#        }
