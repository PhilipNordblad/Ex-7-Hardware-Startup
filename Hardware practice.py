import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
spi = spidev.SpiDev()


s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)