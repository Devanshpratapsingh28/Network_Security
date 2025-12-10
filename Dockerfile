FROM python:3.10-slim-bullseye

WORKDIR /app
COPY . /app

RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
