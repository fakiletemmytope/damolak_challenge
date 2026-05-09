# Use the official Nginx image as a base
FROM nginx:alpine

# Copy the frontend files to the Nginx default public directory
COPY . /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
