# import serial
# import time
# import sys
 
# # ser = serial.Serial('COM3', 9600, timeout = 1)
# try:
#     ser = serial.Serial('COM3', 9600, timeout = 1)
#     time.sleep(1)
# except:
#     print("Device can not be found or can not be configured.")
#     sys.exit(0)
 
# if (ser.readable()):
#     print(ser.readline().decode(), end ='') # 아두이노 준비 상태 확인.
#     # 아두이노에서 Serial.println("Arduino ready"); 명령으로 데이터를 보내기 때문에
#     # Serial 통신으로 읽어온 데이터에는 줄바꿈 문자(\r\n)가 이미 포함되어 있다.
#     # Serial.print("Arduino ready");으로 바꾸면 end = ''가 필요 없다. 
 
# while (True):
#     print("\n0: Off, 1: On, q(Q): Quit\nChoose: ", end = '')    
#     state = input()
 
#     if state == 'q' or state == 'Q':
#         break
#     elif state == '0':
#         ser.write(b'0')
#         print(ser.readline().decode(), end = '')
#     else:
#         ser.write(b'1')
#         print(ser.readline().decode(), end = '')
 
#     time.sleep(0.1)
 
# ser.close()

import keyboard
import serial
ser=serial.Serial('com3',9600)
while True:
    if keyboard.ispressed('w'):
        ser.write(b'f')
    elif keyboard.is_pressed("s"):
        ser.write(b'b')
    elif keyboard.is_pressed("d"):
        ser.write(b'r')
    elif keyboard.is_pressed("a"):
        ser.write(b'l')
    else:
        ser.write(b's')  