
from pandac.PandaModules import (
	Quat,OdeBody, OdeMass, OdeBoxGeom, BitMask32)

from model.SurfaceType import SurfaceType

class Coin:
	"""
	An object that a ball collects.
	"""
	MODEL = "box.egg"
	collectable = 0

	def __init__(self, world, space, pos):
		self.world = world
		self.space = space
		self.addBox(pos)
		self.isCollected = False
		Coin.collectable += 1
    
	def collect(self):
		if not self.isCollected:
			self.isCollected = True
			self.box.setColor(1,0,0)
			Coin.collectable -= 1

	def addBox(self, pos):
		lx,ly,lz = 1,1,1   # dimension
		px,py,pz = pos # position
		
		self.box = loader.loadModel(self.MODEL)
		self.box.setPos(-0.5,-0.5,-0.5)
		self.box.flattenLight() # ApplyTransform
		self.box.reparentTo(render)
		
		# Make sure its center is at 0, 0, 0 like OdeBoxGeom
		self.box.setPos( px -lx/2, py -ly/2, pz -lz/2)
		self.box.setScale( lx, ly, lz )
		self.box.setHpr( 0, 50, 0 )
		
		# define mass
		mass = OdeMass()
		mass.setBox( 500, lx, ly, lz)
		
		self.boxBody = OdeBody( self.world )
		self.boxBody.setPosition( self.box.getPos(render) )
		self.boxBody.setQuaternion( self.box.getQuat(render) )
		self.boxBody.setMass( mass )
		
		self.geom = OdeBoxGeom( self.space, lx, ly, lz)
		self.space.setSurfaceType( self.geom, SurfaceType.COIN )
		self.geom.setBody( self.boxBody )
	
	def updateModelNode(self):
		self.box.setPos( render, self.boxBody.getPosition() )
		self.box.setQuat(render, Quat(self.boxBody.getQuaternion() ) )
	
	def getBody(self):
		return self.boxBody
	
	def removeNode(self):
		if not self.isCollected:
			Coin.collectable -= 1
		# http://www.panda3d.org/apiref.php?page=NodePath#removeNode
		self.box.removeNode()
