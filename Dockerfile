FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

RUN apt-get update -y \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

CMD ["python", "app.py"]
