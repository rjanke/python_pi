#! python3

import picamera
import time

with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    camera.start_preview()
    time.sleep(3)
    camera.capture('/home/pi/projects/python/plant_pods/camera_tests/image.jpg')
    camera.stop_preview()