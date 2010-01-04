
# mathematics
import math
from pandac.PandaModules import (Quat, Vec4)

# physics - game world
from pandac.PandaModules import (OdeWorld, OdeBody, OdeMass)

# physics - collision
from pandac.PandaModules import (OdeSimpleSpace, OdeHashSpace,
 OdeJointGroup, OdeBoxGeom, OdeSphereGeom, OdePlaneGeom)

from pandac.PandaModules import (BitMask32, CardMaker, OdePlane2dJoint)

from pandac.PandaModules import (CollisionNode, CollisionSphere,
CollisionTraverser, CollisionHandlerQueue)

# collision detection
# from pandac.PandaModules import LPoint3f

from model.Ball import Ball

from model.Player import Player
from model.Coin import Coin
from model.Camera import Camera

from event.Event import createNamedEvent
from event.EventType import EventType

from model.SurfaceType import SurfaceType
from model.LevelFactory import LevelFactory

class GameModel:
	#Represents the world data.
	
	def __init__(self, base, mapNo):
		self.isListening = False
		
		# Holds rigid bodies, joints, controls global params
		self.world = OdeWorld()
		self.world.setGravity(0,0,-9.8)
		
		st = SurfaceType()
		st.load( self.world )
		del st
		
		self.contactgroup = OdeJointGroup()
		
		self.space = OdeHashSpace()
		self.space.setAutoCollideWorld(self.world)
		self.space.setAutoCollideJointGroup( self.contactgroup )
		self.space.setCollisionEvent(EventType.ODE_COLLISION)
		base.accept(EventType.ODE_COLLISION, self.onCollision)
		
		self.ball = Ball(self.world, self.space, "Johanneksen pallo")
		
		factory = LevelFactory()
		self.level = factory.load( self, mapNo )
		self.player = Player("Johannes")
		
		self.camera = Camera(base, self.ball)
	
	def turnGravityTask(self):
		''''''
		g = self.world.getGravity()
		g = -g
		self.world.setGravity( g )
		self.camera.turn()
	
	def turnGravityTask2(self):
		''''''
		g = self.world.getGravity()
		g2 = self.ball.perpendicularUnitVec3WithFixedX(g)
		g2 *= g.length()
		self.world.setGravity( g2 )
	
	def updateObjects(self):
		'''
		Update objects after one physics iteration
		@see GameLoop.simulationTask
		'''
		self.ball.updateModelNode()
		self.level.updateModelNode()
		self.camera.updateModelNode()
		
	def getBall(self):
		return self.ball
	
	def getPlayer(self):
		return self.player
	
	# http://www.panda3d.org/wiki/index.php/Collision_Detection_with_ODE
	def onCollision(self, entry):
		geom1 = entry.getGeom1()
		geom2 = entry.getGeom2()
		body1 = entry.getBody1()
		body2 = entry.getBody2()
	
		# Is the ball touching something?
		if body1 == self.ball.getBody() or body2 == self.ball.getBody():
			self.ball.refreshCollisionTime(entry)
	
		for coin in self.level.getCoins():
			if body1 == coin.getBody() and body2 == self.ball.getBody():
				coin.collect()
				messenger.send(EventType.UPDATE_HUD)
		
		exit = self.level.getExit()
		if geom1 == exit or geom2 == exit:
			if Coin.collectable == self.level.getGoal():
				# todo: make event based
				messenger.send(EventType.NEXT_LEVEL)
		
		
	
	def cleanUp(self):
		self.level.removeLevel()
		self.ball.removeNode()
		
