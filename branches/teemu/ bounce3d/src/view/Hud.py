# plotting text
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import TextNode

from model.Coin import Coin

class Hud:
	'''
		a stylished text is placed on the screen.
	'''
	DEFAULT = "Jump [SPACE], moving [ARROWS], turn gravity [g/h], degub mode [d]"
	COINS_TEXT = "Collect coins:"
	DEFAULT_APPEND = ""
	
	def __init__(self, basetext = DEFAULT):
		self.basetext = basetext
		
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
		
		self.updateHUD()
		
	def updateHUD(self, append=DEFAULT_APPEND):
		self.helpText1.setText(self.basetext + append)
		self.helpText2.setText(Hud.COINS_TEXT + " " + str(Coin.collectable) )
		
	