FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py src/main.py

CMD ["python3", "src/main.py"]
