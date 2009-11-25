from pandac.PandaModules import (OdeTriMeshData, OdeTriMeshGeom)
from model.Coin import Coin
from model.MovingPlane import MovingPlane

class Level:
	
	MODEL_EGG_LIST=[
		"../egg/level0_1_visual.egg",
		"../egg/level0_2_visual.egg",
		"../egg/level0_1_visual.egg" ]
	COLLISION_EGG_LIST=[
		"../egg/level0_1_collision.egg",
		"../egg/level0_2_collision.egg",
		"../egg/level0_1_collision.egg"]
	POS_DEFAULT = ( 0,0,0 )
	SCALE_DEFAULT = ( 1,1,1 )
	
	def __init__(
		self,
		space,
		world,
		mapNo,
		pos = POS_DEFAULT,
		scale = SCALE_DEFAULT,
	):
		self.space = space
		self.world = world
		self.pos = pos
		self.scale = scale
		self.modelNode = self.createModelNode( self.pos, self.scale,
			self.MODEL_EGG_LIST[mapNo] )
		self.collNode = loader.loadModel( self.COLLISION_EGG_LIST[mapNo] )
		self.trimesh = OdeTriMeshData( self.collNode, True )
		self.collGeom = OdeTriMeshGeom( self.space, self.trimesh )
		
		self.modelNode.flattenStrong()
		self.modelNode.reparentTo( render )
		
		self.loadEntities(mapNo)
	
	def createModelNode( self, pos, scale, modelEgg ):
		modelNode = loader.loadModel( modelEgg ) 
		modelNode.setPos( pos )
		modelNode.setScale( scale )
		return modelNode
	
	def removeLevel (self):
		self.collGeom = None
		self.modelNode.removeNode()
		self.unloadEntities()
	
	def unloadEntities( self ):
		map( MovingPlane.removeNode, self.planes )
		map( Coin.removeNode, self.coins )
		self.exit.removeNode()
	
	def loadEntities( self, mapNo ):
		self.planes = []
		self.coins = []
		
		if(mapNo == 0):
			self.exit = MovingPlane( self.space, (0.0,5.0,1.0), (1.0,1.0,1.0) )
			
			dim = (5.0,5.0,1.0)
			self.planes.append( MovingPlane( self.space, (0.0,0.0,5.0),   dim ) )
			self.planes.append( MovingPlane( self.space, (0.0,5.0,10.0),  dim ) )
			self.planes.append( MovingPlane( self.space, (0.0,10.0,15.0), dim ) )

			self.coins.append( Coin(self.world, self.space, pos = (0,5,15) ) )
			self.coins.append( Coin(self.world, self.space, pos = (0,10,17) ) )
		elif(mapNo == 1):
			self.exit = MovingPlane( self.space, (0.0,5.0,1.0), (1.0,1.0,1.0) ) 
		else:
			self.exit = MovingPlane( self.space, (0.0,5.0,1.0), (1.0,1.0,1.0) ) 
		
	def updateModelNode(self):
		map( Coin.updateModelNode, self.coins)
		map( MovingPlane.updateModelNode, self.planes)
	
	def getExit(self):
		''' Return the geometry of an exit'''
		return self.exit.getGeom()
	