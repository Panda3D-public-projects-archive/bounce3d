from pandac.PandaModules import (OdeTriMeshData, OdeTriMeshGeom)
from model.Coin import Coin
from model.MovingPlane import MovingPlane
from model.Ball import Ball

from model.SurfaceType import SurfaceType
from model.LevelFactory import LevelFactory

class Level:
	''' Combines level geometry, behaviour and model '''
	
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
		self.planes = []
		self.coins = []
		self.levelNode = None
		self.exit = MovingPlane( self.space, (0.0,5.0,1.0), (1.0,1.0,1.0) )
		self.ball = model.getBall()
		self.goal = 0 # kerattavat kolikot
		
		print 'level ', mapNo
		
		if(mapNo == 0):
			self.ball.setPosition( (0.0,-20.0,10.0) )
			self.exit.setPosition(  (0.0,60.0,7.0) )
			self.loadLevelEntity(mapNo)
			
		elif (mapNo == 1):
			self.ball.setPosition( (0.0,-20.0,10.0) )
			self.exit.setPosition( (0.0,5.0,1.0) )
			self.loadLevelEntity(mapNo)
			
		elif(mapNo == 2):
			LevelFactory().load( self, mapNo )
		else:
			raise Error
		

		
	def loadLevelEntity( self, mapNo):
		self.levelNode = self._createModelNode( self.pos, self.scale, self.MODEL_EGG_LIST[mapNo] )
		self.collNode = loader.loadModel( self.COLLISION_EGG_LIST[mapNo] )
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
		map( Coin.updateModelNode, self.coins)
		map( MovingPlane.updateModelNode, self.planes)
		self.exit.updateModelNode()
		
	def removeLevel(self):
		
		self.collGeom = None
		if ( self.levelNode != None ):
			self.levelNode.removeNode()
		
		map( MovingPlane.removeNode, self.planes )
		map( Coin.removeNode, self.coins )
		
		if ( self.exit != None ):
			self.exit.removeNode()
	
	def getExit(self):
		''' Return the geometry of an exit'''
		return self.exit.getGeom()
		
	def getGoal(self):
		return self.goal
		


