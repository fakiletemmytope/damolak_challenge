#!/bin/sh
# Replace environment variables in the config template
envsubst '${API_BASE_URL}' < /usr/share/nginx/html/js/config.js.template > /usr/share/nginx/html/js/config.js

# Start Nginx
exec "$@"
