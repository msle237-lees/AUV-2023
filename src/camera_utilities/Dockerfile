FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py src/main.py

CMD ["python3", "src/main.py"]
