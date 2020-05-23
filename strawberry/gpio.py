import RPi.GPIO as GPIO
import RPi

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # irc
#  GPIO.add_event_detect(25, GPIO.FALLING)
  GPIO.setup(7, GPIO.OUT) # motor A forward
  GPIO.setup(8, GPIO.OUT) # motor A backward
  GPIO.setup(9, GPIO.OUT) # motor B forward
  GPIO.setup(10, GPIO.OUT) # moto B backward


def destroy():
  GPIO.cleanup()
