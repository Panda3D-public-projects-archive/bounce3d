
# keyboard
from direct.showbase.DirectObject import DirectObject

from GameModel import GameModel
from Event import Event, createNamedEvent

class KeyboardControl(DirectObject):
	''' @author J3lly '''

	PLAYER_RIGHT_KEY = "arrow_right"
	PLAYER_LEFT_KEY = "arrow_left"
	PLAYER_UP_KEY = "arrow_up"
	PLAYER_DOWN_KEY = "arrow_down"
	PLAYER_JUMP = "space"
	TURN_GRAVITY = "g"
	TURN_GRAVITY2 = "h"

	def __init__(self, model):
		player = model.getPlayer()
		ball = model.getBall()
		
		playerMoveRightOn = createNamedEvent(
			player.name, Event.PLAYER_MOVE_RIGHT_ON
		)
		playerMoveRightOff = createNamedEvent(
			player.name, Event.PLAYER_MOVE_RIGHT_OFF
		)
		playerMoveLeftOn = createNamedEvent(
			player.name, Event.PLAYER_MOVE_LEFT_ON
		)
		playerMoveLeftOff = createNamedEvent(
			player.name, Event.PLAYER_MOVE_LEFT_OFF
		)
		playerJumpOn = createNamedEvent(
			player.name, Event.PLAYER_JUMP_ON
		)
		playerJumpOff = createNamedEvent(
			player.name, Event.PLAYER_JUMP_OFF
		)

		self.accept(playerMoveRightOn, ball.startMoveRight)
		self.accept(playerMoveRightOff, ball.stopMoveRight)		
		self.accept(playerMoveLeftOn, ball.startMoveLeft)
		self.accept(playerMoveLeftOff, ball.stopMoveLeft)
		self.accept(playerJumpOn, ball.jumpOn) 	
		self.accept(playerJumpOff, ball.jumpOff)

		self.accept(KeyboardControl.PLAYER_RIGHT_KEY, ball.arrowRightDown)
		self.accept(KeyboardControl.PLAYER_RIGHT_KEY + "-up", ball.arrowRightUp)
		self.accept(KeyboardControl.PLAYER_LEFT_KEY, ball.arrowLeftDown)
		self.accept(KeyboardControl.PLAYER_LEFT_KEY + "-up", ball.arrowLeftUp)
		self.accept(KeyboardControl.PLAYER_UP_KEY, ball.arrowUpDown)
		self.accept(KeyboardControl.PLAYER_UP_KEY + "-up", ball.arrowUpUp)
		self.accept(KeyboardControl.PLAYER_DOWN_KEY, ball.arrowDownDown)
		self.accept(KeyboardControl.PLAYER_DOWN_KEY + "-up", ball.arrowDownUp)
		self.accept(KeyboardControl.PLAYER_JUMP, player.jumpOn)
		self.accept(KeyboardControl.PLAYER_JUMP + "-up", player.jumpOff)
		
		self.accept(KeyboardControl.TURN_GRAVITY, model.turnGravityTask )
		self.accept(KeyboardControl.TURN_GRAVITY2, model.turnGravityTask2 )
		
		model.isListening = True
		
		
	 
