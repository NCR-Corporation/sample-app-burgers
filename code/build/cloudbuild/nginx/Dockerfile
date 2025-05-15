ARG NGINX_VERSION
ARG NGINX_VARIANT

FROM nginx:1.15-alpine

WORKDIR /etc/nginx/
RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx

EXPOSE 8080/tcp
CMD ["nginx", "-g", "daemon off;"]