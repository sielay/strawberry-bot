import RPi.GPIO as GPIO
from time import time

pinNo = 24

CODES = {
  # some old exmaples
  "0XFFA25D": "ON/OFF",
  "0XFF629D": "MODE",
  "0XFFE21D": "MUTE",
  "0XFF22DD": "PLAY/PAUSE",
  "0XFF02FD": "PREVIOUS",
  "0XFFC23D": "NEXT",
  "0XFFE01F": "EQ",
  "0XFFA857": "MINUS",
  "0XFF906F": "PLUS",
  "0XFF6897": "0",
  "0XFF9867": "SHUFFLE",
  "0XFFB04F": "U/SD",
  "0XFF30CF": "1",
  "0XFF18E7": "2",
  "0XFF7A85": "3",
  "0XFF10EF": "4",
  "0XFF38C7": "5",
  "0XFF5AA5": "6",
  "0XFF42Bd": "7",
  "0XFF4AB5": "8",
  "0XFF52AD": "9",
  # LG
  # https://gitlab.com/snippets/1690600
  "0X20DF10EF": "ON/OFF",
  "0X20DF0FF0": "TV/RAD",
  "0X20DFD02F": "INPUT",
  "0X20DFC23D": "SETTING",
  "0X20DFF50A": "LIVEZOOM",
  "0X20DF9C63": "SUBTITLE",
  "0X20DF8877": "1",
  "0X20DF48B7": "2",
  "0X20DFC837": "3",
  "0X20DF28D7": "4",
  "0X20DFA857": "5",
  "0X20DF6897": "6",
  "0X20DFE817": "7",
  "0X20DF18E7": "8",
  "0X20DF9867": "9",
  "0X20DF08F7": "0",
  "0X20DFCA35": "LIST",
  "0X20DFD52A": "GUIDE",
  "0X20DF40BF": "VOLUME/UP",
  "0X20DFC03F": "VOLUME/DOWN ",
  "0X20DF55AA": "INFO",
  "0X20DF1EE1": "SEARCH",
  "0X20DF906F": "MUTE",
  "0X20DF00FF": "PAGE/NEXT",
  "0X20DF807F": "PAGE/PREV",
  "0X20DFAD52": "RECENT",
  "0X20DF3EC1": "HOME",
  "0X20DF7986": "MENU",
  "0X20DF14EB": "BACK",
  "0X20DFDA25": "EXIT",
  "0X20DF02FD": "UP",
  "0X20DF827D": "DOWN",
  "0X20DF609F": "RIGHT",
  "0X20DFE01F": "LEFT",
  "0X20DF22DD": "OK",
  "0X20DF04FB": "TELETEXT",
  "0X20DF847B": "TELETEXT/OPTIONS",
  "0X20DF8976": "AD",
  "0X20DFBD42": "REC/*",
  "0X20DF8D72": "STOP",
  "0X20DF0DF2": "PLAY",
  "0X20DF5DA2": "PAUSE",
  "0X20DFF10E": "REW",
  "0X20DF718E": "FORWARD",
  "0X20DF4EB1": "RED",
  "0X20DF8E71": "GREEN",
  "0X20DFC639": "YELLOW",
  "0X20DF8679": "BLUE",

# Below are buttons not present on the actual remote, if they are uncommented they actually work on 55UH605V
  "0X20DFA35C": "OFF",
  "0X20DF23DC": "ON",
  "0X20DFA956": "ENERGY",
  "0X20DF58A7": "QUICKVIEW",
  "0X20DF7887": "FAV",
  "0X20DF9E61": "EZ/RATIO",
  "0X20DFB24D": "EZ/PICTURE",
  "0X20DF708F": "EZ/CLEEP",
  "0X20DF3BC4": "3D", # Will just say 3D mode is unsupported on my TV
  "0X20DFFF00": "EZ/ADJUST", # Password is 0413
  "0X20DFDF20": "IN/START", # Password is 0413 # Here you can turn off the retarded dimming
  "0X20DF6B94": "INPUT/ANTENNA",
  "0X20DFFD02": "INPUT/COMPOENT1",
  "0X20DF0CF3": "INPUT/AV1", # Looks like an old code - moved to a different code on new TVs?
  "0X20DF5AA5": "INPUT/AV",
  "0X20DF738C": "INPUT/HDMI1",
  "0X20DF33CC": "INPUT/HDMI2",
  "0X20DF9768": "INPUT.HDMI3",
  "0X20DF5BA4": "INPUT/HDMI4", # TV doesn't have HDMI4
  "0X20DF09F6": "RECORD/LIST",
  "0X20DF50AF": "AUDIO",
  "0X20DF7E81": "SIMPLINK",
  "0X20DF956A": "TV/GUIDE",
  "0X20DF5EA1": "USER/GUIDE",
  "0X20DFF00F": "TV/RADIO",
  "0X20DF6A95": "NETFLIX", # webOS 4.x, replaces 'recent' button
  "0X20DF3AC5": "AMAZON", # webOS 4.x, replaces 'live menu' button
}

def binary_aquire(pinNo, duration):
    # aquires data as quickly as possible
    t0 = time()
    results = []
    while (time() - t0) < duration:
        results.append(GPIO.input(pinNo))
    return results


def on_ir_receive(pinNo, bouncetime=150):
    # when edge detect is called (which requires less CPU than constant
    # data acquisition), we acquire data as quickly as possible
    data = binary_aquire(pinNo, bouncetime/1000.0)
    if len(data) < bouncetime:
        return
    rate = len(data) / (bouncetime / 1000.0)
    pulses = []
    i_break = 0
    # detect run lengths using the acquisition rate to turn the times in to microseconds
    for i in range(1, len(data)):
        if (data[i] != data[i-1]) or (i == len(data)-1):
            pulses.append((data[i-1], int((i-i_break)/rate*1e6)))
            i_break = i
    # decode ( < 1 ms "1" pulse is a 1, > 1 ms "1" pulse is a 1, longer than 2 ms pulse is something else)
    # does not decode channel, which may be a piece of the information after the long 1 pulse in the middle
    outbin = ""
    for val, us in pulses:
        if val != 1:
            continue
        if outbin and us > 2000:
            break
        elif us < 1000:
            outbin += "0"
        elif 1000 < us < 2000:
            outbin += "1"
    try:
        return int(outbin, 2)
    except ValueError:
        # probably an empty code
        return None

#def waitForEdge(pinNo, retry = 2):
#  try:
#    GPIO.wait_for_edge(pinNo, GPIO.FALLING)
#  except RuntimeError as err:
#    if (retry > 0):
#      waitForEdge(pinNo, retry)
#      pass
#    else:
#      print("Runtime error: {0}".format(err))
#      pass

def getLastKey():
  code = None
#  if GPIO.event_detected(pinNo):
  code = on_ir_receive(pinNo)
  if code:
    value = str(hex(code)).upper()
    try:
      key = CODES.get(value)
      if key:
        return key
      print("Unknown key {0}".format(value))
      return None
    except KeyError as err:
      print("Name error: {0}".format(err))
      return value
      pass
    except NameError as err:
      print("Name error: {0}".format(err))
      return value
      pass
    except AttributeError as err:
      print("Name error: {0}".format(err))
      return value
      pass
  else:
   return None
