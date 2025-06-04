FROM python:3.10-slim

WORKDIR /code/m60

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/m60/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/