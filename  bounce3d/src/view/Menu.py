from direct.gui.DirectGui import OnscreenText
# from direct.gui.DirectGui import OnscreenImage

from pandac.PandaModules import TextNode

from model.GameModel import GameModel

from event.Event import createNamedEvent
from event.EventType import EventType

class Menu:
	
	DEFAULT_SELECTION_POINTERS = ["-[", "]-"]
	# BACKGROUND_IMAGE ="../media/bg_test.tif"
	DEFAULT_SELECTION = -1
	DEFAULT_VISIBILITY = False
	
	def __init__(
		self,
		engine,
		info_texts,
		item_texts,
		item_events,
		selection = DEFAULT_SELECTION,
		visibility = DEFAULT_VISIBILITY
	):
		self.engine=engine
		self.info_texts = info_texts
		self.info_table = []
		self.item_texts = item_texts
		self.menu_items = []
		self.item_events = item_events
		self.selection = selection
		self.visible = visibility

	def generateMenu(self):
		
		for i in self.info_texts:
			item = OnscreenText(
				text = i,
				style = 1,
				fg = (1,1,1,1),
				pos = (0,(((len(self.info_texts) + len(self.item_texts))*0.5) -(self.info_texts.index(i))*0.1)),
				align = TextNode.ACenter,
				scale = 0.07
			)
			item.hide()
			self.info_table.append(item)
			
		for i in self.item_texts:
			item = OnscreenText(
				text = i,
				style = 1,
				fg = (1,1,1,1),
				pos = (0,(((len(self.info_texts) + len(self.item_texts))*0.5) -(self.item_texts.index(i))*0.1)),
				align = TextNode.ACenter,
				scale = 0.07
			)
			item.hide()
			self.menu_items.append(item)
		self.selectionDown()

	def selectionUp(self):
		if ( 0 < self.selection ):
			self.menu_items[self.selection].setText(self.item_texts[self.selection])
			self.menu_items[self.selection-1].setText(self.DEFAULT_SELECTION_POINTERS[0] + self.item_texts[self.selection-1] + self.DEFAULT_SELECTION_POINTERS[1])
			self.selection -= 1
		else:
			print "Menu top reached"

	def selectionDown(self):
		if ( self.selection < (len(self.item_texts)-1) ):
			self.menu_items[self.selection].setText(self.item_texts[self.selection])
			self.menu_items[self.selection+1].setText(self.DEFAULT_SELECTION_POINTERS[0] + self.item_texts[self.selection+1] + self.DEFAULT_SELECTION_POINTERS[1])
			self.selection += 1
		else:
			print "Menu bottom reached"

	def select(self):
		self.hideMenu()
		messenger.send(self.item_events[self.selection])
		messenger.send(EventType.CONTROL_CHANGE)
		print "Selection"

	def showMenu(self):
		if not self.visible:
			self.visible = True
			messenger.send(EventType.CONTROL_CHANGE)
			for i in self.menu_items:
				i.show()
			for j in self.info_table:
				j.show()

	# Should only be called when a selection is made
	def hideMenu(self):
		if self.visible:
			self.visible = False
			messenger.send(EventType.CONTROL_CHANGE)
			for i in self.menu_items:
				i.hide()
			for j in self.info_table:
				j.hide()