import sockets
import asyncio
import cv2
import logging


# create a camera class
class Camera:
    def __init__(self, cam):
        self.cam = cv2.VideoCapture(cam)

        # attempt to open the camera
        try: 
            test = self.cam.read()
        except Exception as e:
            print(f'Error has occured, check log file for complete error')
            return e
        
    def update(self):
        return self.cam.read()
    
