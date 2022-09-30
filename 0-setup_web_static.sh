#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

sudo apt-get -y update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'
sudo mkdir -p /data/web_static/shared/ /data/web_static/releases/test/
sudo chown -hR "$USER":"$USER" /data
sudo touch /data/web_static/releases/test/index.html
echo "This is a test" > /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo sed -i '/listen [::]:80 default_server;/a\\tlocation /hbnb_static/ { alias /data/web_static/current/;}' /etc/nginx/sites-available/default
sudo service nginx restart
