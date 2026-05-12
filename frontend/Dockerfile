# Use the official Nginx image as a base
FROM nginx:alpine

# Copy the frontend files to the Nginx default public directory
COPY . /usr/share/nginx/html

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 80 to the outside world
EXPOSE 80

# Use the entrypoint script to inject env vars
ENTRYPOINT ["/entrypoint.sh"]

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
