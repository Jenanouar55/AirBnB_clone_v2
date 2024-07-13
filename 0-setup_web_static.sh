#!/usr/bin/env bash
# Script to set up web servers for the deployment of web_static

if ! nginx -v &> /dev/null; then
    apt-get update
    apt-get install -y nginx
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

if ! grep -q "location /hbnb_static/" /etc/nginx/sites-available/default; then
    sed -i '/server_name _;/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default
fi

service nginx restart

exit 0
