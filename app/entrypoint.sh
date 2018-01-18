#! /usr/bin/env bash
set -e
# Get the maximum upload file size for Nginx, default to 0: unlimited
USE_NGINX_MAX_UPLOAD=${NGINX_MAX_UPLOAD:-0}
# Generate Nginx config for maximum upload file size
echo "client_max_body_size $USE_NGINX_MAX_UPLOAD;" > /etc/nginx/conf.d/upload.conf

# Get the listen port for Nginx, default to 80
USE_LISTEN_PORT=${LISTEN_PORT:-80}

echo "server {
  listen ${USE_LISTEN_PORT};

  location @app {
    include uwsgi_params;
    uwsgi_pass unix:///tmp/uwsgi.sock;
  }
  location /api/ {
    try_files \$uri @app;
  }
  location / {
    root /app/front;
    index index.html;
    expires 0;
  }
}" > /etc/nginx/conf.d/nginx.conf

exec "$@"