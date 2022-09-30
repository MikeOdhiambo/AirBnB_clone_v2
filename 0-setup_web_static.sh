#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

apt-get -y update
apt-get -y install nginx
ufw allow 'Nginx HTTP'
mkdir -p /data/web_static/shared/ /data/web_static/releases/test/
chown -hR ubuntu:ubuntu /data
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
sed -i '/listen 80 default_server;/a\\tlocation /hbnb_static/ { alias /data/web_static/current/;}' /etc/nginx/sites-available/default
sudo service nginx restart
