import RPi.GPIO as GPIO
import prop_control as control

ctrl = control.Control()

ctrl.move('stop')
GPIO.cleanup()
