FROM ubuntu:latest
FROM python:3.7
FROM continuumio/anaconda3

MAINTAINER zhipeng.ye19@student.xjtlu.edu.cn

ENV PATH /usr/local/bin:$PATH

ADD . /crawler

WORKDIR /workspace

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD python __main__.pcony