# plotting text
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import *

from model.Coin import Coin

class Hud:
	'''
		a stylished text is placed on the screen.
	'''
	DEFAULT = "Jump [SPACE], moving [ARROWS], turn gravity [g/h], degub mode [d]"
	COINS_TEXT = "Collect coins:"
	TIMER_TEXT = "Time: "
	DEFAULT_APPEND = ""
	DEBUG = False
	
	def __init__(self, basetext = DEFAULT):
		self.time = ClockObject()
		self.basetext = basetext
		self.font = loader.loadFont("../media/DejaVuCondensedSansBold.ttf")
		
		if Hud.DEBUG:
			# Add a text on the screen.
			self.helpText1 = OnscreenText(
				text = self.basetext,
				style = 1,
				fg = (1,1,1,1),
				pos = (-1.25,0.85),
				align = TextNode.ALeft,
				scale = 0.07
			)
			self.helpText1.show()
			
			self.helpText2 = OnscreenText(
				text = Hud.COINS_TEXT,
				style = 2,
				fg = (1,1,1,1),
				pos = ( -1.25, -0.85 ),
				align = TextNode.ALeft,
				scale = 0.07
			)
			self.helpText2.show()
			
		self.helpText3 = OnscreenText(
		    text = Hud.TIMER_TEXT + ' 00:00',
		    style = 2,
			font = self.font,
		    fg = (1,1,1,1),
		    pos = ( 0.8, -0.85 ),
		    align = TextNode.ALeft,
		    scale = 0.07
		)
		self.helpText3.show()
		
		self.updateHUD()
		
	def updateHUD(self, append=DEFAULT_APPEND):
		if Hud.DEBUG:
			self.helpText1.setText(self.basetext + append)
			self.helpText2.setText(Hud.COINS_TEXT + " " + str(Coin.collectable) )
		
		# http://www.panda3d.org/phpbb2/viewtopic.php?t=2630
		# http://www.panda3d.org/phpbb2/viewtopic.php?t=315
		curtime = int(self.time.getRealTime())
		curmins = int(curtime/60)
		curtext = Hud.TIMER_TEXT + self.format(str(curmins%60)) + ':' + self.format(str(curtime%60))
		self.helpText3.setText(curtext)
	
	def format(self, t_str):
		if len(t_str) != 2:
			t_str = '0' + t_str
		return t_str

	
	def hideHUD(self):
		if Hud.DEBUG:
			self.helpText1.hide()
			self.helpText2.hide()
		self.helpText3.hide()
	
	def showHUD(self):
		if Hud.DEBUG:
			self.helpText1.show()
			self.helpText2.show()
		self.helpText3.show()
	
	def clearHUD(self):
		self.hideHUD
		if Hud.DEBUG:
			self.helpText1.destroy()
			self.helpText2.destroy()
		self.helpText3.destroy()