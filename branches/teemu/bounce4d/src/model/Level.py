from pandac.PandaModules import (OdeTriMeshData, OdeTriMeshGeom)
from model.Coin import Coin
from model.MovingPlane import MovingPlane
from model.Ball import Ball

from model.SurfaceType import SurfaceType

# for Trigger
from pandac.PandaModules import ( CollisionTraverser,
	CollisionSphere, CollisionNode, NodePath,
	PandaNode, CollisionHandlerEvent)


class Level:
	''' Combines level geometry, behaviour and model '''

	POS_DEFAULT = ( 0,0,0 )
	SCALE_DEFAULT = ( 1,1,1 )
	
	def __init__(
		self,
		model,
		pos = POS_DEFAULT,
		scale = SCALE_DEFAULT,
	):
		self.model = model
		self.space = model.space
		self.world = model.world
		self.pos = pos
		self.scale = scale
		self._planes = []
		self._coins = []
		self._triggers = []
		
		self.levelNode = None
		self.ball = model.getBall()
		self.goal = 0 # kerattavat kolikot
		
		self.initCollisionTest()
		
	def initCollisionTest(self):
		self.collHandEvent = CollisionHandlerEvent()
		self.collHandEvent.addInPattern('into-%in')
		base.cTrav = CollisionTraverser('test name')
		if False:
			base.cTrav.showCollisions(render)
		
		cName = 'BallCollNode'
		cSphere = CollisionSphere( 0,0,0, 1.0)
		cNode = CollisionNode( cName )
		cNode.addSolid( cSphere )
		cNodePath = self.ball.modelNode.attachNewNode( cNode )
		base.cTrav.addCollider( cNodePath, self.collHandEvent )
	
	def onTrigger(self, entry):
		print 'trigger on'
		
	def loadLevelEntity( self, mEgg, cEgg):
		self.levelNode = self._createModelNode( self.pos, self.scale, mEgg )
		self.collNode = loader.loadModel( cEgg )
		self.trimesh = OdeTriMeshData( self.collNode, True )
		self.collGeom = OdeTriMeshGeom( self.space, self.trimesh )
		self.space.setSurfaceType( self.collGeom, SurfaceType.FLOOR )
		self.levelNode.flattenStrong()
		self.levelNode.reparentTo( render )

	def _createModelNode( self, pos, scale, modelEgg ):
		modelNode = loader.loadModel( modelEgg ) 
		modelNode.setPos( pos )
		modelNode.setScale( scale )
		return modelNode
		
	def updateModelNode(self):
		map( Coin.updateModelNode, self._coins)
		map( MovingPlane.updateModelNode, self._planes)
		self.exit.updateModelNode()
		
	def removeLevel(self):
		
		self.collGeom = None
		if ( self.levelNode != None ):
			self.levelNode.removeNode()
		
		map( MovingPlane.removeNode, self._planes )
		map( Coin.removeNode, self._coins )
		
		if ( self.exit != None ):
			self.exit.removeNode()
	
	def getExit(self):
		''' Return the geometry of an exit'''
		return self.exit.getGeom()
		
	def getGoal(self):
		return self.goal
		
	def addCoin( self, pos ):
		self._coins.append( Coin(self.world, self.space, pos ) )
	
	def getCoins( self ):
		return self._coins
		
	def addTrigger(self, name, pos, radius, function):
		'''
		Adds a new CollisionNode into base.cTrav and an Event into the EventManager.
		
		http://www.panda3d.org/apiref.php?page=DirectObject
		http://www.panda3d.org/wiki/index.php/Collision_Solids
		http://www.panda3d.org/apiref.php?page=CollisionTraverser
		http://www.panda3d.org/apiref.php?page=CollisionHandlerEvent
		http://www.panda3d.org/apiref.php?page=NodePath#find
		'''
		cSphere = CollisionSphere(pos[0], pos[1], pos[2], radius)
		cNode = CollisionNode( name )
		cNode.addSolid(cSphere)
		
		model = render.find(name) # deletes old one's
		if not model.isEmpty():
			model.removeNode()
		
		# Now we alter global variables. (side-effect)		
		cnodePath = render.attachNewNode( cNode )
		cnodePath.show()
		base.cTrav.addCollider( cnodePath, self.collHandEvent )
		# base.accept( 'into-' + name, self.onTrigger )
		base.accept( 'into-' + name, function )
	
	def addPlane( self, pos, dim, type ):
		self._planes.append( MovingPlane( self.space, pos, dim, type) )
		
	def addExit( self, pos ):
		self.exit = MovingPlane( self.space, pos, (1.0,1.0,1.0) )
		self.addTrigger( 'ExitTriggerNode', pos, 2.0, self.onExit )
		
	def onExit( self, entry ):
		print "On Exit"
		
	