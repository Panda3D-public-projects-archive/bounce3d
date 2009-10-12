
from pandac.PandaModules import Quat

from pandac.PandaModules import OdeBody
from pandac.PandaModules import OdeMass

from pandac.PandaModules import OdeSphereGeom
from pandac.PandaModules import BitMask32

class Ball:

	NAME_DEFAULT = "UNNAMED"
	POS_DEFAULT = (0,0,0)
	SCALE_DEFAULT = (1,1,1)
	HPR_DEFAULT = (0,0,0)
	
	BALL_BODY_MASS_WEIGHT = 1000
	BALL_BODY_MASS_RADIUS = 1
	
	def __init__(
	self, 
	world,
	space,
	name = NAME_DEFAULT, 
	pos = POS_DEFAULT, 
	scale = SCALE_DEFAULT, 
	hpr = HPR_DEFAULT,
	):
		self.name = name
		self.pos = pos
		self.hpr = hpr
		self.scale = scale
		self.world = world
		self.space = space
		self.moveLeft = False
		self.moveRight = False
		self.modelNode = self.createModelNode(self.pos, self.hpr, self.scale)
		self.ballBody = self.createBallBody(self.modelNode, self.world)
		self.ballGeom = self.createBallGeom(self.modelNode, self.ballBody, self.space)
		
	def createModelNode(self, pos, hpr, scale):
		modelNode = loader.loadModel("smiley") 
		modelNode.setPos( pos )
		modelNode.setHpr( hpr )
		modelNode.setScale( scale )
		modelNode.reparentTo(render)
		return modelNode
		
	def createBallBody(self, modelNode, world):
		ballBody = OdeBody(world)
		M = OdeMass()
		M.setSphere(Ball.BALL_BODY_MASS_WEIGHT, Ball.BALL_BODY_MASS_RADIUS)
		ballBody.setMass(M)
		ballBody.setPosition(modelNode.getPos(render))
		ballBody.setQuaternion(modelNode.getQuat(render))
		return ballBody
	
	def createBallGeom(self, modelNode, ballBody, space):
		ballGeom = OdeSphereGeom( space, 1 )
		ballGeom.setCollideBits( BitMask32( 0x2 ) )
		ballGeom.setCategoryBits( BitMask32( 0x1 ) )
		ballGeom.setBody(ballBody)
		return ballGeom
	
	def startMoveLeft(self):
		self.moveLeft = True
	def stopMoveLeft(self):
		self.moveLeft = False
	
	def startMoveRight(self):
		self.moveRight = True
	def stopMoveRight(self):
		self.moveRight = False
	
	def moveRight(self):
		self.ballBody.setForce( y = 10000, x = 0, z = 0)
		self.ballBody.setTorque( y = 1000, x = 0, z = 0)
		
	def moveLeft(self):
		self.ballBody.setForce( y = -10000, x = 0, z = 0)
		self.ballBody.setTorque( y = -1000, x = 0, z = 0)		
	
	def updateModelNode(self):
		''' Update objects after one physics iteration '''
		if self.moveLeft:
			self.ballBody.setForce( y = -10000, x = 0, z = 0)
			self.ballBody.setTorque( y = -1000, x = 0, z = 0)	
		elif self.moveRight:
			self.ballBody.setForce( y = 10000, x = 0, z = 0)
			self.ballBody.setTorque( y = 1000, x = 0, z = 0)		
			
		# Set the new position
		self.modelNode.setPos(render, self.ballBody.getPosition())
		self.modelNode.setQuat(render, Quat(self.ballBody.getQuaternion() ) )	
		
	def getPosition(self):
		return self.ballBody.getPosition()
	
