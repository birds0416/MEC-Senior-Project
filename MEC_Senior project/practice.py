import numpy as np
import cv2


cap = cv2.VideoCapture(0)
#kernel window for morphological operations

#begin capture
while(True):
    ret, frame = cap.read()

    #Smooth the frame
    # frame = cv2.GaussianBlur(frame,(11,11),0)
    
    #display the image
    cv2.imshow('frame',frame)
    #Mask image
    #Quit if user presses 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

#Release the capture
cap.release()
cv2.destroyAllWindows()