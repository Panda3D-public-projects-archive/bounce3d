
# mathematics
import math
from pandac.PandaModules import Quat
from pandac.PandaModules import Vec4

# physics - game world
from pandac.PandaModules import (OdeWorld, OdeBody, OdeMass)

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
from event.Event import createNamedEvent
from event.EventType import EventType
		
class GameModel:
	'''
	Represents the world data.
	'''
	
	def __init__(self, app, mapNo):
		self.app = app
		engine = app.engine
		self.camera = engine.camera
		
		self.hud = app.hud
		self.isListening = False
				
		# Holds rigid bodies, joints, controls global params
		self.world = OdeWorld()
		self.world.setGravity(0,0,-9.8)

		self.world.initSurfaceTable(num_surfaces = 1)
		# http://www.panda3d.org/apiref.php?page=OdeWorld#setSurfaceEntry
		# http://www.panda3d.org/wiki/index.php/Collision_Detection_with_ODE
		# (surfaceId1, surfaceId2, mu, bounce, bounce_vel, soft_erp, soft_cfm, slip, dampen)
		self.world.setSurfaceEntry(0, 0, 0.8, 0.0, 9.1, 0.9, 0.00001, 100.0, 0.002)
		
		self.contactgroup = OdeJointGroup()

		self.space = OdeHashSpace()
		self.space.setAutoCollideWorld(self.world)
		self.space.setAutoCollideJointGroup( self.contactgroup )		
		
		self.space.setCollisionEvent("ode-collision")
		
		engine.accept("ode-collision", self.onCollision)
				
		self.ball = Ball(self.hud, self.world, self.space,
		    "Johanneksen pallo", pos=(0.0,-20.0,10.0))
		#ballBody = self.ball.getBody()
		#ballJoint = OdePlane2dJoint(self.world)
		#ballJoint.attachBody(ballBody, 1)
		self.kentta = Level(self.space, mapNo)
		self.player = Player("Johannes")
		
		dim = (5.0,5.0,1.0)
		self.planes = []
		self.planes.append( MovingPlane( self.space, (0.0,0.0,5.0),   dim ) )
		self.planes.append( MovingPlane( self.space, (0.0,5.0,10.0),  dim ) )
		self.planes.append( MovingPlane( self.space, (0.0,10.0,15.0), dim ) )
		
		# a set of coins to be collected
		self.coins = []
		self.coins.append( Coin(self.world, self.space, pos = (0,5,15) ) )
		self.coins.append( Coin(self.world, self.space, pos = (0,10,17) ) )

		self.exit = MovingPlane( self.space, pos = (0.0,25.0,1.0), dim = (1.0,1.0,1.0) )
		self.exitid = self.exit.getId()
	
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
		map( Coin.updateModelNode, self.coins)
		map( MovingPlane.updateModelNode, self.planes)

		x,y,z = self.ball.getPosition()
		self.camera.lookAt( x,y,z+1 )
		# alter only y-axis
		cx,cy,cz = self.camera.getPos()
		self.camera.setPos( cx, y, cz )
	
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
		
		exit = self.exit.getGeom()
		if geom1 == exit or geom2 == exit:
			self.app.nextLvl()
			# TODO: send event Level Restart
	
	# end onCollision
	
	
	def cleanUp(self):
	    map( MovingPlane.removeNode, self.planes )
	    map( Coin.removeNode, self.coins )
	    self.ball.removeNode()
	
