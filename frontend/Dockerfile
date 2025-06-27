# frontend/Dockerfile
# This file now copies ALL frontend assets into the image.

# Start from the official Nginx image
FROM nginx:alpine

# Copy our custom Nginx configuration file.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# ADDED: Copy the frontend application files into the Nginx web root.
COPY index.html /usr/share/nginx/html/
