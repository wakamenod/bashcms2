FROM nginx:alpine

RUN echo "now building..."

RUN apk add --update git
RUN apk add --update bash
RUN apk add --update gawk
RUN apk add --update sed
#RUN apk add --update pandoc

ENV TERM dumb
ENV USER root

WORKDIR /usr/app

COPY . .
