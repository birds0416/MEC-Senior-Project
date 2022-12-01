from collections import deque
from imutils.video import VideoStream
from numpy import interp
import numpy as np
import argparse
import imutils
import time
import numpy as np
import cv2
import serial
import pigpio

# when running pigpio, type in command:
# sudo pigpiod
# python pantilt_color_tracking_final.py

panServo = 25
tiltServo = 9

panPos = 0
tiltPos = 0

servo = pigpio.pi()
servo.set_servo_pulsewidth(panServo, panPos)
servo.set_servo_pulsewidth(tiltServo, tiltPos)

minMov = 30
maxMov = 100

def movePanTilt(x, y, w, h):
	global panPos
	global tiltPos
	
	if int(x+(w/2)) > 360:
		panPos = int(panPos - interp(int(x+(w/2)), (360, 640), (minMov, maxMov)))
	elif int(x+(w/2)) < 280:
		panPos = int(panPos + interp(int(x+(w/2)), (280, 0), (minMov, maxMov)))
	
	if int(y+(h/2)) > 280:
		tiltPos = int(tiltPos + interp(int(y+(h/2)), (280, 480), (minMov, maxMov)))
	elif int(y+(h/2)) < 200:
		tiltPos = int(tiltPos - interp(int(y+(h/2)), (200, 0), (minMov, maxMov)))
	
	if not panPos > 2500 and not panPos < 500:
		servo.set_servo_pulsewidth(panServo, panPos)
		
	if not tiltPos > 2500 and not tiltPos < 500:
		servo.set_servo_pulsewidth(tiltServo, tiltPos)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
              'white': [[180, 18, 255], [0, 0, 231]],
              'red1': [[180, 255, 255], [159, 50, 70]],
              'red2': [[9, 255, 255], [0, 50, 70]],
              'green': [[89, 255, 255], [36, 50, 70]],
              'blue': [[128, 255, 255], [90, 50, 70]],
              'yellow': [[35, 255, 255], [25, 50, 70]],
              'purple': [[158, 255, 255], [129, 50, 70]],
              'orange': [[24, 255, 255], [10, 50, 70]],
              'gray': [[180, 18, 230], [0, 0, 40]]}

greenLower = (36, 50, 70)
greenUpper = (89, 255, 255)

yellow_lower = (25, 50, 70)
yellow_upper = (35, 255, 255)

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()

# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
	# grab the current frame
	frame = vs.read()

	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
 
	# mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None

	contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]

	try:
		biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
	except ValueError:
		servo.set_servo_pulsewidth(panServo, 0)
		servo.set_servo_pulsewidth(tiltServo, 0)
		
	x, y, w, h = cv2.boundingRect(biggest_contour)
	cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	movePanTilt(x, y, w, h)

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

	# update the points queue
	pts.appendleft(center)

	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the frame to our screen
	cv2.imshow("frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		servo.set_servo_pulsewidth(panServo, 0)
		servo.set_servo_pulsewidth(tiltServo, 0)
		break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()

# otherwise, release the camera
else:
	vs.release()

# close all windows
cv2.destroyAllWindows()
