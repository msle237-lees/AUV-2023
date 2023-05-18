#!/bin/bash

echo "Checking if Docker is installed..."
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Attempting to install..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

echo "Building Docker image..."
docker build -t surface_station ../

echo "Running Docker container..."
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
xhost + $IP
docker run -e DISPLAY=$IP:0.0 surface_station
