# Create a screen session to run the surface station node
screen -S surface_station "cd src/surface_station && docker build -t surface_station:latest src/surface_station && docker run --rm -e DISPLAY=10.0.0.163:0 -it surface_station:latest"

# Create a screen session to run the vlan controller node
screen -S vlan_controller "cd src/vlan_controller && docker build -t vlan_controller:latest src/vlan_controller && docker run --rm -it vlan_controller:latest"

# Create a screen session to run the camera node

# Create a screen session to run the movement package node

# Create a screen session to run the neural networks node

# Create a screen session to run the orin hardware node