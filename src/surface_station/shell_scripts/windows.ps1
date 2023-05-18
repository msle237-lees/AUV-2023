echo "Checking if Docker is installed..."
if (!(Get-Command "docker" -ErrorAction SilentlyContinue)) {
    echo "Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit
}

echo "Building Docker image..."
docker build -t surface_station ../

echo "Running Docker container..."
# Please replace this IP with your local IP. Use `ipconfig` to find your local IP address
$IP = "your-local-ip-here"
docker run -e DISPLAY=$IP:0.0 surface_station
