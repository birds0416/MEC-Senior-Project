import numpy as np
import time
import cv2

import pigpio
from numpy import interp

# when running pigpio, type in command:
# sudo pigpiod
# python pantilt_color.py

panServo = 23
tiltServo = 22

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
		tiltPos = int(tiltPos + interp(int(cenY), (280, 480), (minMov, maxMov)))
	elif int(cenY) < 200:
		tiltPos = int(tiltPos - interp(int(cenY), (200, 0), (minMov, maxMov)))
		
	if int(cenX) <= 360 and int(cenX) >= 280:
            panPos = initPos
	if int(cenY) <= 280 and int(cenY) >= 200:
            tiltPos = initPos
		
	if not panPos > 2500 and not panPos < 500:
	    servo.set_servo_pulsewidth(panServo, panPos)
		
	if not tiltPos > 2500 and not tiltPos < 500:
	    servo.set_servo_pulsewidth(tiltServo, tiltPos)

#Capture from external USB webcam instead of the in-built webcam (shitty quality)
cap = cv2.VideoCapture(0)

#kernel window for morphological operations
kernel = np.ones((5,5),np.uint8)

#resize the capture window to 640 x 480
ret = cap.set(3,640)
ret = cap.set(4,480)

#upper and lower limits for the color yellow in HSV color space
# lower_yellow = np.array([25, 50, 70])
# upper_yellow = np.array([35,255,255])

# lower_red = np.array([0, 50, 70])
# upper_red = np.array([9, 255, 255])

# lower_gray = np.array([0, 0, 40])
# upper_gray = np.array([180, 18, 230])

# lower_blue = np.array([90, 50, 70])
# upper_blue = np.array([128, 255, 255])

# lower_orange = np.array([10, 50, 70])
# upper_orange = np.array([24, 255, 255])

# lower_black = np.array([0, 0, 0])
# upper_black = np.array([360, 255, 50])

lower_specific = np.array([9, 60, 80])
upper_specific = np.array([24, 255, 255]) 

#begin capture
while(True):
    ret, frame = cap.read()

    #Smooth the frame
    frame = cv2.GaussianBlur(frame,(11,11),0)

    #Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Mask to extract just the yellow pixels
    # mask = cv2.inRange(hsv,lower_yellow,upper_yellow)
    #Mask to extract just the red pixels
    mask = cv2.inRange(hsv,lower_specific, upper_specific)

    #morphological opening
    mask = cv2.erode(mask,kernel,iterations=2)
    mask = cv2.dilate(mask,kernel,iterations=2)

    #morphological closing
    mask = cv2.dilate(mask,kernel,iterations=2)
    mask = cv2.erode(mask,kernel,iterations=2)

    #Detect contours from the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if(len(cnts) > 0):
        #Contour with greatest area
        c = max(cnts,key=cv2.contourArea)
        #Radius and center pixel coordinate of the largest contour
        ((x,y),radius) = cv2.minEnclosingCircle(c)
	
        movePanTilt(x, y)

        if radius > 5:
            #Draw an enclosing circle
            cv2.circle(frame,(int(x), int(y)), int(radius),(0, 255, 255), 2)

            #Draw a line from the center of the frame to the center of the contour
            cv2.line(frame,(320,240),(int(x), int(y)),(0, 0, 255), 1)
            #Reference line
            cv2.line(frame,(320,0),(320,480),(0,255,0),1)

            radius = int(radius)

            #distance of the 'x' coordinate from the center of the frame
            #wdith of frame is 640, hence 320
            length = 320-(int(x))

    else:
        servo.set_servo_pulsewidth(panServo, initPos)
        servo.set_servo_pulsewidth(tiltServo, initPos)

    #display the image
    cv2.imshow('frame',frame)
    #Mask image
    #cv2.imshow('mask',mask)
    #Quit if user presses 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        servo.set_servo_pulsewidth(panServo, 0)
        servo.set_servo_pulsewidth(tiltServo, 0)
        break

#Release the capture
cap.release()
cv2.destroyAllWindows()

