FROM python:3.9.6
LABEL maintainer="jameelhamdan99@yahoo.com"
COPY requirements.txt /
RUN pip install -U pip && pip install -r requirements.txt
WORKDIR /usr/src/app
COPY . .
RUN chmod -R +x release.sh
