import RPi.GPIO as GPIO

pin = 24

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # irc

def destroy():
  GPIO.cleanup()

def wait(pinNo, retry = 2):
  try:
    GPIO.wait_for_edge(pinNo, GPIO.FALLING)
  except RuntimeError as err:
    if (retry > 0):
      wait(pinNo, retry - 1)
      pass
    else:
      print("Runtime error: {0}".format(err))
      pass

setup()
wait(pin)
destroy()
