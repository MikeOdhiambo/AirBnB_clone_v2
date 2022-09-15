#!/usr/bin/env bash
# sets up web servers for the deployment of web static
apt-get update
apt-get -y install nginx
/etc/init.d/nginx start
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared
echo -e "testing nginx configuration\n" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test /data/web_static/current
chown ubuntu:ubuntu -R /data
f=/etc/nginx/sites-available/default
rm $f
echo -e "server {
    listen 80 default_server;
    root /usr/share/nginx/html;
    index index.html index.htm;
    add_header X-Served-By $HOSTNAME;
    location /redirect_me {
        return 301 https://www.youtube.com;
    }
    location /hbnb_static {
        alias /data/web_static/current;
    }
}" > $f
service nginx restart
