
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
from Level import Level
from Coin import Coin
from MovingPlane import MovingPlane

class GameModel:
	'''
	Represents the world data.
	TODO: separate physics from this class
	Coordinatates information between Coin and Ball.
	'''

	def __init__(self):
		base.disableMouse()
		base.camera.lookAt(0, 0, 6)
		base.setBackgroundColor(0,0,0)
		
		self.world = self.createWorld()
		self.contactgroup = OdeJointGroup()
		self.space = self.createCollisionSpace(self.world, self.contactgroup)
		self.space.setCollisionEvent("ode-collision")
		base.accept("ode-collision", self.onCollision)
	
		self.setLights()
		
		
		
		self.ball = Ball(self.world, self.space, "Johannes", pos=(0,0,10))
	
		self.kentta = Level(self.space)
		
		plane = MovingPlane( self.space, pos = (0,0,5) )
		plane = MovingPlane( self.space, pos = (0,5,10 ) )
		plane = MovingPlane( self.space, pos = (0,10,15) )
		
		# a set of coins to be collected
		self.coins = []
		self.coins.append( Coin(self.world, self.space, pos = (0,5,15) ) )
		self.coins.append( Coin(self.world, self.space, pos = (0,10,17) ) )

		base.camera.setPos(40, 0, 2)
		
	def setLights(self):
		''' @author latenssi '''
		# Ambient Light
		ambientLight = AmbientLight( 'ambientLight' )
		ambientLight.setColor( Vec4( 0.1, 0.1, 0.1, 1 ) )
		ambientLightNP = render.attachNewNode( ambientLight.upcastToPandaNode() )
		render.setLight(ambientLightNP)

		# Directional light 01
		directionalLight = DirectionalLight( "directionalLight" )
		directionalLight.setColor( Vec4( 1, 1, 1, 1 ) )
		directionalLightNP = render.attachNewNode( directionalLight.upcastToPandaNode() )
		directionalLightNP.setPos(10,-20,20)
		directionalLightNP.lookAt(0,0,0)
		render.setLight(directionalLightNP)

		# Directional light 02
		directionalLight = DirectionalLight( "directionalLight" )
		directionalLight.setColor( Vec4( 1, 1, 1, 1 ) )
		directionalLightNP = render.attachNewNode( directionalLight.upcastToPandaNode() )
		directionalLightNP.lookAt(0,0,0)
		directionalLightNP.setPos(10,20,20)
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
		# (surfaceId1, surfaceId2, mu, bounce, bounce_vel, soft_erp, soft_cfm, slip, dampen)
		world.setSurfaceEntry(0, 0, 0.8, 0.0, 9.1, 0.9, 0.00001, 100.0, 0.002)
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

		for coin in self.coins:
			coin.updateModelNode()
		
		x,y,z = self.ball.getPosition()
		base.camera.lookAt( x,y,z+1 )
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

		for coin in self.coins:
			if body1 == coin.getBody() and body2 == self.ball.getBody():
				coin.collect()
			
		