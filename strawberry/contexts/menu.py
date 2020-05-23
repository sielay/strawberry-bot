def render(options, cursor, screen):
  length = len(options)
  screen.clear()
  for i in range(length):
    fill = 255
    if i == cursor:
      screen.rect(0, i * 10, screen.getWidth(), 10, 255, 255)
      fill = 0
    screen.text(2, i * 10, options[i].label, fill)
  screen.render()

def prev(total, index):
  if (index == 0):
    return total - 1
  return index - 1

def next(total, index):
  if (index >= total - 1):
    return 0
  return index + 1

class Option:
  def __init__(self, id, label):
    self.id = id;
    self.label = label
