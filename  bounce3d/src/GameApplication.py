
# taskMgr
# messenger
from direct.showbase.ShowBase import ShowBase 

from GameControl import GameControl
from GameLoop import GameLoop

from model.GameModel import GameModel
from view.Hud import Hud
from view.GameView import GameView

class GameApplication:
	
	def __init__(self):
		self.base = ShowBase()
		self.model = None
		self.loop = None
		self.keys = None
		self.mapNo = 0
		self.hud = Hud()
		self.view = GameView( self.base )
		
		# CULLING!
		self.base.accept('d', self.toggleDebug )
		
		# create hud event listener
		# http://www.panda3d.org/wiki/index.php/Event_Handlers
		self.base.accept('updateHUD', self.hud.updateHUD)
		self.base.accept('nextLevel', self.nextLvl)
		self.base.accept('restart', self.restart)
		
		self.restart()
	
	def toggleDebug(self):
		# http://www.panda3d.org/wiki/index.php/The_Default_Camera_Driver
		#self.base.oobe()
		self.base.oobeCull()
	
	def run(self):
		self.base.run()
		
	def restart(self):
		taskMgr.remove("Physics Simulation", )
		
		if ( self.model != None ):
		    self.model.cleanUp()
		    
		self.model = GameModel( self.base, self.mapNo)
		self.loop = GameLoop( self.model )
		self.keys = GameControl( self.model, self )
	    
		# http://www.panda3d.org/wiki/index.php/Tasks
		taskMgr.doMethodLater(0.01, self.loop.simulationTask, "Physics Simulation")

	def nextLvl(self):
		if (self.mapNo < 2):
			self.mapNo = self.mapNo + 1
			print "Loading map no. ", self.mapNo 
			print self.mapNo + 1
			self.restart()
		else:
			print "Out of maps, restarting last level"
			self.restart()

if __name__ == "__main__":
	game = GameApplication()
	game.run()
	
	