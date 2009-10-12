'''
	Bounce3d
	@authors: Teemustin, J3lly, latenssi
'''


# Mielestani on hyva tapa kirjoittaa
# tarkasti kaikki luokkien ja pakkauksien
# valiset riippuvuudet.

# system
import sys

# loader, task manager
import direct.directbase.DirectStart
from direct.task import Task

# animation
from direct.actor import Actor

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

# plotting text
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import TextNode

# keyboard
from direct.showbase.DirectObject import DirectObject

# lights
from pandac.PandaModules import AmbientLight
from pandac.PandaModules import DirectionalLight

class GameModel:
	''' Represents the world data. TODO: separate physics from this class'''
	
	def __init__(self):
		self.world = self.createWorld()
		self.contactgroup = OdeJointGroup()
		self.space = self.createCollisionSpace(self.world, self.contactgroup)

		# outlook model
		boxModel = loader.loadModel("smiley")
		boxModel.reparentTo(render)
		boxModel.setScale( 1.0, 1.0, 1.0 )
		boxModel.setPos(0,0,5)
		boxModel.setColor(0.5, 0.5, 0.5, 1)
		boxModel.setHpr(0,45,45)
		self.boxModel = boxModel
		
		# physical model
		body = OdeBody(self.world)
		M = OdeMass()
		#M.setBox(density = 50, lx = 1, ly = 1, lz = 1)
		M.setSphere( 50, 0.5 )
		body.setMass(M)
		body.setPosition( boxModel.getPos(render) )
		body.setQuaternion( boxModel.getQuat(render) )
		self.body = body
		
		# physical collision
		#boxGeom = OdeBoxGeom( self.space, 1, 1, 1)
		boxGeom = OdeSphereGeom( self.space, 1 )
		boxGeom.setCollideBits( BitMask32( 0x00000002 ) )
		boxGeom.setCategoryBits( BitMask32( 0x00000001 ) )
		boxGeom.setBody(body)

		# http://www.panda3d.org/apiref.php?page=CardMaker
		cm = CardMaker("groud")
		cm.setFrame( -20, 20, -20, 20)

		ground = render.attachNewNode( cm.generate() )
		ground.setPos(0,0,0)
		ground.lookAt(0,0,-1)
		ground.setColor(0,0,.3,1)
		# http://www.ode.org/ode-latest-userguide.html#sec_10_7_3
		groundGeom = OdePlaneGeom( self.space, Vec4( 0, 0, 1, 0) )
		groundGeom.setCollideBits( BitMask32( 0x00000001 ) )
		groundGeom.setCategoryBits( BitMask32( 0x00000002 ) )

		cm2 = CardMaker("groud")
		cm2.setFrame( -20, 20, -20, 20)
		ground2 = render.attachNewNode( cm2.generate() )
		ground2.setPos(0,0,10)
		ground2.lookAt(0,0,-1)
		ground2.setHpr( 0, 90, 0)
		ground2.setColor(0,0.3,0,1)


		# Set the camera position
		base.disableMouse()
		base.camera.setPos(40, 0, 5)
		base.camera.lookAt(0, 0, 5)
		
		self.setLights()
	
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
		world.setSurfaceEntry(pos1 = 0, pos2 = 0, mu = 150, 
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
		
	def moveRight(self):
		self.body.setForce( y = 10000, x = 0, z = 0)
		self.body.setTorque( y = 1000, x = 0, z = 0)
		
	def moveLeft(self):
		self.body.setForce( y = -10000, x = 0, z = 0)
		self.body.setTorque( y = -1000, x = 0, z = 0)		
	
	def updateObjects(self):
		''' Update objects after one physics iteration '''
		# Set the new position
		self.boxModel.setPos(render, self.body.getPosition())
		self.boxModel.setQuat(render, Quat(self.body.getQuaternion() ) )
	
class GameControl:
	''' Game Loop on eras kontrolli '''

	def __init__(self, fps, model):
		# Simulaation kaytetty aika
		self.simTime = 0.0
		# frame time in seconds
		self.stepSize = 1.0 / fps
		self.model = model

	def simulationTask(self, task):
		''' contains the main loop '''
		
		model = self.model
		
		# Setup the contact joints
		model.space.autoCollide()
		
		# http://www.panda3d.org/apiref.php?page=ClockObject
		self.simTime += globalClock.getDt()
		
		while self.simTime > self.stepSize:
			self.simTime -= self.stepSize
			model.world.quickStep( self.stepSize )
		
		#
		model.updateObjects()
		
		# Clear the contact joints
		model.contactgroup.empty()
		
		return Task.cont

class KeyboardControl(DirectObject):
	''' @author J3lly '''

	def __init__(self, model):
	
		self.accept("arrow_up" , self.KeyDo, [1])
		self.accept("arrow_up-repeat" , self.KeyDo, [2])
		self.accept("arrow_down" , self.KeyDo, [3])
		self.accept("arrow_down-repeat" , self.KeyDo, [4])
		self.accept("arrow_left" , model.moveLeft )
		self.accept("arrow_left-repeat" , self.KeyDo, [6])
		self.accept("arrow_right" , model.moveRight )
		self.accept("arrow_right-repeat" , self.KeyDo, [8])
		 
		self.accept("space", model.turnGravityTask )
	  
	def KeyDo(task, key):
		if key==1:
			print "Up"
		if key==2:
			print"Up repeat"
		if key==3:
			print "Down"
		if key==4:
			print"Down repeat"
		if key==5:
			print "Left"
		if key==6:
			print"Left repeat"
		if key==7:
			print "Right"
		if key==8:
			print"Right repeat"
		return Task.done

class GameApplication(DirectObject):
	
	def __init__(self):
		model = GameModel()
		loop = GameControl( 60.0, model )
		keys = KeyboardControl( model )
		
		# http://www.panda3d.org/wiki/index.php/Tasks
		# http://www.panda3d.org/apiref.php?page=TaskManager#doMethodLater
		taskMgr.doMethodLater(delayTime = 0.2,
			funcOrTask = loop.simulationTask,
			name = "Physics Simulation")
			
		self.createHUD()
		
	def createHUD(self):
		'''
		PRE: call once
		POST: a stylished text is placed on the screen.
		'''
		# Add a text on the screen.
		helpText = OnscreenText(
			text = "Turn gravity [SPACE], moving [ARROWS]",
			style = 1,
			fg = (1,1,1,1),
			pos = (-1.25,0.85),
			align = TextNode.ALeft,
			scale = 0.07
		)
		helpText.show()
	
	def run(self):
		base.run()

if __name__ == "__main__":
	game = GameApplication()
	game.run()
	
	