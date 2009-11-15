from pandac.PandaModules import OdeTriMeshData
from pandac.PandaModules import OdeTriMeshGeom
from pandac.PandaModules import OdeTriMeshGeom

class Level:
	
	MODEL_EGG_LIST=["../egg/level0_1_visual.egg", "../egg/level0_2_visual.egg", "../egg/level0_1_visual.egg" ]
	COLLISION_EGG_LIST=["../egg/level0_1_collision.egg", "../egg/level0_2_collision.egg", "../egg/level0_1_collision.egg"]
	POS_DEFAULT = ( 0,0,0 )
	SCALE_DEFAULT = ( 1,1,1 )
	
	def __init__(
	self,
	space,
	mapNo,
	pos = POS_DEFAULT,
	scale = SCALE_DEFAULT,
	):
		self.space = space
		self.pos = pos
		self.scale = scale
		self.modelNode = self.createModelNode( self.pos, self.scale, self.MODEL_EGG_LIST[mapNo] )
		self.collNode = loader.loadModel( self.COLLISION_EGG_LIST[mapNo] )
		self.trimesh = OdeTriMeshData( self.collNode, True )
		self.collGeom = OdeTriMeshGeom( self.space, self.trimesh )
		self.modelNode.reparentTo( render )
	
	def createModelNode( self, pos, scale, modelEgg ):
		modelNode = loader.loadModel( modelEgg ) 
		modelNode.setPos( pos )
		modelNode.setScale( scale )
		return modelNode
	
	def removeLevel (self):
		self.collGeom = None
		self.modelNode.removeNode()