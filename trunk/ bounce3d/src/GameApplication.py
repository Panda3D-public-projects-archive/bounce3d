
# taskMgr
# messenger
from direct.showbase.ShowBase import ShowBase 

from GameControl import GameControl
from GameLoop import GameLoop

from model.GameModel import GameModel
from view.Hud import Hud
from view.GameView import GameView

from event.EventType import EventType

class GameApplication:
	
	SIM_TASK = "Physics Simulation"
	
	def __init__(self):
		self.base = ShowBase()
		self.model = self.loop = self.keys = None
		self.mapNo = 0 #default
		self.hud = Hud()
		self.view = GameView( self.base )
		
		# http://www.panda3d.org/wiki/index.php/Event_Handlers
		self.base.accept(EventType.UPDATE_HUD, self.hud.updateHUD) # hud event listener
		
		self.base.accept(EventType.NEXT_LEVEL, self._nextLevel)
		self.base.accept('n', self._nextLevel)
		
		self.base.accept(EventType.RESTART, self._restart)
		self.base.accept('r', self._restart)
		
		self.base.accept('d', self._toggleDebug )
		
		messenger.send(EventType.RESTART)
	
	def _toggleDebug(self):
		# http://www.panda3d.org/wiki/index.php/The_Default_Camera_Driver
		#self.base.oobe()
		self.base.oobeCull()
	
	def run(self):
		self.base.run()
		
	def _restart(self):
		taskMgr.remove( self.SIM_TASK )
		
		if ( self.model != None ): self.model.cleanUp()
		    
		self.model = GameModel( self.base, self.mapNo)
		self.loop = GameLoop( self.model )
		self.keys = GameControl( self.model, self )
		
		messenger.send(EventType.UPDATE_HUD)
	    
		# http://www.panda3d.org/wiki/index.php/Tasks
		taskMgr.doMethodLater(0.01, self.loop.simulationTask, self.SIM_TASK)

	def _nextLevel(self):
		if (self.mapNo < 2):
			self.mapNo = self.mapNo + 1
			messenger.send(EventType.RESTART)
		else:
			self.mapNo = 0
			messenger.send(EventType.RESTART)
			

if __name__ == "__main__":
	game = GameApplication()
	game.run()
	
	