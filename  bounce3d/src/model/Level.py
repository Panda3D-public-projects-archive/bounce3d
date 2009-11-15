from pandac.PandaModules import OdeTriMeshData
from pandac.PandaModules import OdeTriMeshGeom
from pandac.PandaModules import OdeTriMeshGeom

class Level:
	
	MODEL_EGG_DEFAULT = "../egg/level0_1_visual.egg"
	COLLISION_EGG_DEFAULT = "../egg/level0_1_collision.egg"
	POS_DEFAULT = ( 0,0,0 )
	SCALE_DEFAULT = ( 1,1,1 )
	
	def __init__(
	self,
	space,
	modelEgg = MODEL_EGG_DEFAULT,
	collisionEgg = COLLISION_EGG_DEFAULT,
	pos = POS_DEFAULT,
	scale = SCALE_DEFAULT,
	):
		self.space = space
		self.pos = pos
		self.scale = scale
		self.modelNode = self.createModelNode( self.pos, self.scale, modelEgg )
		self.collNode = loader.loadModel( collisionEgg )
		self.trimesh = OdeTriMeshData( self.collNode, True )
		self.collGeom = OdeTriMeshGeom( self.space, self.trimesh )
		self.modelNode.reparentTo( render )
	
	def createModelNode( self, pos, scale, modelEgg ):
		modelNode = loader.loadModel( modelEgg ) 
		modelNode.setPos( pos )
		modelNode.setScale( scale )
		return modelNode