echo "Building docker image"
docker build -t surface_station:latest .
echo "Ensuring X11 forwarding is enabled"
xhost + 10.0.0.100
echo "Starting docker container"
docker run --name surface_station -v /Users/user/Documents/AUV-2023/logs:/app/logs -a stdout -e DISPLAY=10.0.0.100:0 surface_station:latest
echo "Removing docker container"
docker rm surface_station