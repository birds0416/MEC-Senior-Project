import spidev
import time
import os

from gpiozero import Servo

# servo pins
panServo = 23
tiltServo = 22

pan = Servo(panServo)
tilt = Servo(tiltServo)
pan.value = None
tilt.value = None

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
	adc = spi.xfer2([1, (8+channel) << 4, 0])
	data = ((adc[1] & 3) << 8) + adc[2]
	return data

# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0
vrx_channel = 1
vry_channel = 2

# Define delay between readings (s)
delay = 0.5

# endless loop
while True:
	# Read the joystick position data
	vrx_pos = ReadChannel(vrx_channel)
	vry_pos = ReadChannel(vry_channel)
	
	# Read switch state
	swt_val = ReadChannel(swt_channel)
	
	# Print out results
	print("--------------------------------------")
	print("X : {} Y : {} Switch : {}".format(vrx_pos, vry_pos, swt_val))
	
	if vrx_pos >= 0 and vrx_pos < 512:
		print("pan: left")
		pan.value = 0.1
	elif vrx_pos >= 512 and vrx_pos < 540:
		print("pan: stop")
		pan.value = None 
	elif vrx_pos > 680:
		print("pan: right")
		pan.value = -0.5
		
	if vry_pos >= 0 and vry_pos < 512:
		print("tilt: up")
		tilt.value = -0.5
	elif vry_pos >= 512 and vry_pos < 540:
		print("tilt: stop")
		tilt.value = None
	elif vry_pos > 680:
		print("tilt: down")
		tilt.value = 0.1
	
	
	# Wait before repeating loop
	# time.sleep(delay)
	
	
	
	


