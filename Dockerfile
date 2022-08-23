# syntax=docker/dockerfile:1

FROM python:3.10-alpine

WORKDIR /app

COPY docker/pip_requirements.txt  requirements.txt
RUN pip3 install -r requirements.txt

COPY src /app

CMD ["python3", "/app/main.py", "/app/conf/config.yml"]