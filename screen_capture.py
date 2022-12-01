import cv2
import threading

command = None

def process():
    while True:
        command = input('Enter command')

thread = threading.Thread(target=process)
thread.start()

cap = cv2.VideoCapture(0)
reqCommand = 'Capture_pic'
while(True):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    cv2.imshow('frame', rgb)
    if command == reqCommand:
        out = cv2.imwrite('capture.jpg', frame)
        thread.terminate()
        break

cap.release()
cv2.destroyAllWindows()
