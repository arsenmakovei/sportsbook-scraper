FROM python:3.10-slim
LABEL maintainer="makoveyarsen@gmail.com"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["scrapy", "crawl", "football", "-O", "test.csv"]