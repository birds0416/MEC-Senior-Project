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
maxMov = 1

servo = pigpio.pi()
servo.set_servo_pulsewidth(panServo, initPW)
servo.set_servo_pulsewidth(tiltServo, initPW)

def movePanTilt(cenX, cenY):
	global panPW
	global tiltPW
	
	if int(cenX) > 360:
		panPW = int(panPW - interp(int(cenX), (360, 640), (minMov, maxMov)))
	elif int(cenX) < 280:
		panPW = int(panPW + interp(int(cenX), (280, 0), (minMov, maxMov)))
		
	if int(cenY) > 280:
		tiltPW = int(tiltPW + interp(int(cenY), (280, 480), (minMov, maxMov)))
	elif int(cenY) < 200:
		tiltPW = int(tiltPW - interp(int(cenY), (200, 0), (minMov, maxMov)))
		
	if not panPW > 2500 and not panPW < 500:
	    servo.set_servo_pulsewidth(panServo, panPW)
		
	if not tiltPW > 2500 and not tiltPW < 500:
	    servo.set_servo_pulsewidth(tiltServo, tiltPW)

# horizontal moves
print("horizontal moves")
for i in range(0, 640):
	movePanTilt(i, 0)

time.sleep(3)

# center position
movePanTilt(320, 240)

time.sleep(1)

print("vertical moves")
# vertical move
for i in range(0, 480):
	movePanTilt(0, i)
	
time.sleep(3)

# center position
movePanTilt(320, 240)

time.sleep(1)

print("positive diagonal moves")
# positive diagonal movement
for x in range(0, 480):
	y = 0.75 * x
	movePanTilt(x, y)

time.sleep(3)
# center position
movePanTilt(320, 240)

time.sleep(1)

print("negative diagonal moves")
# negative diagonal movement
for x in range(480, 0, -1):
	y = -0.75 * x + 480
	movePanTilt(x, y)
	
servo.set_servo_pulsewidth(panServo, initPW)
servo.set_servo_pulsewidth(tiltServo, initPW)


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


