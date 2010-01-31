
from pandac.PandaModules import (
	Quat,OdeBody, OdeMass, OdeBoxGeom, BitMask32)
	
from pandac.PandaModules import (CollisionTraverser,
	CollisionSphere, CollisionNode, NodePath,
	PandaNode, CollisionHandlerEvent)

from model.SurfaceType import SurfaceType

class Coin:
	"""
	An object that a ball collects.
	"""
	MODEL = "../egg/kolikko.egg"
	collectable = 0

	def __init__(self, model, world, space, pos):
		self.model = model
		self.world = world
		self.space = space
		self.collHandEvent = CollisionHandlerEvent()
		self.collHandEvent.addInPattern('into-%in')
		self.addBox(pos)
		self.isCollected = False
		Coin.collectable += 1
    
	def collect(self):
		if not self.isCollected:
			self.isCollected = True
			self.box.setColor(1,0,0)
			Coin.collectable -= 1

	def onCollide(self, entry):
		body1 = entry.getFromNodePath()
		ballNode = self.model.getBall().getModelNode()
		if ballNode and ballNode == body1.getParent():
			self.collect()

	def addBox(self, pos):
		lx,ly,lz = 1,1,1   # dimension
		px,py,pz = pos # position
		name = "box" + str(pos)
		self.box = loader.loadModel(self.MODEL)
		self.box.setPos(-0.5,-0.5,-0.5)
		self.box.flattenLight() # ApplyTransform
		self.box.reparentTo(render)
		
		# Make sure its center is at 0, 0, 0 like OdeBoxGeom
		self.box.setPos( px -lx/2, py -ly/2, pz -lz/2)
		self.box.setScale( lx, ly, lz )
		self.box.setHpr( 0, 50, 0 )
		
		# Offset z by -1.0 because the coin model was so small
		cSphere = CollisionSphere(pos[0], pos[1], pos[2] - 1.0, 1)
		cNode = CollisionNode(name)
		cNode.addSolid(cSphere)
		
		model = render.find(name)
		if not model.isEmpty():
			model.removeNode()
			
		cnodePath = render.attachNewNode( cNode )
		#cnodePath.show()
		base.cTrav.addCollider( cnodePath, self.collHandEvent )
		base.accept( 'into-' + name, self.onCollide )
		
		# Implementation below would not allow coins to float?
		# define mass
		"""
		mass = OdeMass()
		mass.setBox(500, lx, ly, lz)
		
		self.boxBody = OdeBody( self.world )
		self.boxBody.setPosition( self.box.getPos(render) )
		self.boxBody.setQuaternion( self.box.getQuat(render) )
		self.boxBody.setMass( mass )
		
		self.geom = OdeBoxGeom( self.space, lx, ly, lz)
		self.space.setSurfaceType( self.geom, SurfaceType.COIN )
		self.geom.setBody( self.boxBody )
		self.boxBody = None
		"""
	def updateModelNode(self):
		return None
		#None
		#self.box.setPos( render, self.boxBody.getPosition() )
		#self.box.setQuat(render, Quat(self.boxBody.getQuaternion() ) )
	
	def getBody(self):
		return None
		#return self.boxBody
	
	def removeNode(self):
		if not self.isCollected:
			Coin.collectable -= 1
		# http://www.panda3d.org/apiref.php?page=NodePath#removeNode
		self.box.removeNode()

