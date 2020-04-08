FROM nginx:alpine

RUN echo "now building..."

RUN apk add --update git
RUN apk add --update bash
RUN apk add --update gawk
RUN apk add --update sed
RUN apk add --update rsync
RUN apk add --update fcgiwrap
RUN apk add --update spawn-fcgi
RUN apk add --update curl
RUN apk add --update coreutils
# RUN apk add --update alpine-pandoc

RUN wget https://github.com/jgm/pandoc/releases/download/2.3.1/pandoc-2.3.1-linux.tar.gz
RUN tar xvzf pandoc-2.3.1-linux.tar.gz --strip-components 1 -C /usr/local

ENV TERM dumb
ENV USER root

WORKDIR /usr/app

COPY ./src .
COPY ./misc/nginx/default.conf /etc/nginx/conf.d/
COPY ./misc/nginx/fcgiwrap /etc/init.d/


# RUN sed -i 's/www-data/nginx/g' /etc/init.d/fcgiwrap
RUN chown nginx:nginx /etc/init.d/fcgiwrap
RUN ./deploy

COPY ./misc/nginx/index.cgi /usr/share/nginx/html/bashcms2/index.cgi
RUN chown nginx:nginx /usr/share/nginx/html/bashcms2/index.cgi
RUN chmod 755 /usr/share/nginx/html/bashcms2/index.cgi

# CMD sh /usr/app/deploy
# ENTRYPOINT ["sh", "/usr/app/deploy"]

CMD spawn-fcgi -s /var/run/fcgiwrap.socket /usr/bin/fcgiwrap && \
     chmod g+w /var/run/fcgiwrap.socket && \
     chgrp nginx /var/run/fcgiwrap.socket && \
    nginx -g "daemon off;"

# CMD /etc/init.d/fcgiwrap start \
#     && nginx -g 'daemon off;'
