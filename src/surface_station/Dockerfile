FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    python3-tk

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY placeholder.png .
COPY configs configs
RUN mkdir -p /app/logs

CMD ["python3", "main.py"]
