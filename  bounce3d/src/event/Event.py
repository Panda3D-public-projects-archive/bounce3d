class Event:

  PLAYER_MOVE_RIGHT_ON = "Player Move Right On"
  PLAYER_MOVE_RIGHT_OFF = "Player Move Right Off"
  PLAYER_MOVE_LEFT_ON = "Player Move Left On"
  PLAYER_MOVE_LEFT_OFF = "Player Move Left Off"
  PLAYER_JUMP_ON = "Player Jump On"
  PLAYER_JUMP_OFF = "Player Jump Off"

def createNamedEvent(name, event):
  return name + " " + event
