# This is the main file for the surface station of the AUV
# It is responsible for the following:
# 1. Receiving data from the connected joystick and toggle switches
# 2. Depending on the data received, it will change certain configuration variables
# 3. It will query the AUV for on status and battery level
# 4. It will send the configuration variables to the AUV
# 5. It will start the AUV if the user presses the start button
# 6. If in AUV mode, it will then start the autonomous mode and disconnect
# 7. If in manual mode, it will send the joystick data to the AUV

#!/usr/bin/env python3

# Import python libraries
import os
import sys
import datetime
import logging
import platform
import subprocess
from dataclasses import dataclass

# Import custom libraries
import PySimpleGUI as sg
import numpy as np
from numpysocket import NumpySocket
import serial
import yaml

@dataclass
class Joystick:
    x_axis: float
    y_axis: float
    z_axis: float

@dataclass
class Controller:
    left: Joystick
    right: Joystick
    buttons: dict


# Define the main class
class surfaceStation:
    def __init__(self):
        # Create an instance of the Controller class
        self.controller = Controller(Joystick(0.0, 0.0, 0.0), Joystick(0.0, 0.0, 0.0), 
                                {"button" + str(i): False for i in range(1, 11)})
        
        # Set the theme
        sg.theme('DarkAmber')
        
        # Initialize the logger to output to both the console and a file
        logging.basicConfig(
            filename='logs/surfaceStation.log', 
            filemode='a', 
            format='%(asctime)s - %(levelname)s - %(message)s', 
            level=logging.DEBUG)
        
        # Load the configuration file
        try:
            with open('configs/surface_station.yml', 'r') as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            logging.error('Error loading configuration file: {}'.format(e))
            sys.exit(1)
                      
        # If self.config['serial'] is true, then initialize the serial port at the specified baudrate and specified port
        if self.config['serial'] == 1:
            self.ser = serial.Serial(self.config['port'], self.config['baudrate'], timeout=int(self.config['timeout']))
            logging.info('Serial port initialized')
            
            # Read in the joystick data and store it in self.joystick
            self.joystick = self.ser.readline().decode('utf-8').strip().split(',')
            logging.info('Joystick data read in %s', self.joystick)
            
        else:
            self.ser = None
            logging.info('Serial port not initialized')
            
        title_size = (25, 1)
        label_size = (20, 1)
        data_label_size = (17, 1)
        data_size = (10, 1)
        font_size = 12
            
        # Define the layout of the GUI (these are stored in the layouts folder)
        try:
            layout = [
                [sg.Text('Surface Station', size=title_size,  font=("Helvetica", 25))],
                [sg.Column([
                    [sg.Text('AUV Configuration', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Mode', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='mode', size=data_size,  font=("Helvetica", font_size))],
                    [sg.Text('Serial', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='serial', size=data_size,  font=("Helvetica", font_size))],
                    [sg.Text('Motors', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='motors', size=data_size,  font=("Helvetica", font_size))],
                    [sg.Text('Camera', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='camera', size=data_size,  font=("Helvetica", font_size))],
                    [sg.Text('Servos', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='servos', size=data_size,  font=("Helvetica", font_size))],
                    [sg.Text('Sensors', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='sensors', size=data_size,  font=("Helvetica", font_size))],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Motor Configuration', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Motor Speed Max: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['motor_speed_max'], size=data_size, key='motor_speed_max',  font=("Helvetica", font_size))],
                    [sg.Text('Motor Speed Min: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['motor_speed_min'], size=data_size, key='motor_speed_min',  font=("Helvetica", font_size))],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Camera Configuration', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Camera 1 Res: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['camera_1_resolution'], size=data_size, key='camera_1_resolution',  font=("Helvetica", font_size))],
                    [sg.Text('Camera 2 Res: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['camera_2_resolution'], size=data_size, key='camera_2_resolution',  font=("Helvetica", font_size))],
                    [sg.Text('Camera 1 FPS: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['camera_1_fps'], size=data_size, key='camera_1_fps',  font=("Helvetica", font_size))],
                    [sg.Text('Camera 2 FPS: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['camera_2_fps'], size=data_size, key='camera_2_fps',  font=("Helvetica", font_size))],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Servo Configuration', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Servo 1 Min: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['servo_1_min'], size=data_size, key='servo_1_min',  font=("Helvetica", font_size))],
                    [sg.Text('Servo 1 Max: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['servo_1_max'], size=data_size, key='servo_1_max',  font=("Helvetica", font_size))],
                    [sg.Text('Servo 2 Min: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['servo_2_min'], size=data_size, key='servo_2_min',  font=("Helvetica", font_size))],
                    [sg.Text('Servo 2 Max: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['servo_2_max'], size=data_size, key='servo_2_max',  font=("Helvetica", font_size))],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Sensor Configuration', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Temperature Unit: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Combo(['Celsius', 'Fahrenheit'], default_value=self.config['temperature_unit'], size=data_size, key='temperature_unit',  font=("Helvetica", font_size))],
                    [sg.Text('Humidity Unit: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Combo(['%', 'g/m3'], default_value=self.config['humidity_unit'], size=data_size, key='humidity_unit',  font=("Helvetica", font_size))],
                    [sg.Text('Voltage Unit: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Combo(['V', 'mV'], default_value=self.config['voltage_unit'], size=data_size, key='voltage_unit',  font=("Helvetica", font_size))],
                    [sg.Text('Current Unit: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Combo(['A', 'mA'], default_value=self.config['current_unit'], size=data_size, key='current_unit',  font=("Helvetica", font_size))],
                    [sg.Text('IMU Axis Min: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['imu_axis_min'], size=data_size, key='imu_axis_min',  font=("Helvetica", font_size))],
                    [sg.Text('IMU Axis Max: ', size=data_label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['imu_axis_max'], size=data_size, key='imu_axis_max',  font=("Helvetica", font_size))],
                    [sg.Text('Pressure Unit: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Combo(['Pa', 'hPa', 'kPa', 'MPa'], default_value=self.config['pressure_unit'], size=data_size, key='pressure_unit',  font=("Helvetica", font_size))],
                    [sg.HorizontalSeparator()],
                ], size=(320, 1080)),
                sg.Column([
                    [sg.Image('imgs/placeholder.png', key='camera_feed', size=(1280, 720))],
                    [
                        sg.Column([
                            [sg.Text('Orin Status', size=label_size,  font=("Helvetica", font_size)), sg.Text('0', key='orin_status', size=data_size,  font=("Helvetica", font_size))],
                            [sg.Text('Orin IP Address: ', size=label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['orin_ip_address'], size=label_size, key='orin_ip_address',  font=("Helvetica", font_size))],
                            [sg.Button('Ping Orin', size=data_size, key='ping_orin', font=("Helvetica", font_size)) , sg.Button('Connect', size=data_size, key='connect_orin', font=("Helvetica", font_size))],
                        ], size=(640, 150)),
                        sg.Column([
                            [sg.Text('Arduino Configuration', size=label_size,  font=("Helvetica", font_size))],
                            [sg.Text('Arduino Serial Port: ', size=label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['arduino_serial_port'], size=label_size, key='arduino_serial_port',  font=("Helvetica", font_size))],
                            [sg.Text('Arduino Baudrate: ', size=label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['arduino_baudrate'], size=label_size, key='arduino_baudrate',  font=("Helvetica", font_size))],
                            [sg.Text('Arduino Timeout: ', size=label_size,  font=("Helvetica", font_size)), sg.InputText(self.config['arduino_timeout'], size=label_size, key='arduino_timeout',  font=("Helvetica", font_size))],
                            [sg.Button('Connect', size=data_size, key='connect_arduino', font=("Helvetica", font_size))],
                        ], size=(640, 150)),
                    ],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Battery 1', size=label_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery1', size=data_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery1', size=data_size,  font=("Helvetica", font_size)), sg.Text('V', size=data_size,  font=("Helvetica", font_size)), sg.Text('Battery 3', size=label_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery3', size=data_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery3', size=data_size,  font=("Helvetica", font_size)), sg.Text('V', size=data_size,  font=("Helvetica", font_size))],
                    [sg.Text('Battery 2', size=label_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery2', size=data_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery2', size=data_size,  font=("Helvetica", font_size)), sg.Text('V', size=data_size,  font=("Helvetica", font_size)), sg.Text('Battery 4', size=label_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery4', size=data_size,  font=("Helvetica", font_size)), sg.Text('0', key='battery4', size=data_size,  font=("Helvetica", font_size)), sg.Text('V', size=data_size,  font=("Helvetica", font_size))],
                ], size=(1280, 1080)),
                sg.Column([
                    [sg.Text('IMU Data', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Roll: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='imu_roll', size=data_size,  font=("Helvetica", font_size))],
                    [sg.Text('Pitch: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='imu_pitch', size=data_size,  font=("Helvetica", font_size))],
                    [sg.Text('Yaw: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='imu_yaw', size=data_size,  font=("Helvetica", font_size))],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Depth Data', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Depth: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='depth', size=data_size,  font=("Helvetica", font_size))],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Temperature Data', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Temperature: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='temperature', size=data_size,  font=("Helvetica", font_size))],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Humidity Data', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Humidity: ', size=data_label_size,  font=("Helvetica", font_size)), sg.Text('0', key='humidity', size=data_size,  font=("Helvetica", font_size))],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Motor Data', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Motor 1: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor1_progress')],
                    [sg.Text('Motor 2: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor2_progress')],
                    [sg.Text('Motor 3: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor3_progress')],
                    [sg.Text('Motor 4: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor4_progress')],
                    [sg.Text('Motor 5: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor5_progress')],
                    [sg.Text('Motor 6: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor6_progress')],
                    [sg.Text('Motor 7: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor7_progress')],
                    [sg.Text('Motor 8: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='motor8_progress')],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Servo Data', size=label_size,  font=("Helvetica", font_size))],
                    [sg.Text('Servo 1: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='servo1_progress')],
                    [sg.Text('Servo 2: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='servo2_progress')],
                    [sg.Text('Servo 3: ', size=data_label_size, font=("Helvetica", font_size)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='servo3_progress')],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Acoustics Data', size=label_size,  font=("Helvetica", font_size))]
                ], size=(320, 1080)),
                ],  
            ]
        except Exception as e:
            logging.error('Error loading the GUI: %s', e)
            sys.exit(1)

        # Create the window using the layout loaded
        self.window = sg.Window('Surface Station', layout, size=(1920, 1080), element_justification='c', finalize=True)
        
        # Run the GUI
        self.run()
        
    def ping_orin(self, host):
        # Ping parameters as function of OS
        parameters = "-n 1" if platform.system().lower()=="windows" else "-c 1"

        # Pinging
        try:
            output = subprocess.check_output("ping " + parameters + " " + host, shell=True)
            if "unreachable" in output.lower():
                return False
            else:
                return True
        except Exception:
            return False
    
    # Data format is as follows:
    # left_x,left_y,left_z,right_x,right_y,right_z,button1,button2,button3,button4,button5,button6,button7,button8, button9, button10
    def update_controller(self, data, controller):
        values = data.split(',')
        controller.left.x_axis = float(values[0])
        controller.left.y_axis = float(values[1])
        controller.left.z_axis = float(values[2])
        controller.right.x_axis = float(values[3])
        controller.right.y_axis = float(values[4])
        controller.right.z_axis = float(values[5])
        for i, val in enumerate(values[6:]):
            controller.buttons["button" + str(i + 1)] = val == 'True'
    
    def serial_thread(self):
        self.ser = serial.Serial(self.values['arduino_serial_port'], self.values['arduino_baud_rate'], timeout=self.values['arduino_timeout'])
        while True:
            data = self.ser.readline().decode('utf-8').rstrip()
            self.update_controller(data, self.controller)
    
    def parse_imu_data(self, data):
        pass
    
    def parse_acoustics_data(self, data):
        pass
    
    def update_gui(self, imu, acoustics):
        pass
    
    def recv_data(self):
        pass
    
    def start_sub(self):
        pass
    
    def emergency_stop(self):
        pass
    
    def run(self):
        self.event, self.values = self.window.read(timeout=100)
        while True:
            self.event, self.values = self.window.read(timeout=100)
            
            if self.ser is not None:
                pass

            
            
            if self.event == 'ping_orin':
                try:
                    status = self.ping_orin(self.values['orin_ip_address'])
                    self.window['orin_status'].update('1' if status else '0')
                    logging.info('Pinging ORIN: %s with Status: %s', self.values['orin_ip_address'], status)
                except Exception as e:
                    logging.error('Error pinging ORIN: %s', e)        
            elif self.event == sg.WIN_CLOSED:
                break
        

if __name__ == '__main__':
    ss = surfaceStation()