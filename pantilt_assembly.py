import spidev
import time
import os
import numpy as np
import cv2
import pigpio

from numpy import interp
from gpiozero import Servo

''' Defaults from joystick.py '''
# servo pins
panServo = 23
tiltServo = 22

pan = Servo(panServo)
tilt = Servo(tiltServo)
pan.value = None
tilt.value = None

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

def ReadChannel(channel):
	adc = spi.xfer2([1, (8+channel) << 4, 0])
	data = ((adc[1] & 3) << 8) + adc[2]
	return data

# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0
vrx_channel = 1
vry_channel = 2

# Define delay between readings (s)
delay = 0.5

''' Defaults from color.py '''
# when running pigpio, type in command:
# sudo pigpiod
# python pantilt_color.py
# default servo position
initPos = 1500
panPos = 1500
tiltPos = 1500

servo = pigpio.pi()
servo.set_servo_pulsewidth(panServo, initPos)
servo.set_servo_pulsewidth(tiltServo, initPos)

minMov = 1
maxMov = 5

def movePanTilt(cenX, cenY):
    global panPos
    global tiltPos

    if int(cenX) > 360:
        panPos = int(panPos - interp(int(cenX), (360, 640), (minMov, maxMov)))
    elif int(cenX) < 280:
        panPos = int(panPos + interp(int(cenX), (280, 0), (minMov, maxMov)))

    if int(cenY) > 280:
        tiltPos = int(tiltPos - interp(int(cenY), (280, 480), (minMov, maxMov)))
    elif int(cenY) < 200:
        tiltPos = int(tiltPos + interp(int(cenY), (200, 0), (minMov, maxMov)))
    
    if int(cenX) <= 360 and int(cenX) >= 280:
        panPos = initPos
    if int(cenY) <= 280 and int(cenY) >= 200:
        tiltPos = initPos

    if not panPos > 2500 and panPos < 500:
        servo.set_servo_pulsewidth(panServo, panPos)
    if not tiltPos > 2500 and tiltPos < 500:
        servo.set_servo_pulsewidth(tiltServo, tiltPos)


#Capture from external USB webcam instead of the in-built webcam (shitty quality)
cap = cv2.VideoCapture(0)

#kernel window for morphological operations
kernel = np.ones((5,5),np.uint8)

#resize the capture window to 640 x 480
ret = cap.set(3,640)
ret = cap.set(4,480)

# stick memo color hsv code
lower_specific = np.array([9, 60, 80])
upper_specific = np.array([24, 255, 255]) 

# endless loop
swt_default = True
def swap_val(tmp, val):
    if val == 0:
        return not tmp
    else:
        return tmp

while True:
    ''' from joystick.py '''
    # Read the joystick position data
    vrx_pos = ReadChannel(vrx_channel)
    vry_pos = ReadChannel(vry_channel)

    # Read switch state
    swt_val = ReadChannel(swt_channel)
    swt_default = swap_val(swt_default, swt_val)

    # Print out results
    print("--------------------------------------")
    print("X : {} Y : {} Switch : {}".format(vrx_pos, vry_pos, swt_val))

    ''' from color.py '''
    ret, frame = cap.read()

    # Smooth the frame
    frame = cv2.GaussianBlur(frame, (11, 11), 0)

    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask to extract just the yellow pixels
    mask = cv2.inRange(hsv, lower_specific, upper_specific)

    # morphological opening
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    # morphological closing
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.erode(mask, kernel, iterations=2)

    # Detect contours from the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if swt_default == True:

        if (len(cnts) > 0):
            # Contour with greates area
            c = max(cnts, key=cv2.contourArea)

            # Radius and center pixel coordinate of the largest contour
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            movePanTilt(x, y)

            if radius > 5:
                # Drawing an enclosing circle
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

                # Draw a line from the center of the frame to the center of the contour
                cv2.line(frame, (320, 240), (int(x), int(y)), (0, 0, 255), 1)
                # Reference line
                cv2.line(frame, (320, 0), (320, 480), (0, 255, 0), 1)

                radius = int(radius)

                # Distance of the 'x' coordinate from the center of the frame
                # width of frame is 640, hence 320
                length = 320 - (int(x))
        
        else:
            servo.set_servo_pulsewidth(panServo, initPos)
            servo.set_servo_pulsewidth(tiltServo, initPos)

    elif swt_default == False:

        if vrx_pos >= 0 and vrx_pos < 512:
            print("pan: left")
            pan.value = 0.1
        elif vrx_pos >= 512 and vrx_pos < 540:
            print("pan: stop")
            pan.value = None
        elif vrx_pos > 600:
            print("pan: right")
            pan.value = -0.5

        if vry_pos >= 0 and vry_pos < 512:
            print("tilt: up")
            tilt.value = -0.5
        elif vry_pos >= 512 and vry_pos < 540:
            print("tilt: stop")
            tilt.value = None
        elif vry_pos > 600:
            print("tilt: right")
            tilt.value = 0.1
        
        # Wait before repeating loop
        time.sleep(delay)

    # Display the image
    cv2.imshow('frame', frame)
    
    # Quit if user presses 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        servo.set_servo_pulsewidth(panServo, 0)
        servo.set_servo_pulsewidth(tiltServo, 0)
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
