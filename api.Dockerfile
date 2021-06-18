FROM python:3.8

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /api
COPY . .

EXPOSE 8000




