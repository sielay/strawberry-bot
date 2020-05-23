import RPi.GPIO as GPIO  # Import the GPIO Library
import time  # Import the Time library

step = 0.2

ForwardA = 7
ForwardB = 9
BackwardA = 8
BackwardB = 10

def tick(A, B):
  GPIO.output(A, 1)
  GPIO.output(B, 1)
#  time.sleep(0.2)
#  GPIO.output(A, 0)
#  GPIO.output(B, 0)

def forward():
  tick(ForwardA, ForwardB)

def reverse():
  tick(BackwardA, BackwardB)

def right():
  tick(BackwardA, ForwardB)

def left():
  tick(ForwardA, BackwardB)

def reset():
  GPIO.output(ForwardA, 0)
  GPIO.output(ForwardB, 0)
  GPIO.output(BackwardA, 0)
  GPIO.output(BackwardB, 0)

def read(key):
  if key == "UP":
    forward()
  elif key == "DOWN":
    reverse()
  elif key == "LEFT":
    left()
  elif key == "RIGHT":
    right()
  else:
    reset()
