import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

font = cv.FONT_HERSHEY_SIMPLEX

face_cascade_file = "cascade/haarcascade_frontalface_alt.xml"
face_cascade = cv.CascadeClassifier(face_cascade_file)

cap = cv.VideoCapture(0)
while True:
    ret, cam = cap.read()

    if ret:
        cv.imshow('camera', cam)

        # press esc to close window
        if cv.waitKey(1) & 0xFF == 27:
            break

    gray = cv.cvtColor(cam, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.5, 3, minSize=(150, 150))

    for (x, y, w, h) in faces:
        mid_point = (x + w/2, y + h/2)
        
        cv.rectangle(cam, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.putText(cam, "Detected Face", (x - 5, y - 5), font, 0.5, (0, 0, 255), 2)


    cv.imshow("cam", cam)
    k = cv.waitKey(1)

cap.release()
cv.destroyAllWindows()





