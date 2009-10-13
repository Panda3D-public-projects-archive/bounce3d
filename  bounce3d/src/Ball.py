
from pandac.PandaModules import (
	Quat,OdeBody, OdeMass, OdeSphereGeom, BitMask32)	
from pandac.PandaModules import OdePlane2dJoint

class Ball:
	
	NAME_DEFAULT = "UNNAMED"
	POS_DEFAULT = ( 0,0,5 )
	SCALE_DEFAULT = ( 1,1,1 )
	HPR_DEFAULT = ( 0,0,0 )
	MODEL_EGG_DEFAULT = "../egg/paahahmo.egg"
	
	BALL_BODY_MASS_WEIGHT = 1000
	BALL_BODY_MASS_RADIUS = 1
	FORCE = 90000
	TORQUE = 3000
	
	def __init__(
	self, 
	world,
	space,
	name = NAME_DEFAULT, 
	modelEgg = MODEL_EGG_DEFAULT,
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
		self.modelNode = self.createModelNode( self.pos, self.hpr, self.scale, modelEgg )
		self.ballBody = self.createBallBody( self.modelNode, self.world )
		self.ballGeom = self.createBallGeom( self.modelNode, self.ballBody, self.space )
		self.modelNode.reparentTo( render )
	
	def createModelNode( self, pos, hpr, scale, modelEgg ):
		modelNode = loader.loadModel( modelEgg ) 
		modelNode.setPos( pos )
		modelNode.setHpr( hpr )
		modelNode.setScale( scale )
		return modelNode
		
	def createBallBody( self, modelNode, world ):
		ballBody = OdeBody( world )
		M = OdeMass()
		M.setSphere( Ball.BALL_BODY_MASS_WEIGHT, Ball.BALL_BODY_MASS_RADIUS )
		ballBody.setMass( M )
		ballBody.setPosition( modelNode.getPos( render ) )
		ballBody.setQuaternion( modelNode.getQuat( render ) )
		return ballBody
	
	def createBallGeom( self, modelNode, ballBody, space ):
		ballGeom = OdeSphereGeom( space, 1 )
		ballGeom.setCollideBits( BitMask32( 0x2 ) )
		ballGeom.setCategoryBits( BitMask32( 0x1 ) )
		ballGeom.setBody( ballBody )
		return ballGeom
	
	def startMoveLeft( self ):
		self.moveLeft = True
	def stopMoveLeft( self ):
		self.moveLeft = False
	def isMovingLeft( self ):
		return self.moveLeft
	
	def startMoveRight( self ):
		self.moveRight = True
	def stopMoveRight( self ):
		self.moveRight = False
	def isMovingRight( self ):
		return self.moveRight
	
	def jump ( self ):
		#TODO ADD IMPLEMENTATION
		pass
	
	def updateModelNode(self):
		''' Update objects after one physics iteration '''
		if self.moveLeft:
			self.ballBody.setForce( y = -Ball.FORCE, x = 0, z = 0 )
			self.ballBody.setTorque( y = -Ball.TORQUE, x = 0, z = 0 )	
		elif self.moveRight:
			self.ballBody.setForce( y = Ball.FORCE, x = 0, z = 0 )
			self.ballBody.setTorque( y = Ball.TORQUE, x = 0, z = 0 )		
		
		# Keep the body in 2d position
		self.alignBodyTo2d()
		
		# Set the new position
		self.modelNode.setPos( render, self.ballBody.getPosition() )
		self.modelNode.setQuat( render, Quat(self.ballBody.getQuaternion() ) )	

	def alignBodyTo2d( self ):
		body = self.ballBody
		
		# Constrain position of the body
		oldPos = body.getPosition()
		newPos = oldPos
		newPos[0] = 0
		newPos[1] = oldPos[1]
		newPos[2] = oldPos[2]
		
		# Constrain quaternion of the body
		oldQuat = body.getQuaternion()
		newQuat = oldQuat
		newQuat[0] = oldQuat[0]
		newQuat[1] = oldQuat[1]
		newQuat[2] = 0
		newQuat[3] = 0
		
		# Set new position and quaternion of the body
		body.setPosition(newPos)
		body.setQuaternion(Quat(newQuat))
	
	def getPosition( self ):
		return self.ballBody.getPosition()
		
	def getBody( self ):
		return self.ballBody
	
