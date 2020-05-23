import gpio
import irc
import motor
import sys
import context
#import keyboard

def run():
  try:
    gpio.setup()
#    keyboard.setup()
    print("Starting the loop")
    while True:
      print("1")
      key = irc.getLastKey()
#      if not key:
#        key = keyboard.read()
      current = context.getCurrent()
      current.read(key)
      if context.getDrive():
        motor.read(key)
      else:
        motor.read(None)
      current.render()
      if key:
        print(key)
  except KeyboardInterrupt:
    pass
  except AttributeError as err:
    print("Attribute error: {0}".format(err))
  except RuntimeError as err:
    print("Runtime error: {0}".format(err))
  except NameError as err:
    print("Name error: {0}".format(err))
  except TypeError as err:
    print("Type error: {0}".format(err))
  except:
    print("Unexpected error:", sys.exc_info()[0])
    pass
  gpio.destroy()

if __name__ == "__main__":
  run()
