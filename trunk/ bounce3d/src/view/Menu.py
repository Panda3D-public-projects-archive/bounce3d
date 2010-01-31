from direct.gui.DirectGui import OnscreenText
from direct.gui.DirectGui import OnscreenImage

from pandac.PandaModules import TextNode
from pandac.PandaModules import *


from model.GameModel import GameModel

from direct.showbase import *

from event.Event import createNamedEvent
from event.EventType import EventType

class Menu:
	
	DEFAULT_SELECTION_POINTERS = ["-[", "]-"]
	BACKGROUND_IMAGE ="../media/menuBg800x600.tif"
	DEFAULT_SELECTION = -1
	DEFAULT_VISIBILITY = False
	
	def __init__(
		self,
		engine,
		info_texts,
		item_texts,
		item_events,
		img_load,
		offset,
		selection = DEFAULT_SELECTION,
		visibility = DEFAULT_VISIBILITY,
		bgi = BACKGROUND_IMAGE
	):
		self.engine=engine
		self.info_texts = info_texts
		self.info_table = []
		self.item_texts = item_texts
		self.menu_items = []
		self.item_events = item_events
		self.img_load = img_load
		self.offset = offset
		self.selection = selection
		self.visible = visibility
		self.bgi = bgi
		self.bg_image = None
		self.font = loader.loadFont("../media/DejaVuCondensedSansBold.ttf")
		
		self.generateMenu()

	def generateMenu(self):
		
		for i in self.info_texts:
			item = OnscreenText(
				text = i,
				style = 1,
				fg = (1,1,1,1),
				font = self.font,
				pos = (0,((len(self.info_texts) + len(self.item_texts) - self.info_texts.index(i))*0.1) + self.offset),
				align = TextNode.ACenter,
				drawOrder = 1,
				parent = render2d,
				scale = 0.1
			)
			item.hide()
			self.info_table.append(item)
			
		for j in self.item_texts:
			item = OnscreenText(
				text = j,
				style = 1,
				fg = (1,1,1,1),
				font = self.font,
				pos = (0,((len(self.item_texts) - self.item_texts.index(j))*0.1) + self.offset),
				align = TextNode.ACenter,
				drawOrder = 1,
				parent = render2d,
				scale = 0.06
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
		if ( self.selection < (len(self.menu_items)-1)):
			self.menu_items[self.selection].setText(self.item_texts[self.selection])
			self.menu_items[self.selection+1].setText(self.DEFAULT_SELECTION_POINTERS[0] + self.item_texts[self.selection+1] + self.DEFAULT_SELECTION_POINTERS[1])
			self.selection += 1
		else:
			print "Menu bottom reached"

	def select(self):
		self.bgHide()
		messenger.send(self.item_events[self.selection])
		self.hideMenu()
		print "Selection ", self

	def showMenu(self):
		if not self.visible:
			self.visible = True
			messenger.send(EventType.CONTROL_CHANGE)
			for i in self.menu_items:
				i.show()
			for j in self.info_table:
				j.show()
			print "Menu loaded"

	# Should only be called when a selection is made
	def hideMenu(self):
		if self.visible:
			self.visible = False
			messenger.send(EventType.CONTROL_CHANGE)
			for i in self.menu_items:
				i.hide()
			for j in self.info_table:
				j.hide()
			print "Menu unloaded"
	
	def getVisibility(self):
		return self.visible
	
	def bgHide(self, task = None):
		if self.img_load:
			self.bg_image.destroy()
	
	def bgShow(self):
		if self.img_load:
			self.bg_image = OnscreenImage(image = self.bgi, pos = (0, 0, 0), scale = (1,1,1), parent = render2d)