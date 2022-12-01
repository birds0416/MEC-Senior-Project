# 
# Reference from two github projects
# https://github.com/badrobot15/Color-Tracking-and-Following-using-OpenCV
# https://github.com/Practical-CV/Color-Based-Ball-Tracking-With-OpenCV
# 

from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import serial
import argparse
import imutils
import time

# For Arduino uno connection
# ser = serial.Serial("")

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

yellow_lower = np.array([0, 100, 100])
yellow_upper = np.array([30, 255, 255])

red_lower = np.array([0, 70, 50])
red_upper = np.array([10, 255, 255])

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	cap = VideoStream(src=0).start()

# otherwise, grab a reference to the video file
else:
	cap = cv2.VideoCapture(args["video"])

#kernel window for morphological operations
kernel = np.ones((5,5),np.uint8)

time.sleep(2.0)

while True:
    frame = cap.read()

    frame = frame[1] if args.get("video", False) else frame
    
    frame = imutils.resize(frame, width=640)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
 
    # Find contours of the object
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    try:
		biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
	except ValueError:
		biggest_contour = None
    x, y, w, h = cv2.boundingRect(biggest_contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # send information to arduino
    # length = 320 - int(x)
    # ser.write(str(length))
    # ser.write("#")
    # ser.write(str(radius))
    # ser.write("/")
 
    if len(cnts) > 0:
        # find the largest contour in the mask,
        # then use it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    
    pts.appendleft(center)
    
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore them
        if pts[i - 1] is None or pts[i] is None:
            continue
        
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    # press 'q' to exit the window
    if key == ord("q"):
        break

if not args.get("video", False):
    cap.stop()

else:
    cap.release()
    
cv2.destroyAllWindows()
    
        
