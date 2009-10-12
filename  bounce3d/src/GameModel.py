
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
		self.kentta = Level(self.space)
		
		# a set of coins to be collected
		self.coins = []
		self.coins.append( Coin(self.world, self.space, pos = (0,10,6) ) )
		self.coins.append( Coin(self.world, self.space, pos = (0,5,6) ) )
		
		# some elevator that are moving
		#self.addGround( pos = (0,0,-10 ) )
		#self.addGround( pos = (0,5,-5 ) )
		#self.addGround( pos = (0,10,0 ) )
		
		# Set the camera position
		base.disableMouse()
		base.camera.setPos(20, 0, 2)
		base.camera.lookAt(0, 0, 6)
		
		self.setLights()
		
		self.counter = 0
	
	def reset(self):
		''' not implemented '''
		pass

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
	
	def addGround(self, pos):
		'''move this somewhere else'''
		lx,ly,lz = 5,5,1   # dimension
		px,py,pz = pos # position
	
		self.ground = loader.loadModel("box")
		self.ground.reparentTo(render)
		self.ground.setScale( lx, ly, lz )
		self.ground.setPos( px -lx/2, py -ly/2, pz -lz/2)
		
		geom = OdeBoxGeom( self.space, lx, ly, lz)
		geom.setPosition( px, py, pz)
		
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
		
		self.counter = self.counter + 1
		
		#print "some collision ", self.counter