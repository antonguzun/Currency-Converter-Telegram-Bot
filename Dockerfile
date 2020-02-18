FROM python:3.7.6-alpine3.11
WORKDIR /app

#RUN set -ex \
#    && apk add --no-cache -t build-deps \
#        alpine-sdk \
#        linux-headers \
#        jpeg-dev
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev


RUN set -ex \
    && pip install -U \
        pip \
        pip-tools \
        setuptools

COPY ./requirements.txt ./requirements.txt

RUN set -ex \
    && pip install --no-cache-dir  -r requirements.txt

CMD [ "python", "./bot.py" ]
