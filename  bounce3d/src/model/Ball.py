import math

from pandac.PandaModules import (
	Quat,OdeBody, OdeMass, OdeSphereGeom, BitMask32)
from pandac.PandaModules import OdePlane2dJoint
from pandac.PandaModules import Vec4
from pandac.PandaModules import VBase3

from direct.directtools.DirectGeometry import LineNodePath

# from direct.directbase.DirectStart import *

from model.SurfaceType import SurfaceType

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

	MOVEMENT_DEBUG = 0
	JUMP_DEBUG = 0
	STATIC_JUMP = 0
	STATIC_JUMP_FORCE = 2800000
	JUMP_FORCE = 120000
	MAX_JUMP_REACH_TIME = 0.7
	COLLISION_THRESHOLD_TIME = 0.33

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
		self.jumping = False
		self.jumpStarted = 0.0
		self.jumpLastUpdate = 0.0
		self.lastCollisionTime = 0.0
		self.lastCollisionIsGround = True
		self.lastGroundCollisionBodyPos = None
		
		if Ball.MOVEMENT_DEBUG:
			self.lastDrawTime = 0.0
			self.lastDrawTime2 = 0.0
			self.lines = LineNodePath(parent = render, thickness = 3.0, colorVec = Vec4(1, 0, 0, 1))
			self.lines2 = LineNodePath(parent = render, thickness = 3.0, colorVec = Vec4(0, 0, 1, 1))
			self.lines3 = LineNodePath(parent = render, thickness = 3.0, colorVec = Vec4(0, 1, 0, 1))
		if Ball.JUMP_DEBUG:
			self.lastTakeoffTime = 0.0
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
		space.setSurfaceType( ballGeom, SurfaceType.BALL )
		return ballGeom
	
	def getDefaultGravityVec3( self ):
		out = VBase3()
		out.setX(0.0)
		out.setY(0.0)
		out.setZ(-9.8)
		return out
	def angleVec3( self, v1, v2):
		return math.acos(self.dotProductVec3(v1, v2)/(v1.length()*v2.length()))
	def dotProductVec3( self, v1, v2 ):
		return v1.getX()*v2.getX()+v1.getY()*v2.getY()+v1.getZ()*v2.getZ()
	def moveBall( self, normalGravity, func ):
		g = self.world.getGravity()
		angle = self.angleVec3(g,self.getDefaultGravityVec3())
		if not (angle > math.pi/3.99 and angle < math.pi / 1.99):
			if normalGravity:
				func()
		else:
			if not normalGravity:
				func()
		return
	def arrowRightDown( self ):
		self.moveBall(1,self.startMoveRight)
	def arrowRightUp( self ):
		self.moveBall(1,self.stopMoveRight)
	def arrowLeftDown( self ):
		self.moveBall(1,self.startMoveLeft)
	def arrowLeftUp( self ):
		self.moveBall(1,self.stopMoveLeft)
	def arrowUpDown( self ):
		self.moveBall(0,self.startMoveRight)
	def arrowUpUp( self ):
		self.moveBall(0,self.stopMoveRight)
	def arrowDownDown( self ):
		self.moveBall(0,self.startMoveLeft)
	def arrowDownUp( self ):
		self.moveBall(0,self.stopMoveLeft)

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
		
	def perpendicularUnitVec3WithFixedX(self, v):
		out = VBase3()
		a = 1.0
		out.setX(0.0)
		if v.getY() != 0.0:
			out.setY(-(v.getZ()*a)/v.getY())
			out.setZ(a)
		else:
			out.setY(a)
			out.setZ(0.0)
		out /= out.length()
		return out
		
	def jumpOn( self ):
		if self.isColliding() == True and self.lastCollisionIsGround:
			self.jumping = True
			self.jumpStarted = globalClock.getLongTime()
		return

	def jumpOff( self ):
		self.jumping = False
		self.jumpStarted = 0.0
		self.jumpLastUpdate = 0.0
		return

	def isColliding( self ):
		if self.lastCollisionTime == 0.0:
			return False

		now = globalClock.getLongTime()
		interval = now - self.lastCollisionTime
                
		if interval < Ball.COLLISION_THRESHOLD_TIME:
			if Ball.JUMP_DEBUG:
				self.lastTakeoffTime = 0.0
			return True
		else:
			if Ball.JUMP_DEBUG:
				# Draw debug info
				if self.lastTakeoffTime == 0.0:
					self.lastTakeoffTime = now
					messenger.send('updateHUD', [", Ball state: AIR"])
			return False
	
	def isGroundCollision( self, bodyPos, colPos ):
		# Tolerance should probably be some fraction of the radius
		g = self.world.getGravity()
		g /= g.length()
		# g *= Ball.RADIUS
		bodyPos[0] = bodyPos[0] + g.getX() 
		bodyPos[1] = bodyPos[1] + g.getY()
		bodyPos[2] = bodyPos[2] + g.getZ()
		return self.areCloseEnough(bodyPos, colPos)

	def areCloseEnough( self, pos1, pos2 ):
		tolerance = 0.3
		dy = pos1[1] - pos2[1]
		# >= is important
		if (dy >= 0.0 and dy < tolerance) or (dy < 0.0 and dy > -tolerance):
			dz = pos1[2] - pos2[2]
			# >= is important
			if (dz >= 0.0 and dz < tolerance) or (dz < 0.0 and dz > -tolerance):
				return True
		return False
		
	def refreshCollisionTime( self, collisionEntry):
		body = self.ballBody
		pos = body.getPosition()
		now = globalClock.getLongTime()
		
		'''
		Only "sample" collisions occasionally, should be enough for jumping.
		This also effects the collision threshold time, which should be somewhat
		larger (maybe twice?) than this value for jumping to work properly
		'''
		
		if now - self.lastCollisionTime < 0.15:
			return
		
		self.lastCollisionTime = now 
		
		if Ball.JUMP_DEBUG:
			previous = self.lastCollisionIsGround
		
		self.lastCollisionIsGround = False
		n = collisionEntry.getNumContacts()

		for i in range(n):
			p = collisionEntry.getContactPoint(i)
			if Ball.MOVEMENT_DEBUG and now - self.lastDrawTime > 0.1:
				self.lines2.reset()
				x = p.getX() + 1.2 # This will bring the line in front of the ball
				y = p.getY()
				z = p.getZ()
				self.lines2.drawLines([((x, y, z), (x, y-1.0, z+2.0))]) # "marker" will be a line upwards tilting to the left
				self.lines2.create()
				self.lastDrawTime = now
			if self.isGroundCollision(pos,p):
				self.lastCollisionIsGround = True
				self.lastGroundCollisionBodyPos = pos
				break
		
		if not self.lastCollisionIsGround and self.lastGroundCollisionBodyPos != None:
			if self.areCloseEnough(pos, self.lastGroundCollisionBodyPos):
				self.lastCollisionIsGround = True
				# Position should not be updated, since this was not technically a ground collision
				# as we normally judge them
		
		if Ball.JUMP_DEBUG:
			# Draw debug info
			if previous != self.lastCollisionIsGround or self.lastTakeoffTime != 0.0:
				self.lastTakeoffTime = 0.0
				if self.lastCollisionIsGround:
					messenger.send('updateHUD', [", Ball state: GROUND"])
				else:
					messenger.send('updateHUD', [", Ball state: ???"])
					
	def updateModelNode(self):
		''' Update objects after one physics iteration '''		
		now = globalClock.getLongTime()
		body = self.ballBody
		g = self.world.getGravity()
		
		if Ball.MOVEMENT_DEBUG and now - self.lastDrawTime2 > 0.2:
			v = body.getLinearVel()
			v2 = self.perpendicularUnitVec3WithFixedX(v)
			self.lines.reset()
			self.lines3.reset()
			x = body.getPosition().getX() + 1.2 # This will bring the line in front of the ball
			y = body.getPosition().getY()
			z = body.getPosition().getZ()
			self.lines.drawLines([((x, y, z), (x+v.getX(), y+v.getY(), z+v.getZ()))])
			self.lines3.drawLines([((x, y, z), (x+v2.getX(), y+v2.getY(), z+v2.getZ()))])
			self.lines.create()
			self.lines3.create()
			self.lastDrawTime2 = 0.0

		''' Can move better when on (touching) something, moving in the air is harder '''
		divisor = 3.5
		if self.isColliding() and self.lastCollisionIsGround:
		   divisor = 1.0

		if self.moveLeft or self.moveRight:
			factor = 1.0
			if self.moveLeft:
				factor = -1.0
			v3 = self.perpendicularUnitVec3WithFixedX(g)
			v3 *= factor*Ball.FORCE/divisor
			self.ballBody.setForce( y = v3.getY() , x = v3.getX(), z = v3.getZ())
			v3 = self.perpendicularUnitVec3WithFixedX(g)
			v3 *= factor*Ball.TORQUE/divisor
			self.ballBody.setTorque( y = v3.getY(), x = v3.getX(), z = v3.getX())	

		''' This is still really crappy, will revise later '''
		if self.jumping == True:
			g = -g
			g /= g.length()
			if Ball.STATIC_JUMP:
				g *= Ball.STATIC_JUMP_FORCE
				self.ballBody.setForce( y = g.getY(), x = g.getX(), z = g.getZ())
				self.jumping = False
			else:
				elapsed = now - self.jumpStarted
				if elapsed > 0.0 and elapsed < Ball.MAX_JUMP_REACH_TIME:	
					g *= Ball.JUMP_FORCE
					self.ballBody.setForce( y = g.getY(), x = g.getX(), z = g.getZ())
				elif elapsed > Ball.MAX_JUMP_REACH_TIME:
					self.jumping = False 
	
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
	
	def setPosition( self, pos):
		self.ballBody.setPosition( pos )
	
	def getBody( self ):
		return self.ballBody

	def getModelNode( self ):
                return self.modelNode
	
	def removeNode(self):
	    self.modelNode.removeNode()
