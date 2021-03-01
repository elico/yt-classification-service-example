FROM golang:alpine AS redwood-build-env
LABEL maintainer "Eliezer Croitoru <ngtech1ltd@gmail.com>"

COPY init-local-rootca.sh /init-local-rootca.sh

# Install OS-level dependencies.
RUN apk add --no-cache curl git vim bash wget patch tar util-linux ca-certificates openssl && \
	git clone --single-branch --depth 1 https://github.com/elico/redwood /root/redwood && \
	cd /root/redwood && \
	CGO_ENABLED=0 go build -o /root/redwood/redwood


RUN /bin/bash /init-local-rootca.sh


FROM alpine:latest

RUN apk add --no-cache curl git vim bash wget patch tar supervisor ca-certificates openssl && rm  -rf /tmp/* /var/cache/apk/*

ADD supervisord.conf /etc/

## Create Filesystem
RUN mkdir -p /var/lib/redwood && \
	mkdir /var/lib/redwood/categories-enabled && \
	mkdir /var/lib/redwood/categories-avaliable && \
	mkdir /var/lib/redwood/static && \
	mkdir /var/lib/redwood/cgi && \
	mkdir /var/log/redwood && \
	mkdir /etc/redwood && \
	mkdir /etc/redwood/pruning.d && \
	mkdir /etc/redwood/acls.d && \
	mkdir /etc/ssl-cert && \
	ln -s /etc/redwood/ssl-cert/myCA-cert.pem /var/lib/redwood/static/ && \
	ln -s /etc/redwood/ssl-cert/myCA-cert.der /var/lib/redwood/static/ && \
	git clone https://github.com/andybalholm/redwood-config /var/lib/redwood/example-config

COPY reload-1 /etc/redwood/reload

COPY block.html /var/lib/redwood/static/

COPY acls.conf /etc/redwood/
COPY pruning.conf /etc/redwood/
COPY safesearch.conf /etc/redwood/

COPY redwood.conf /etc/redwood/

COPY --from=redwood-build-env /root/redwood/redwood /redwood

## 
COPY --from=redwood-build-env /myCA.pem /etc/redwood/ssl-cert/
COPY --from=redwood-build-env /myCA-cert.pem /etc/redwood/ssl-cert/

COPY --from=redwood-build-env /myCA-cert.der /etc/redwood/ssl-cert/



COPY redwood-superviserod.conf /etc/supervisor/conf.d/

RUN mkdir /var/lib/redwood/categories-avaliable/localbump && \
    cd /var/lib/redwood/ && \
    echo -e "description: SSL-BUMP\naction: ignore\n" > categories-avaliable/localbump/category.conf && \
    echo -e "default 500\n\nyoutube.com\nytimg.com\nyoutu.be\n" > categories-avaliable/localbump/domains.list && \ 
    cd categories-enabled && \
    cp -rv ../categories-avaliable/localbump localbump && \
    cp -rv ../example-config/categories/pornography pornography-example

VOLUME /var/lib/redwood
VOLUME /var/log/redwood
VOLUME /etc/redwood

#ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]
ENTRYPOINT ["/redwood", "-c", "/etc/redwood/redwood.conf"]
