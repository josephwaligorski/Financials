# frontend/Dockerfile
# This new file builds our custom Nginx image.

# Start from the official Nginx image
FROM nginx:alpine

# Copy our custom configuration file into the container.
# This replaces the default Nginx configuration.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# No other steps are needed. The base image handles the rest.
