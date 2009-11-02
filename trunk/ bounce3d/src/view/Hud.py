# plotting text
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import TextNode

class Hud:
	'''
		a stylished text is placed on the screen.
	'''
	def __init__(self):
	
		# Add a text on the screen.
		self.helpText = OnscreenText(
			text = "Jump [SPACE], moving [ARROWS], turn gravity [g/h]",
			style = 1,
			fg = (1,1,1,1),
			pos = (-1.25,0.85),
			align = TextNode.ALeft,
			scale = 0.07
		)
		self.helpText.show()
		
	def updateHUD(self, append):
		self.helpText.setText("Jump [SPACE], moving [ARROWS], turn gravity [g/h]" + append)
	