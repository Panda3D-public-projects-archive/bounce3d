
# keyboard
from direct.showbase.DirectObject import DirectObject

from GameModel import GameModel

class KeyboardControl(DirectObject):
	''' @author J3lly '''
	
	def __init__(self, model):
	
		self.accept("arrow_left" , model.startMoveLeft)
		self.accept("arrow_left-up", model.stopMoveLeft)
		self.accept("arrow_right" , model.startMoveRight )
		self.accept("arrow_right-up", model.stopMoveRight)
		
		self.accept("space", model.turnGravityTask )
	 