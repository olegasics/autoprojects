FROM python:3.8

RUN apt update && apt install -y python3-pip

WORKDIR /etc/fluidbusiness/

COPY . /etc/fluidbusiness/

RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 5000