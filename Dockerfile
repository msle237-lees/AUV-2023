FROM python:3.11.3-slim-buster

RUN apt-get update && apt-get install -y \
    python3-tk

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY src/main.py src/main.py
COPY imgs/placeholder.png imgs/placeholder.png
COPY layouts layouts
COPY configs configs
RUN mkdir -p /app/logs

CMD ["python3", "src/main.py"]