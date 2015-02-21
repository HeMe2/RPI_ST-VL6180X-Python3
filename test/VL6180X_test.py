#!/usr/bin/python

""" ST VL6180X ToF range finder program
 - power explorer board with 3.3 V
 - explorer board includes pull-ups on i2c """

import sys
from ST_VL6180X import VL6180X
from time import sleep
import RPi.GPIO as GPIO  # Import GPIO functions

debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":  # sys.argv[0] is the filename
        debug = True

# setup ToF ranging/ALS sensor
tof_address = 0x29
tof_sensor = VL6180X(address=tof_address, debug=debug)
tof_sensor.get_identification()
if tof_sensor.idModel != 0xB4:
    print"Not a valid sensor id: %X" % tof_sensor.idModel
else:
    print"Sensor model: %X" % tof_sensor.idModel
    print"Sensor model rev.: %d.%d" % \
         (tof_sensor.idModelRevMajor, tof_sensor.idModelRevMinor)
    print"Sensor module rev.: %d.%d" % \
         (tof_sensor.idModuleRevMajor, tof_sensor.idModuleRevMinor)
    print"Sensor date/time: %X/%X" % (tof_sensor.idDate, tof_sensor.idTime)
tof_sensor.default_settings()

# Set output pin numbers for LEDS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use GPIO numbering scheme (not pin numbers)
LED = [17, 27]  # List of GPIOs to use for LED output

# Setup GPIOs and initial states
for i in range(len(LED)):
    GPIO.setup(LED[i], GPIO.OUT)  # Set all as output
    print("GPIO_%d is output" % LED[i])
    GPIO.output(LED[i], 0)  # Turn all LEDs off

sleep(1)


"""-- LED lighting function for debug --"""
def led_out(value):
    for i in range(len(LED)):
        GPIO.output(LED[i], value & (1 << i))  # Set LEDs based on value


"""-- MAIN LOOP --"""
while True:
    # write(0, 0x51)  # Set SRF to return distance in cm
    # sleep(0.1)
    # while range() == 0xFF:        # Wait for range finder to be ready
    #     pass                          # Do nothing
    # rng = (read_range() + read_range()) / 2

    # print "\rDistance is: %3.0f" % rng,
    # sys.stdout.flush()  # Flush output buffer to force print update

    # Set LED output based on range value
    # if rng >= 50:
    #     led_out(0x01)
    # elif rng >= 40:
    #     led_out(0x03)
    # elif rng >= 30:
    #     led_out(0x07)
    # elif rng >= 20:
    #     led_out(0x0F)
    # elif rng >= 10:
    #     led_out(0x1F)
    # else:
    #     led_out(0x3F)
    print "Measured distance is : %d mm" % tof_sensor.get_distance()
    print "Measured light level is : %d lux" % tof_sensor.get_ambient_light(20)
    sleep(1)
