from direct.gui.DirectGui import OnscreenText
# from direct.gui.DirectGui import OnscreenImage

from pandac.PandaModules import TextNode

from model.GameModel import GameModel

from event.Event import createNamedEvent
from event.EventType import EventType

class Menu:
	
	
	OPTIONS = ["Start","Next level"]
	# Should contain Event_Type :s
	OPTION_EVENTS = ["RESTART","NEXT_LEVEL"]
	SELECTION_POINTERS = ["-[","]-"]
	DEFAULT_APPEND = ""
	# BACKGROUND_IMAGE ="../media/bg_test.tif"
	DEFAULT_SELECTION = -1
	
	def __init__(self, menu_text = OPTIONS, default = DEFAULT_SELECTION):
		self.menu_text = menu_text
		self.menu_items = []
		self.selection = default
		
		
		# Generates a menu.
		for i in self.menu_text:
			item = OnscreenText(
				text = i,
				style = 1,
				fg = (1,1,1,1),
				pos = (0,0-(self.menu_text.index(i))*0.1),
				align = TextNode.ACenter,
				scale = 0.07
			)
			item.hide()
			self.menu_items.append(item)
		self.selectionDown()
	
	def selectionUp(self):
		if ( 0 < self.selection ):
			self.menu_items[self.selection].setText(self.OPTIONS[self.selection])
			self.menu_items[self.selection-1].setText(self.SELECTION_POINTERS[0] + self.OPTIONS[self.selection-1] + self.SELECTION_POINTERS[1])
			self.selection -= 1
		else:
			print "Menu top reached"

	def selectionDown(self):
		if ( self.selection < (len(self.OPTIONS)-1) ):
			self.menu_items[self.selection].setText(self.OPTIONS[self.selection])
			self.menu_items[self.selection+1].setText(self.SELECTION_POINTERS[0] + self.OPTIONS[self.selection+1] + self.SELECTION_POINTERS[1])
			self.selection += 1
		else:
			print "Menu bottom reached"

	def select(self):
		'''
		for i in self.OPTIONS:
			if self.selection == self.OPTIONS.index(i):
				messenger.send(EventType.self.OPTION_EVENTS[self.OPTIONS.index(i)]) # Work in progress
		'''
		print "Selection made"
		self.hideMenu()

	def showMenu(self):
		messenger.send(EventType.CONTROL_CHANGE)
		for i in self.menu_items:
			i.show()

	# Should only be called when a selection is made
	def hideMenu(self):
		messenger.send(EventType.CONTROL_CHANGE)
		for i in self.menu_items:
			i.hide()