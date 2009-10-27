
# keyboard
from direct.showbase.DirectObject import DirectObject

from GameModel import GameModel
from Event import Event, createNamedEvent

class KeyboardControl(DirectObject):
	''' @author J3lly '''

	PLAYER_RIGHT_KEY = "arrow_right"
	PLAYER_LEFT_KEY = "arrow_left"
	PLAYER_JUMP = "space"
	TURN_GRAVITY = "g"
	
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

		self.accept(KeyboardControl.PLAYER_RIGHT_KEY, player.moveRightOn)
		self.accept(KeyboardControl.PLAYER_RIGHT_KEY + "-up", player.moveRightOff)
		self.accept(KeyboardControl.PLAYER_LEFT_KEY, player.moveLeftOn)
		self.accept(KeyboardControl.PLAYER_LEFT_KEY + "-up", player.moveLeftOff)
		self.accept(KeyboardControl.PLAYER_JUMP, player.jumpOn)
		self.accept(KeyboardControl.PLAYER_JUMP + "-up", player.jumpOff)
		
		self.accept(KeyboardControl.TURN_GRAVITY, model.turnGravityTask )
		
		model.isListening = True
		
		
	 
