# 
# Reference from three github projects & one Arduino project
# https://github.com/jtmorris/Two-Axis-Camera-Tracking
# https://github.com/badrobot15/Color-Tracking-and-Following-using-OpenCV
# https://github.com/Practical-CV/Color-Based-Ball-Tracking-With-OpenCV
# https://create.arduino.cc/projecthub/shubhamsantosh99/face-tracker-using-opencv-and-arduino-55412e
# 

from imutils.video import WebcamVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import cv2
import imutils
import time
import serial
from motor_movement import Serial_Motor_Control

# Serial object for communication with Arduino
ser = serial.Serial('COM3', 9600)

def forward():
    print("CTRL -> FORWARD -> ON")
    ser.write(b'FY')

def reverse():
    print("CTRL -> REVERSE -> ON")
    ser.write(b'RY')

def quit():
    print("\n** END OF PROGRAM")
    ser.write(b'Q')

cap = cv2.VideoCapture(0)
kernel = np.ones((5, 5), np.uint8)

ret = cap.set(3, 640)
ret = cap.set(4, 480)

lower_red = np.array([-10, 100, 100])
upper_red = np.array([10, 255, 255])

# begin capture
while(True):
    ret, frame = cap.read()
    
    #Smooth the frame
    frame = cv2.GaussianBlur(frame,(11,11),0)

    #Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Mask to extract just the yellow pixels
    # mask = cv2.inRange(hsv,lower_yellow,upper_yellow)
    #Mask to extract just the red pixels
    mask = cv2.inRange(hsv,lower_red,upper_red)

    #morphological opening
    mask = cv2.erode(mask,kernel,iterations=2)
    mask = cv2.dilate(mask,kernel,iterations=2)

    #morphological closing
    mask = cv2.dilate(mask,kernel,iterations=2)
    mask = cv2.erode(mask,kernel,iterations=2)

    #Detect contours from the object
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    if(len(cnts) > 0)    :
        c = max(cnts, key = cv2.contourArea)
        # print(c)
        # Draw rectangle
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        FY = 'FY'
        RY = 'RY'
        Q = 'Q'
        
        # Position adjust of pitch axis
        if y > 240:
            print("CTRL -> FORWARD -> ON")
            ser.write(FY.encode())
            print("serial sent")
        elif y < 240:
            print("CTRL -> REVERSE -> ON")
            ser.write(RY.encode())
            print("serial sent")
        elif y == 240:
            print("\n** END OF PROGRAM")
            ser.write(Q.encode())
            print("serial sent")
            
        if ser.readable():
            response = ser.readline()
            print(response[:len(response) - 1].decode())
            
        
        
        # Draw a line from the center of the frame to the center of the contour
        cv2.line(frame,(320,240),(x + w, y + h),(0, 0, 255), 1)
    
    cv2.rectangle(frame, (320-25, 240+25), (320+25, 240-25), (255, 255, 255), 2)
    
    # display image
    cv2.imshow('frame', frame)
    # mask image
    cv2.imshow('mask', mask)
    # quit if user presses 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    
# release capture
cap.release()
cv2.destroyAllWindows()