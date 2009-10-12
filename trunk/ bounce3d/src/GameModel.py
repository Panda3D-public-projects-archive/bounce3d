
# loader, task manager
import direct.directbase.DirectStart

# mathematics
import math
from pandac.PandaModules import Quat
from pandac.PandaModules import Vec4

# physics - game world
from pandac.PandaModules import OdeWorld
from pandac.PandaModules import OdeBody
from pandac.PandaModules import OdeMass

# physics - collision
from pandac.PandaModules import OdeSimpleSpace
from pandac.PandaModules import OdeHashSpace
from pandac.PandaModules import OdeJointGroup
from pandac.PandaModules import OdeBoxGeom
from pandac.PandaModules import OdeSphereGeom
from pandac.PandaModules import OdePlaneGeom

from pandac.PandaModules import BitMask32
from pandac.PandaModules import CardMaker

# lights
from pandac.PandaModules import AmbientLight
from pandac.PandaModules import DirectionalLight

from Ball import Ball

class GameModel:
	''' Represents the world data. TODO: separate physics from this class'''
	
	COLLIDE_BITS = BitMask32( 0x00000002 )
	CATEGORY_BITS = BitMask32( 0x00000001 )
	
	def __init__(self):
		self.world = self.createWorld()
		self.contactgroup = OdeJointGroup()
		self.space = self.createCollisionSpace(self.world, self.contactgroup)
		self.space.setCollisionEvent("ode-collision")
		base.accept("ode-collision", self.onCollision)
		
		self.ball = Ball(self.world, self.space, "Johannes")
		self.addBox()
		self.addPlane()
		#self.initEnvironment()
		
		# Set the camera position
		base.disableMouse()
		base.camera.setPos(40, 0, 1)
		base.camera.lookAt(0, 0, 5)
		
		self.setLights()
		
		self.counter = 0
	
	def reset(self):
		''' not implemented '''
		pass
	
	def initEnvironment(self):
		environ = loader.loadModel("models/environment")
		environ.reparentTo(render)
		environ.setScale(0.4, 0.4, 0.4)
		environ.setPos(-8, 20, 0)
	
	"""
	def initBall(self):		
		# physical model
		self.body = OdeBody(self.world)
		M = OdeMass()
		# Densities:
		# 1000 kg / m^3 = water
		# 11340 kg / m^3 = lead
		M.setSphere( density = 4000, radius = 0.5 )
		self.body.setMass(M)
		self.body.setPosition(0,0,5)
		
		# rendering model
		self.ball = loader.loadModel("smiley")
		self.ball.reparentTo(render)
		self.ball.setScale( 1.0, 1.0, 1.0 )
		self.ball.setColor(0.5, 0.5, 0.5, 1)		
		self.ball.setPos( self.body.getPosition() ) # only initial
		
		# Collision Sphere
		geom = OdeSphereGeom( self.space, 1 )
		#geom.setCollideBits( GameModel.COLLIDE_BITS )
		#geom.setCategoryBits( GameModel.CATEGORY_BITS )
		# This will automatically reposition the geometry with regard
		# to the position of the related body in the OdeWorld.		
		geom.setBody(self.body) 
	"""
	
	def addBox(self):
		self.box = loader.loadModel("box")
		self.box.reparentTo(render)
		# Make sure its center is at 0, 0, 0 like OdeBoxGeom
		self.box.setPos( 0, 3, 6)
		self.box.setScale( 1.0, 1.0, 1.0 )
		self.box.setHpr( 0, 50, 0 )
		
		# define mass
		mass = OdeMass()
		mass.setBox( 50, 1.0, 1.0, 1.0)
		
		self.boxBody = OdeBody( self.world )
		self.boxBody.setPosition( self.box.getPos(render) )
		self.boxBody.setQuaternion( self.box.getQuat(render) )
		self.boxBody.setMass( mass )
		
		geom = OdeBoxGeom( self.space, 1.0, 1.0, 1.0)
		#geom.setCollideBits( GameModel.COLLIDE_BITS )
		#geom.setCategoryBits( GameModel.CATEGORY_BITS )
		geom.setBody( self.boxBody )
	
	def addPlane(self):
		# http://www.panda3d.org/apiref.php?page=CardMaker
		cm = CardMaker("groud")
		cm.setFrame( -20, 20, -20, 20)

		ground = render.attachNewNode( cm.generate() )
		ground.setPos(0,0,0)
		ground.lookAt(0,0,-1)
		ground.setColor(0,0,1.0,1)
		
		# http://www.ode.org/ode-latest-userguide.html#sec_10_7_3
		geom = OdePlaneGeom( self.space, Vec4( 0, 0, 1, 0) )
		#geom.setCollideBits( BitMask32( 0x00000003 ) )
		#geom.setCategoryBits( BitMask32( 0x00000004 ) )
		
	def setLights(self):
		''' @author latenssi '''
		# Ambient Light
		ambientLight = AmbientLight( 'ambientLight' )
		ambientLight.setColor( Vec4( 0.1, 0.1, 0.1, 1 ) )
		ambientLightNP = render.attachNewNode( ambientLight.upcastToPandaNode() )
		render.setLight(ambientLightNP)

		# Directional light 01
		directionalLight = DirectionalLight( "directionalLight" )
		directionalLight.setColor( Vec4( 0, 0, 0, 1 ) )
		directionalLightNP = render.attachNewNode( directionalLight.upcastToPandaNode() )
		directionalLightNP.setPos(-10,0,5)
		directionalLightNP.lookAt(0,0,0)
		render.setLight(directionalLightNP)

		# Directional light 02
		directionalLight = DirectionalLight( "directionalLight" )
		directionalLight.setColor( Vec4( 1, 0.5, 0.3, 1 ) )
		directionalLightNP = render.attachNewNode( directionalLight.upcastToPandaNode() )
		directionalLightNP.lookAt(0,0,0)
		directionalLightNP.setPos(10,0,-5)
		render.setLight(directionalLightNP)
		
	def createWorld(self):
		'''
		PRE: none
		POST: new physics world
		'''
		# Holds rigid bodies, joints, controls global params
		world = OdeWorld()
		world.setGravity(0,0,-9.8)

		world.initSurfaceTable(num_surfaces = 1)
		# http://www.panda3d.org/apiref.php?page=OdeWorld#setSurfaceEntry
		# http://www.panda3d.org/wiki/index.php/Collision_Detection_with_ODE
		world.setSurfaceEntry(pos1 = 0, pos2 = 0, mu = 15000, 
			bounce = 0.0, bounce_vel = 9.1, soft_erp = 0.9,
			soft_cfm = 0.00001, slip = 0.0, dampen = 0.002)
		return world

	def createCollisionSpace(self, world, joints):
		'''
		PRE: initialized world and joints
		POST: new collision space
		'''
		space = OdeHashSpace()
		space.setAutoCollideWorld(world)
		space.setAutoCollideJointGroup( joints )
		return space	
		
	def turnGravityTask(self):
		''''''
		g = self.world.getGravity()
		g = -g
		self.world.setGravity( g )
	
	def startMoveLeft(self):
		self.ball.startMoveLeft()
	def stopMoveLeft(self):
		self.ball.stopMoveLeft()
	def startMoveRight(self):
		self.ball.startMoveRight()
	def stopMoveRight(self):
		self.ball.stopMoveRight()
		
	def updateObjects(self):
		''' Update objects after one physics iteration '''
		self.ball.updateModelNode()

		self.box.setPos( render, self.boxBody.getPosition() )
		self.box.setQuat(render, Quat(self.boxBody.getQuaternion() ) )
		
		x,y,z = self.ball.getPosition()
		base.camera.lookAt( x,y,z )
		# alter only y-axis
		cx,cy,cz = base.camera.getPos()
		base.camera.setPos( cx, y, cz )
	
	def getPallo(self):
		return self.ball
		
	def onCollision(self, entry):
		geom1 = entry.getGeom1()
		geom2 = entry.getGeom2()
		body1 = entry.getBody1()
		body2 = entry.getBody2()
		
		self.counter = self.counter + 1
		
		#print "some collision ", self.counter