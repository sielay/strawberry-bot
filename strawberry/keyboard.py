# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals, print_function

import tty, termios
import time
import sys
if sys.version_info.major < 3:
  import thread as _thread
else:
  import _thread

char = None

def getch():   # define non-Windows version
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

def keypress():
  global char
  try:
    char = getch()
  except ValueError as err:
    print("Value error: {0}".format(err))
    pass
  except SystemExit as err:
    print("System exit: {0}".format(err))
    passs
  except:
    print("Unexpected error:", sys.exc_info()[0])
    pass

def setup():
  global char
  _thread.start_new_thread(keypress, ())
  while True:
    if char is not None:
      try:
        print("Key pressed is '{0}'".format(char))
      except UnicodeDecodeError:
        print("character can not be decoded, sorry!")
        char = None
      _thread.start_new_thread(keypress, ())
#      if char == 'q' or char == '\x1b':  # x1b is ESC
#        exit()
      char = None
      time.sleep(1)

def read():
  print("reading")
  global char
  if not char:
    return None
  print("Detected {0}".format(str(char)))
  key = char
  char = None
  return key
