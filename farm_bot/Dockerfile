FROM python:3.7

WORKDIR /usr/src/farm_bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/farm_bot/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/farm_bot
CMD ["python", "/usr/src/farm_bot/farm_bot.py"]