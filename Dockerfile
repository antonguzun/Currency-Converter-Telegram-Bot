FROM python:3.6-slim

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir _media
VOLUME /_media
RUN python init_db.py

CMD python bot.py

