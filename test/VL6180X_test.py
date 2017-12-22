#!/usr/bin/python3

""" ST VL6180X ToF range finder program
 - power explorer board with 3.3 V
 - explorer board includes pull-ups on i2c """

import sys
from time import sleep

try:
    from ST_VL6180X import VL6180X
except ImportError:
    print("Error importing ST_VL6180X.VL6180X!")
    exit()

"""-- Setup --"""
debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":  # sys.argv[0] is the filename
        debug = True

# setup ToF ranging/ALS sensor
tof_address = 0x29
tof_sensor = VL6180X(address=tof_address, debug=debug)
# apply pre calibrated offset
tof_sensor.set_range_offset(23)
print("Range offset set to: {:d}".format(tof_sensor.get_range_offset()))
# setup ToF ranging/ALS sensor
tof_sensor.get_identification()
if tof_sensor.idModel != 0xB4:
    print("Not a valid sensor id: {:X}".format(tof_sensor.idModel))
else:
    print("Sensor model: {:X}".format(tof_sensor.idModel))
    print("Sensor model rev.: {:d}.{:d}"
          .format(tof_sensor.idModelRevMajor, tof_sensor.idModelRevMinor))
    print("Sensor module rev.: {:d}.{:d}"
          .format(tof_sensor.idModuleRevMajor, tof_sensor.idModuleRevMinor))
    print("Sensor date/time: {:X}/{:X}".format(tof_sensor.idDate, tof_sensor.idTime))
tof_sensor.default_settings()

sleep(1)

"""-- MAIN LOOP --"""
try:
    while True:
        print("Measured distance is : ", tof_sensor.get_distance(), " mm" )
        print("Measured light level is : ", tof_sensor.get_ambient_light(20), " lux")
        sleep(1)
except KeyboardInterrupt:
    print("\nquit")
