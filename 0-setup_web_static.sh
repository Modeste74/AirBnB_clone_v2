#!/usr/bin/env bash
# installs nginx and configures it
sudo apt update
sudo apt -y install nginx

#creates folders
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# creates a HTML test file
echo "Test html for hbnb_project" > /var/www/html/index.html

# creates a symbolic link and deletes already exists and recreates it
rm -f /data/web_static/current && ln -s /data/web_static/releases/test/ /data/web_static/current

# giving onwership to user and group
sudo chown -R ubuntu:ubuntu /data/

# updating the nginx config file to serve the content 
echo 'server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /var/www/html;
    index index.html index.nginx-debian.html;
   
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.nginx-debian.html;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/;
    }

    error_page 404 /error_404.html;
    location / {
        # First attempt to serve request as file, then
        # as directory, then fall back to displaying a 404.
        try_files $uri $uri/ =404;
    }
}' | sudo tee /etc/nginx/sites-available/default > /dev/null
sudo service nginx restart
