import screen
import contexts.welcome as welcome
import contexts.main as main

drive = False

class Context:
  def __init__(self, context):
    self._context = context
    if "init" in dir(context):
      self._state = context.init()
    else:
      self._state = None
  def name(self):
    return self._context.name()
  def render(self):
    return self._context.render(screen, self)
  def read(self, key):
    if not self._context.read(key, self):
      globalActions(key)
  def getState(self):
    return self._state;
  def setState(self, state):
    self._state = state;

current = Context(main)

def getCurrent():
  global current
  return current

def globalActions(key):
  global current
  global drive
  if key == "HOME":
    current = Context(main)
  elif key == "GREEN":
    setDrive(True)
  elif key == "YELLOW":
    setDrive(False)

def setDrive(value):
  global drive
  print("Setting drive to {0}".format(value))
  drive = value

def getDrive():
  global drive
  return drive

