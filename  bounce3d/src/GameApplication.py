
# taskMgr
#from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase 

from GameControl import GameControl
from GameLoop import GameLoop

from model.GameModel import GameModel
from view.Hud import Hud

class GameApplication:
	
	def __init__(self):
		self.engine = ShowBase()
		
		model = GameModel( self )
		loop = GameLoop( model )
		keys = GameControl( model )
		
		# http://www.panda3d.org/wiki/index.php/Tasks
		# http://www.panda3d.org/apiref.php?page=TaskManager#doMethodLater
		# params (delayTime, funcOrTask, name)
		taskMgr.doMethodLater(0.2, loop.simulationTask, "Physics Simulation")
		
		hud = Hud()
	
	def run(self):
		self.engine.run()