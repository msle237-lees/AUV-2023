FROM python:3.11.0a1-alpine3.14
WORKDIR /src/camera_package
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]