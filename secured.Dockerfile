# Use specific NGINX version
FROM nginx:1.21.5

# Update packages and install security updates
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#Copy NGINX configuration file
COPY nginx.conf /etc/nginx/nginx.conf

#Copy static website files
COPY html /usr/share/nginx/html

#Set NGINX user and group to non-root
RUN chown -R nginx:nginx /usr/share/nginx/html \
    && chmod -R 755 /usr/share/nginx/html

#Expose port 30052 (custom port for customer can be added here)
EXPOSE 30052

#Run NGINX in the foreground
CMD ["nginx", "-g", "daemon off;"]
