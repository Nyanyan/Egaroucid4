FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /web_egaroucid/
WORKDIR /web_egaroucid
ADD . /web_egaroucid/
RUN pip install -r requirements.txt
RUN apt update && apt install -y nano git

RUN python3 compile.py ai.cpp ai.out
EXPOSE 5000
