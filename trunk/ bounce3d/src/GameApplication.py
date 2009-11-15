
# taskMgr
from direct.showbase.ShowBase import ShowBase 

from GameControl import GameControl
from GameLoop import GameLoop

from model.GameModel import GameModel
from view.Hud import Hud
from view.GameView import GameView

class GameApplication:
	
	def __init__(self):
		self.engine = ShowBase()
		self.hud = Hud()
		view = GameView( self.engine )
		
		self.model = None
		self.loop = None
		self.keys = None
		self.mapNo = 0
		
		self.restart()
	
	def run(self):
		self.engine.run()
		
	def restart(self):
		'''todo: restart the ball position '''
		taskMgr.remove("Physics Simulation", )
		
		if ( self.model != None ):
		    self.model.cleanUp()
		    
		self.model = GameModel( self, self.mapNo)
		self.loop = GameLoop( self.model )
		self.keys = GameControl( self.model, self )
	    
		taskMgr.doMethodLater(0.1,
		    self.loop.simulationTask,
		    "Physics Simulation")
		#taskMgr.popupControls()

	def nextLvl(self):
		if (self.mapNo < 2):
			self.mapNo = self.mapNo + 1
			print "Loadin map no." 
			print self.mapNo + 1
			self.restart()
		else:
			print "Out of maps, restarting last level"
			self.restart()

if __name__ == "__main__":
	game = GameApplication()
	game.run()
			
	