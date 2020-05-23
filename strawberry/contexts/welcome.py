from PIL import Image

def read(key, state):
  return None

def render(screen, state):
  loadedImage = Image.open('happycat_oled_64.ppm').convert('1')
  screen.image(loadedImage)

def name():
  return "Welcome"
