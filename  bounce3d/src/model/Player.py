from direct.showbase.ShowBase import ShowBase

from event.Event import Event, createNamedEvent

class Player:

  NAME_DEFAULT = "unnamed" 
  RIGHT_DEFAULT = False
  LEFT_DEFAULT = False

  def __init__(self, name = NAME_DEFAULT):
    self.name = name
    self.right = Player.RIGHT_DEFAULT
    self.left = Player.LEFT_DEFAULT

  def jumpOn(self):
    jumpEvent = createNamedEvent(self.name, Event.PLAYER_JUMP_ON)
    messenger.send(jumpEvent)

  def jumpOff(self):
    jumpEvent = createNamedEvent(self.name, Event.PLAYER_JUMP_OFF)
    messenger.send(jumpEvent)

  def moveRightOn(self):
    self.right= True
    moveEvent = createNamedEvent(self.name, Event.PLAYER_MOVE_RIGHT_ON)
    messenger.send(moveEvent)

  def moveRightOff(self):
    self.right = False
    moveEvent = createNamedEvent(self.name, Event.PLAYER_MOVE_RIGHT_OFF)
    messenger.send(moveEvent)

  def isRightOn(self):
    return self.right

  def moveLeftOn(self):
    self.left = True
    moveEvent = createNamedEvent(self.name, Event.PLAYER_MOVE_LEFT_ON)
    messenger.send(moveEvent)

  def moveLeftOff(self):
    self.left = False
    moveEvent = createNamedEvent(self.name, Event.PLAYER_MOVE_LEFT_OFF)
    messenger.send(moveEvent)

  def isLeftOn(self):
    return self.left
