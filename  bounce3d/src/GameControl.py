
# keyboard
from direct.showbase.DirectObject import DirectObject

from model.GameModel import GameModel

from event.Event import createNamedEvent
from event.EventType import EventType

class GameControl(DirectObject):
	'''
	Currently the game can be controlled with a keaboard.
	http://www.panda3d.org/wiki/index.php/Event_Handlers
	'''

	PLAYER_RIGHT_KEY = "arrow_right"
	PLAYER_LEFT_KEY = "arrow_left"
	PLAYER_UP_KEY = "arrow_up"
	PLAYER_DOWN_KEY = "arrow_down"
	PLAYER_JUMP = "space"
	TURN_GRAVITY = "g"
	TURN_GRAVITY2 = "h"
	RESTART_LEVEL = "r"
	SELECT = "enter"

	def __init__(self, model, app):
		player = model.getPlayer()
		self.ball = ball = model.getBall()
		self.app = app
		self.inMenu = False
		
		playerMoveRightOn = createNamedEvent(
			player.name, EventType.PLAYER_MOVE_RIGHT_ON
		)
		playerMoveRightOff = createNamedEvent(
			player.name, EventType.PLAYER_MOVE_RIGHT_OFF
		)
		playerMoveLeftOn = createNamedEvent(
			player.name, EventType.PLAYER_MOVE_LEFT_ON
		)
		playerMoveLeftOff = createNamedEvent(
			player.name, EventType.PLAYER_MOVE_LEFT_OFF
		)
		playerJumpOn = createNamedEvent(
			player.name, EventType.PLAYER_JUMP_ON
		)
		playerJumpOff = createNamedEvent(
			player.name, EventType.PLAYER_JUMP_OFF
		)

		self.accept(playerMoveRightOn, ball.startMoveRight)
		self.accept(playerMoveRightOff, ball.stopMoveRight)
		self.accept(playerMoveLeftOn, ball.startMoveLeft)
		self.accept(playerMoveLeftOff, ball.stopMoveLeft)
		self.accept(playerJumpOn, ball.jumpOn)
		self.accept(playerJumpOff, ball.jumpOff)

		self.accept(GameControl.PLAYER_RIGHT_KEY, ball.arrowRightDown)
		self.accept(GameControl.PLAYER_RIGHT_KEY + "-up", ball.arrowRightUp)
		self.accept(GameControl.PLAYER_LEFT_KEY, ball.arrowLeftDown)
		self.accept(GameControl.PLAYER_LEFT_KEY + "-up", ball.arrowLeftUp)
		
		self.accept(EventType.CONTROL_CHANGE, self.controlLocation)
		
		self.accept(GameControl.PLAYER_UP_KEY, ball.arrowUpDown)
		self.accept(GameControl.PLAYER_UP_KEY + "-up", ball.arrowUpUp)
		self.accept(GameControl.PLAYER_DOWN_KEY, ball.arrowDownDown)
		self.accept(GameControl.PLAYER_DOWN_KEY + "-up", ball.arrowDownUp)
		
		self.accept(GameControl.PLAYER_JUMP, player.jumpOn)
		self.accept(GameControl.PLAYER_JUMP + "-up", player.jumpOff)
		
		self.accept(GameControl.TURN_GRAVITY, model.turnGravityTask )
		self.accept(GameControl.TURN_GRAVITY2, model.turnGravityTask2 )
		
		model.isListening = True
	
	def controlChange(self):
		self.activeMenu = self.app.getActiveMenu()
		if self.inMenu:
			self.accept(GameControl.PLAYER_UP_KEY + "-up", self.activeMenu.selectionUp)
			self.accept(GameControl.PLAYER_DOWN_KEY + "-up", self.activeMenu.selectionDown)
			self.accept(GameControl.SELECT + "-up", self.activeMenu.selection)
		else:
			self.accept(GameControl.PLAYER_UP_KEY + "-up", self.ball.arrowUpUp)
			self.accept(GameControl.PLAYER_DOWN_KEY + "-up", self.ball.arrowDownUp)
			self.accept(GameControl.SELECT + "-up",self.unbind )
	
	def controlLocation(self):
		self.inMenu = not self.inMenu
		self.controlChange()
		
	def unbind(self):
		print "Key unbinded"