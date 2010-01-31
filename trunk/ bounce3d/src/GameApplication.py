
# taskMgr
# messenger
from direct.showbase.ShowBase import ShowBase

from direct.gui.DirectGui import OnscreenText
from direct.gui.DirectGui import DirectWaitBar

from pandac.PandaModules import TextNode

from GameControl import GameControl
from GameLoop import GameLoop

from model.GameModel import GameModel
from view.Hud import Hud
from view.Menu import Menu
from view.GameView import GameView

from event.EventType import EventType

import sys

class GameApplication:
	
	SIM_TASK = "Physics Simulation"
	LOAD_TIME = 5
	START_MAP = 0
	TOGGLE_VERB = False
	BG_MUSIC = "../media/Stereo.mp3"
	
	def __init__(self):
	
		self.base = ShowBase()
		self.hud = self.model = self.loop = self.keys = None
		self.mapNo = self.START_MAP
		self.view = GameView( self.base )
		self.keyInit = False
		self.bg_music = loader.loadSfx(GameApplication.BG_MUSIC)
		
		if self.TOGGLE_VERB:
			print 'INIT KONTROLLIT:'
			print self.keys
		
		# Menues
		self.brmenu = Menu(
			self.base,
			[""],
			[ "Start","Controls","Exit"],
			[EventType.RESTART,EventType.INFO_M, EventType.EXIT],
			True,
			-.26
		)
		self.mmenu = Menu(
			self.base,
			["Main Menu"],
			[ "Continue", "Restart", "Highscores", "Exit"],
			[EventType.MENU, EventType.RESTART, EventType.MENU_HS, EventType.EXIT],
			False,
			0
		)
		self.hs = Menu(
			self.base,
			["Highscores", "***", "Test1 9:59:99", "Test2 9:59:99", "Test3 9:59:99"],
			["Back"],
			[EventType.MENU],
			False,
			0
		)
		
		self.infom = Menu(
			self.base,
			["Controls", "***", "Arrows: Moving", "Space: Jumping", "M: In-game menu", "***"],
			["Back"],
			[EventType.BR_MENU],
			True,
			-.66,
			0.55
		)
		
		print 'HS MENU @:'
		print self.hs
		# In-game menues
		self.menues = [self.brmenu,self.mmenu,self.hs,self.infom]
		
		self.initEvents()
		self.beforeStart()
		#messenger.send(EventType.RESTART)
		
	def initEvents(self):
		if(self != None): messenger.ignoreAll(self)
		if(self.model != None): messenger.ignoreAll(self.model)
		if(self.keys != None): messenger.ignoreAll(self.keys)
		
		# http://www.panda3d.org/wiki/index.php/Event_Handlers
		if( self.hud != None ): self.base.accept(EventType.UPDATE_HUD, self.hud.updateHUD) # hud event listener
		
		self.base.accept(EventType.MENU, self.mmenu.showMenu) # Menu event listener
		self.base.accept('m', self.mmenu.showMenu)
		
		self.base.accept(EventType.MENU_HS, self.hs.showMenu)
		
		self.base.accept(EventType.NEXT_LEVEL, self._nextLevel)
		self.base.accept('n', self._nextLevel)
		
		self.base.accept(EventType.RESTART, self._restart)
		self.base.accept('r', self._restart)
		
		self.base.accept('d', self._toggleDebug )
		
		self.base.accept(EventType.EXIT, sys.exit)
		
		self.base.playMusic(self.bg_music, looping = 1)
	
	def getActiveMenu(self):
		x = -1
		for i  in range(len(self.menues)):
			if (self.menues[i].getVisibility()):
				x = i
				break
		if x != -1:
			return self.menues[x]
	
	def _toggleDebug(self):
		# http://www.panda3d.org/wiki/index.php/The_Default_Camera_Driver
		#self.base.oobe()
		self.base.oobeCull()
	
	def run(self):
		self.base.run()
		
	def beforeStart(self):
		self.base.accept(EventType.BR_MENU, self.brmenu.showMenu)
		self.base.accept(EventType.INFO_M, self.infom.showMenu)
		print 'GameApplication.beforeStart'
		#self.hud.hideHUD()
		self.keys = GameControl(self.model, self)
		
		if self.TOGGLE_VERB:
			print 'ALOTUS KONTROLLIT:'
			print self.keys
		
		self.brmenu.showMenu()
		self.run()
		
	def initSIM_and_HUD(self, task):
		if (self.hud != None): self.hud.clearHUD()
		self.hud = Hud()
		taskMgr.doMethodLater(0, self.loop.simulationTask, self.SIM_TASK, extraArgs=[self.hud])	
		
	def _restart(self):
		self.brmenu.bgShow()
		
		self.initEvents()
		
		taskMgr.remove( self.SIM_TASK )
		
		if ( self.model != None ): self.model.cleanUp()
		
		self.model = GameModel( self.base, self.mapNo)
		self.loop = GameLoop( self.model )
		
		if(self.keyInit):
			self.keys.updateResources( self.model, self )
		else:
			self.keys = GameControl( self.model, self)
			self.keyInit = True
		
		if self.TOGGLE_VERB:
			print 'IN-GAME KONTROLLIT:'
			print self.keys
		# http://www.panda3d.org/wiki/index.php/Tasks
		taskMgr.doMethodLater(self.LOAD_TIME -0.01, self.brmenu.bgHide, 'bg')
		taskMgr.doMethodLater(self.LOAD_TIME, self.initSIM_and_HUD, 'sh')

	def _nextLevel(self):
		if (self.mapNo < 2):
			self.mapNo = self.mapNo + 1
			messenger.send(EventType.RESTART)
		else:
			messenger.send(EventType.EXIT)
			#messenger.send(EventType.RESTART)
			

if __name__ == "__main__":
	game = GameApplication()
	game.run()
	
	