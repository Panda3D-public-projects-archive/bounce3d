from pandac.PandaModules import (OdeTriMeshData, OdeTriMeshGeom)
from model.Coin import Coin
from model.MovingPlane import MovingPlane
from model.Ball import Ball

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
		model,
		mapNo,
		pos = POS_DEFAULT,
		scale = SCALE_DEFAULT,
	):
		self.model = model
		self.space = model.space
		self.world = model.world
		self.pos = pos
		self.scale = scale
		
		self.levelNode = None
		self.exit = None # Every level should have an exit
		
		self.loadEntities(mapNo)
		
		self.goal = 0 # kerattavat kolikot
	
	def createModelNode( self, pos, scale, modelEgg ):
		modelNode = loader.loadModel( modelEgg ) 
		modelNode.setPos( pos )
		modelNode.setScale( scale )
		return modelNode
	
	def removeLevel(self):
		self.collGeom = None
		if ( self.levelNode != None ):
			self.levelNode.removeNode()
		
		map( MovingPlane.removeNode, self.planes )
		map( Coin.removeNode, self.coins )
		if ( self.exit != None ):
			self.exit.removeNode()
	
	def loadLevelEntity( self, mapNo):
		self.levelNode = self.createModelNode( self.pos, self.scale,
			self.MODEL_EGG_LIST[mapNo] )
		self.collNode = loader.loadModel( self.COLLISION_EGG_LIST[mapNo] )
		self.trimesh = OdeTriMeshData( self.collNode, True )
		self.collGeom = OdeTriMeshGeom( self.space, self.trimesh )
		
		self.levelNode.flattenStrong()
		self.levelNode.reparentTo( render )
		
	def loadEntities( self, mapNo ):
		self.planes = []
		self.coins = []
		
		if(mapNo == 0):
			ball = self.model.getBall().setPosition( (0.0,-20.0,10.0) )
			self.loadLevelEntity(mapNo)
			self.exit = MovingPlane( self.space, (0.0,60.0,7.0), (1.0,1.0,1.0) )
		elif(mapNo == 1):
			ball = self.model.getBall().setPosition( (0.0,-20.0,10.0) )
			ball = self.model.getBall()
			ball.pos = (0.0,-20.0,10.0)
			self.loadLevelEntity(mapNo)
			self.exit = MovingPlane( self.space, (0.0,5.0,1.0), (1.0,1.0,1.0) ) 
		elif(mapNo == 2):
			''' Testing Level '''
			ball = self.model.getBall().setPosition( (0.0,-20.0,-10.0) )
			
			dim = (5.0,5.0,1.0)
			plane = MovingPlane( self.space, (0.0,0.0,5.0),   dim )
			plane.rotate = True
			self.planes.append( plane )
			
			for x in xrange(1,5):
				plane = MovingPlane( self.space, (0.0, -5.0*x, -5.0*x+5.0), dim )
			
			for x in xrange(-5,5):
				plane = MovingPlane( self.space, (0.0, -5.0*x, -25.0), (5.0, 5.0, 1.0) )
				
			for x in xrange(-5,5):
				plane = MovingPlane( self.space, (0.0, -5.0*x, 20.0), (5.0, 5.0, 1.0) )
			
			self.coins.append( Coin(self.world, self.space, pos = (0.0,-5.0,15.0) ) )
			self.coins.append( Coin(self.world, self.space, pos = (0.0,-10.0,17.0) ) )
			
			# we will not update exit, it remains static
			self.exit = MovingPlane( self.space, (0.0,5.0,1.0), (1.0,1.0,1.0) )
		else:
			ball = self.model.getBall().setPosition( (0.0,-20.0,10.0) )
			self.loadLevelEntity(mapNo)
			self.exit = MovingPlane( self.space, (0.0,5.0,1.0), (1.0,1.0,1.0) ) 
			
		
	def updateModelNode(self):
		map( Coin.updateModelNode, self.coins)
		map( MovingPlane.updateModelNode, self.planes)
	
	def getExit(self):
		''' Return the geometry of an exit'''
		return self.exit.getGeom()
	
	def getGoal(self):
		return self.goal
	