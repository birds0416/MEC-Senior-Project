import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
servo1 = GPIO.PWM(23,50)

servo1.start(0)

servo1.ChangeDutyCycle(2)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)
time.sleep(0.5)
servo1.ChangeDutyCycle(2.5)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)
servo1.stop()
GPIO.cleanup()
