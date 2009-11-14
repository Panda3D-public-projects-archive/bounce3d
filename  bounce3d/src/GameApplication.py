
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
		
		self.restart()
	
	def run(self):
		self.engine.run()
		
	def restart(self):
		'''todo: restart the ball position '''
		taskMgr.remove("Physics Simulation", )
		
		if ( self.model != None ):
		    self.model.cleanUp()
		    
		self.model = GameModel( self )
		self.loop = GameLoop( self.model )
		self.keys = GameControl( self.model, self )
	    
		taskMgr.doMethodLater(0.1,
		    self.loop.simulationTask,
		    "Physics Simulation")
		#taskMgr.popupControls()
		
if __name__ == "__main__":
	game = GameApplication()
	game.run()
			
	