
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
from pandac.PandaModules import OdePlane2dJoint

# lights
from pandac.PandaModules import AmbientLight
from pandac.PandaModules import DirectionalLight

from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionHandlerQueue

# collision detection
# from pandac.PandaModules import LPoint3f

from model.Ball import Ball
from model.Level import Level
from model.Player import Player
from model.Coin import Coin
from model.MovingPlane import MovingPlane

class GameModel:
	'''
	Represents the world data.
	TODO: separate physics from this class
	Coordinatates information between Coin and Ball.
	'''

	def __init__(self, application):
		
		self.app = application
		self.engine = self.app.engine
	
		self.engine.disableMouse()
		self.engine.camera.lookAt(0, 0, 6)
		self.engine.setBackgroundColor(0,0,0)
		
		self.isListening = False
		
		
		self.world = self.createWorld()
		self.contactgroup = OdeJointGroup()
		self.space = self.createCollisionSpace(self.world, self.contactgroup)
		self.space.setCollisionEvent("ode-collision")
		self.engine.accept("ode-collision", self.onCollision)
	
		self.setLights()
		
		self.ball = Ball(self.app, self.world, self.space, "Johanneksen pallo", pos=(0,0,10))
		#ballBody = self.ball.getBody()
		#ballJoint = OdePlane2dJoint(self.world)
		#ballJoint.attachBody(ballBody, 1)
		self.kentta = Level(self.space)
		self.player = Player("Johannes")
		
		plane = MovingPlane( self.space, pos = (0,0,5) )
		plane = MovingPlane( self.space, pos = (0,5,10 ) )
		plane = MovingPlane( self.space, pos = (0,10,15) )
		
		# a set of coins to be collected
		self.coins = []
		self.coins.append( Coin(self.world, self.space, pos = (0,5,15) ) )
		self.coins.append( Coin(self.world, self.space, pos = (0,10,17) ) )

		self.engine.camera.setPos(40, 0, 2)

		#self.traverser = CollisionTraverser('collision traverser')

		#base.cTrav = self.traverser
		#self.collisionQueue = CollisionHandlerQueue()
		#test = self.ball.getModelNode().attachNewNode(CollisionNode('colNode'))
		#test.node().addSolid(CollisionSphere(0, 0, 0, 12))
		#self.traverser.addCollider(test, self.collisionQueue)
		#self.traverser.addCollider(self.ball.getBody(), onBallCollision)
		
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
	
	def turnGravityTask2(self):
		''''''
		g = self.world.getGravity()
		g2 = self.ball.perpendicularUnitVec3WithFixedX(g)
		g2 *= g.length()
		self.world.setGravity( g2 )
	
	def updateObjects(self):
		''' Update objects after one physics iteration '''
		self.ball.updateModelNode()

		for coin in self.coins:
			coin.updateModelNode()
		
		x,y,z = self.ball.getPosition()
		self.engine.camera.lookAt( x,y,z+1 )
		# alter only y-axis
		cx,cy,cz = self.engine.camera.getPos()
		self.engine.camera.setPos( cx, y, cz )
	
	def getBall(self):
		return self.ball
	def getPlayer(self):
		return self.player
		
	def onCollision(self, entry):
		geom1 = entry.getGeom1()
		geom2 = entry.getGeom2()
		body1 = entry.getBody1()
		body2 = entry.getBody2()

		# Is the ball touching something?
		if body1 == self.ball.getBody() or body2 == self.ball.getBody():
			self.ball.refreshCollisionTime(entry)

		for coin in self.coins:
			if body1 == coin.getBody() and body2 == self.ball.getBody():
				coin.collect()
			
		
