FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /bot
WORKDIR /bot

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7000

CMD python bot.py 0.0.0.0:7000
