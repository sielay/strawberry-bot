import contexts.menu as menu

options = []
options.append(menu.Option("drive", "Toggle drive"))
options.append(menu.Option("welcome", "Welcome screen"))

def init():
  return {
    "option": 0
  }

def read(key, instance):
  state = instance.getState()
  option = state.get("option", 0)
  newOption = option
  if key == "UP":
    newOption = menu.prev(len(options), state.option)
  elif key == "DOWN":
    newOption = menu.next(len(options), state.option)
  if not option == newOption:
    state.update(option=newOption)
    instance.setState(state)
  return None

def render(screen, instance):
  state = instance.getState()
  menu.render(options, state.get("option", 0), screen)

def name():
  return "Main menu"
