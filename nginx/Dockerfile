FROM alpine:3.18

ARG NGINX_VERSION=1.24.0

RUN apk add --no-cache \
	 build-base pcre pcre-dev zlib zlib-dev openssl openssl-dev wget ca-certificates git \
 && wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz -P /usr/src \
 && tar xzf /usr/src/nginx-${NGINX_VERSION}.tar.gz -C /usr/src \
 && git clone https://github.com/arut/nginx-rtmp-module.git /usr/src/nginx-rtmp-module \
 && cd /usr/src/nginx-${NGINX_VERSION} \
 && ./configure \
	 --prefix=/etc/nginx \
	 --sbin-path=/usr/sbin/nginx \
	 --conf-path=/etc/nginx/nginx.conf \
	 --error-log-path=/var/log/nginx/error.log \
	 --http-log-path=/var/log/nginx/access.log \
	 --pid-path=/var/run/nginx.pid \
	 --with-compat \
	 --with-http_ssl_module \
	 --with-http_v2_module \
	 --add-module=/usr/src/nginx-rtmp-module \
 && make -j"$(nproc)" && make install \
 && adduser -D -g 'www' www \
 && mkdir -p /var/cache/nginx /var/run /var/log/nginx \
 && apk del build-base pcre-dev zlib-dev openssl-dev git wget \
 && rm -rf /var/cache/apk/* /usr/src/*

COPY default.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf


EXPOSE 80 1935

CMD ["nginx", "-g", "daemon off;"]
