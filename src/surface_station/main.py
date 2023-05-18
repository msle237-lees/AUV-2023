# Import graphical interface library
import PySimpleGUI as sg

# Import numpy for data manipulation and numpysocket for data transfer
import numpy as np
from numpysocket import NumpySocket as nps

# Import threading for multithreading
import threading

# Import matplotlib.pyplot for plotting
import matplotlib.pyplot as plt

# Import time and datetime for timekeeping and logging
import time
import datetime as dt

# Import yaml for configuration file parsing
import yaml

# Import logging for logging
import logging as log

# Import os for file manipulation
import os

# Define some constants
bar_max = 2000
bar_min = 1000
bar_mid = (bar_max + bar_min) / 2

# Set the gui theme
sg.theme('DarkAmber')

# Create the layout for the GUI
# Right layout (motor data) ( 8 motors and 3 servos)
right_layout = [
    [sg.Text('Actuator Data', font=('Helvetica', 25))],
    [sg.HorizontalSeparator()],
    [sg.Text('Motor Data', font=('Helvetica', 25))],
    [sg.HorizontalSeparator()],
    [sg.Text('Motor 1', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor1')],
    [],
    [sg.Text('Motor 2', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor2')],
    [],
    [sg.Text('Motor 3', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor3')],
    [],
    [sg.Text('Motor 4', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor4')],
    [],
    [sg.Text('Motor 5', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor5')],
    [],
    [sg.Text('Motor 6', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor6')],
    [],
    [sg.Text('Motor 7', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor7')],
    [],
    [sg.Text('Motor 8', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='motor8')],
    [sg.HorizontalSeparator()],
    [sg.Text('Servo Data', font=('Helvetica', 25))],
    [sg.HorizontalSeparator()],
    [sg.Text('Servo 1', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='servo1')],
    [],
    [sg.Text('Servo 2', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='servo2')],
    [],
    [sg.Text('Servo 3', font=('Helvetica', 20)), sg.ProgressBar(bar_max, orientation='h', size=(20, 20), key='servo3')],
]

# Left layout (sensor data and button controls) (Depth, Temperature, Humidity, Voltage, Current, and Power Draw)
left_layout = [
    [sg.Text('Sensor Data', font=('Helvetica', 25))],
    [sg.HorizontalSeparator()],
    [sg.Text('Depth', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='depth'), sg.Text('m', font=('Helvetica', 20))],
    [],
    [sg.Text('Temperature', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='temperature'), sg.Text('°C', font=('Helvetica', 20))],
    [],
    [sg.Text('Humidity', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='humidity'), sg.Text('%', font=('Helvetica', 20))],
    [],
    [sg.Text('Voltage', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='voltage'), sg.Text('V', font=('Helvetica', 20))],
    [],
    [sg.Text('Current', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='current'), sg.Text('A', font=('Helvetica', 20))],
    [],
    [sg.Text('Power Draw', font=('Helvetica', 20)), sg.Text('0', font=('Helvetica', 20), key='power_draw'), sg.Text('W', font=('Helvetica', 20))],
    [sg.HorizontalSeparator()],
    [sg.Text('Controls', font=('Helvetica', 25))],
    [sg.HorizontalSeparator()],
    [sg.Checkbox('Enable Motors', font=('Helvetica', 20), key='enable_motors')],
    [sg.Checkbox('Enable Servos', font=('Helvetica', 20), key='enable_servos')],
    [sg.Checkbox('Enable Sensors', font=('Helvetica', 20), key='enable_sensors')],
    [sg.Checkbox('Enable Camera', font=('Helvetica', 20), key='enable_camera')],
    [sg.HorizontalSeparator()],
    [sg.Button('Update Config', font=('Helvetica', 15), key='update_config', size=(18, 1))],
    [sg.Button('Save Config', font=('Helvetica', 15), key='save_config', size=(18, 1))],
    [sg.Button('Load Config', font=('Helvetica', 15), key='load_config', size=(18, 1))],
    [sg.Button('Start', font=('Helvetica', 15), key='start', size=(18, 1))],
    [sg.Button('Stop', font=('Helvetica', 15), key='stop', size=(18, 1))],
    [sg.Button('Exit', font=('Helvetica', 15), key='exit', size=(18, 1))]
]

# Middle layout (Title, camera feed, and quick settings) ( # TODO: Add quick settings)
middle_layout = [
    [sg.Text('Surface Station', font=('Helvetica', 25), justification='center')],
    [sg.Image(filename='placeholder.png', key='motor_data', size=(1280, 720))],
    [sg.HorizontalSeparator()],
    [sg.Text('Quick Settings', font=('Helvetica', 25))],
    [sg.HorizontalSeparator()],
    [
        sg.VerticalSeparator(),
        sg.Column(
            [
                [sg.Text('Motor Power Execution', font=('Helvetica', 20))],
                [sg.Slider(range=(0, 100), default_value=50, orientation='h', size=(30, 20), key='motor_power_efficiency')],
                [sg.HorizontalSeparator()],
                [sg.Text('Camera FPS', font=('Helvetica', 20))],
                [sg.Slider(range=(30, 60), default_value=60, orientation='h', size=(30, 20), key='camera_fps')],
            ], justification='center', element_justification='center'
        ),
        sg.VerticalSeparator(),
        sg.Column(
            [
                [sg.Button('Save Settings', font=('Helvetica', 20), key='save_settings')],
                [sg.Button('Load Settings', font=('Helvetica', 20), key='load_settings')],
                [sg.Button('Reset Settings', font=('Helvetica', 20), key='reset_settings')]
            ], justification='center', element_justification='center'
        )
    ]
]

# Main layout (combines all layouts into one)
layout = [
    [
        sg.Column(right_layout, key='motor_data', size=(320, 1080), element_justification='center'),
        sg.Column(middle_layout, key='settings', size=(1280, 1080), element_justification='center'),
        sg.Column(left_layout, key='sensor_data', size=(320, 1080), element_justification='center')
    ]
]

# Creates the window with the layout and size of 1920x1080
window = sg.Window('Surface Station', layout, size=(1920, 1080), element_justification='center', finalize=True)

# Load the main config file
with open('configs/config.yml', 'r') as conf:
    config = yaml.load(conf, Loader=yaml.FullLoader)
    
# If config['AUV'] is true, then the config folder is configs/AUV/
if config['AUV']:
    config_path = 'configs/AUV/'
else:
    config_path = 'configs/ROV/'
    
# Load the settings file
with open('configs/settings.yml', 'r') as conf:
    settings = yaml.load(conf, Loader=yaml.FullLoader)
    
# Update the window with the settings
for key, value in settings.items():
    window[key].update(value)

# TODO: Add the ability to update the config file for each node

# TODO: Add the network code

# Main loop
while True:
    # Read the window for events
    event, values = window.read()
    
    # Debugging
    # print(event, values)
    
    # Handle events
    # save_settings
    if event == 'save_settings':
        with open('configs/settings.yml', 'w') as conf:
            yaml.dump(values, conf)
    
    # update_config 
    elif event == 'update_config':
        pass

    # load_config
    elif event == 'load_config':
        pass

    # save_config 
    elif event == 'save_config':
        pass
    
    # start 
    elif event == 'start':
        pass
    
    # stop 
    elif event == 'stop':
        pass
    
    # exit or window closed
    if event == sg.WINDOW_CLOSED or event == 'exit':
        break

window.close()

# Event List
    # save_settings 
    # update_config 
    # save_config 
    # start 
    # stop 
    # exit 
# Values List
# {'motor_power_efficiency': 50.0, 'camera_fps': 60.0, 'enable_motors': False, 'enable_servos': False, 'enable_sensors': False, 'enable_camera': False}