# solution 1

# import spidev
# import time
# import os

# # open SPI bus
# spi = spidev.SpiDev()
# spi.open(0, 0)

# # Function to tead SPI data from MCP3008 chip
# # Channel must be an integer 0~7

# def readChannel(ch):
#     adc = spi.xfer2([1, (8 + ch)<<4, 0])
#     data = ((adc[1]&3) << 8) + adc[2]
#     return data

# # Define sensor channels
# # (channels 3 to 7 unused)
# swt_ch = 0
# vrx_ch = 1
# vry_ch = 2

# # Define delay between readings (s)
# delay = 0.5

# while True:
#     # Read the joystick position data
#     vrx_pos = readChannel(vrx_ch)
#     vry_pos = readChannel(vry_ch)

#     # Read switch state
#     swt_val = readChannel(swt_ch)

#     # Print out results
#     print("-------------------------------")
#     print("X : {} Y : {} Switch : {}".format(vrx_pos, vry_pos, swt_val))

#     # Wait before repeating loop
#     time.sleep(delay)


# solution 2
# using RPi.GPIO
import RPi.GPIO as IO


