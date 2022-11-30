import pigpio
import time
from numpy import interp

# import RPi.GPIO as GPIO

# from gpiozero import Servo
# from gpiozero import AngularServo

# the time ON(1) is remaining = duty cycle in ms
# duty cycle + OFF = pulse_width
# servo motor specs: 4.8V - 0.17sec / 60 degrees

panServo = 23
tiltServo = 22
half_rev_DC = 510

# default servo position
panPW = 1500
tiltPW = 1500
initPW = 1500

minMov = 1
maxMov = 5

servo = pigpio.pi()
servo.set_servo_pulsewidth(panServo, initPW)
servo.set_servo_pulsewidth(tiltServo, initPW)

def movePanTilt(cenX, cenY):
	global panPW
	global tiltPW
	
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

# horizontal moves
for i in range(0, 640):
    movePanTilt(i, 240)

# center position
movePanTilt(320, 240)

# vertical move
for i in range(0, 480):
    movePanTilt(320, i)

movePanTilt(320, 240)

# positive diagonal movement
for x in range(0, 640):
    y = 0.75 * x
    movePanTilt(x, y)

# negative diagonal movement
for x in range(640, -1, -1):
    y = -0.75 * x + 480
    movePanTilt(x, y)

# # <RPi.GPIO>
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(panServo, GPIO.OUT)

# 50 means 50Hz, and start servo with 0 duty cycle so it doesn't set any angles on start up
# pwm_pan = GPIO.PWM(panServo, 50)
# pwm_pan.start(0)

# def setAngle(angle, servo_num, servo_pwm):
# 	duty = angle / 50
#	GPIO.output(servo_num, True)
#	servo_pwm.ChangeDutyCycle(duty)
#	time.sleep(1)
	
#	GPIO.output(servo_num, False)
#	servo_pwm.ChangeDutyCycle(0)

# setAngle(80, panServo, pwm_pan)
# pwm_pan.stop()
# GPIO.cleanup()

# # <gpiozero>
# pan = Servo(panServo, min_pulse_width=minPW, max_pulse_width=maxPW)
# pan = AngularServo(panServo, min_pulse_width=0.0006, max_pulse_width=0.0023)

# servo.value < 0 - cw	(rotate right)
# servo.value > 0 - ccw	(rotate left)
# servo.value = 0 - stop

# one iteration of for loop is about 54 degrees
# two iterations of for looop is approximately 180 degrees


