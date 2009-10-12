
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
from pandac.PandaModules import OdePlaneGeom

from pandac.PandaModules import BitMask32
from pandac.PandaModules import CardMaker

# plotting text
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import TextNode

# keyboard
from direct.showbase.DirectObject import DirectObject

#
# PRE: 
# POST:
#
def createWorld():
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

#
# PRE:
# POST:
#
def createCollisionSpace(world, joints):
	space = OdeHashSpace()
	space.setAutoCollideWorld(world)
	space.setAutoCollideJointGroup( joints )
	return space
	
world = createWorld()
contactgroup = OdeJointGroup()
space = createCollisionSpace(world, contactgroup)

# outlook model
boxModel = loader.loadModel("smiley")
boxModel.reparentTo(render)
boxModel.setPos(0,0,5)
boxModel.setColor(0.5, 0.5, 0.5, 1)
boxModel.setHpr(0,45,45)

# physical model
boxBody = OdeBody(world)
M = OdeMass()
#M.setBox(density = 50, lx = 1, ly = 1, lz = 1)
M.setSphere( 50, 0.5 )
boxBody.setMass(M)
boxBody.setPosition( boxModel.getPos(render) )
boxBody.setQuaternion( boxModel.getQuat(render) )

# physical collision
boxGeom = OdeBoxGeom(space, 1, 1, 1)
boxGeom.setCollideBits( BitMask32( 0x00000002 ) )
boxGeom.setCategoryBits( BitMask32( 0x00000001 ) )
boxGeom.setBody(boxBody)

# http://www.panda3d.org/apiref.php?page=CardMaker
cm = CardMaker("groud")
cm.setFrame( -20, 20, -20, 20)

ground = render.attachNewNode( cm.generate() )
ground.setPos(0,0,0)
ground.lookAt(0,0,-1)
ground.setColor(0,0,.3,1)
# http://www.ode.org/ode-latest-userguide.html#sec_10_7_3
groundGeom = OdePlaneGeom( space, Vec4( 0, 0, 1, 0) )
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
base.camera.setPos(30, 0, 0)
base.camera.lookAt(0, 0, 0)

# Simulaation kaytetty aika
deltaTimeAccumulator = 0.0
stepSize = 1.0 / 90.0


def simulationTask(task):
	global deltaTimeAccumulator
	
	# Setup the contact joints
	space.autoCollide()
	
	# The problem with using the delta time of a task to
	# step the simulation is that the time between tasks
	# might not be consistent. To get around this
	# deltaTimeAccumulator is used to figure out how many steps must be taken.
	# from: http://www.panda3d.org/wiki/index.php/Simulating_the_Physics_World
	
	# http://www.panda3d.org/apiref.php?page=ClockObject
	deltaTimeAccumulator += globalClock.getDt()
	
	# Add the deltaTime for the task to the accumulator
	while deltaTimeAccumulator > stepSize:
		deltaTimeAccumulator -= stepSize
		world.quickStep( stepSize )
	
	# Set the new position
	boxModel.setPos(render, boxBody.getPosition())
	boxModel.setQuat(render, Quat(boxBody.getQuaternion() ) )
	
	# Clear the contact joints
	contactgroup.empty()
	
	return task.cont

# http://www.panda3d.org/apiref.php?page=TaskManager#doMethodLater
taskMgr.doMethodLater(delayTime = 0.2,
	funcOrTask = simulationTask,
	name = "Physics Simulation")

helpText = OnscreenText(
	text = "Turn gravity [SPACE]",
	style = 1,
	fg = (1,1,1,1),
	pos = (-1.25,0.85),
	align = TextNode.ALeft,
	scale = 0.07
)
helpText.show()

def turnGravity():
	g = world.getGravity()
	g = -g
	world.setGravity( g )

def hitBoxLeft():
	boxBody.setForce( 0, -30000, 10000 )

def hitBoxRight():
	boxBody.setForce( 0, 30000, 10000 )

base.accept("space", turnGravity )
base.accept("a", hitBoxLeft )
base.accept("d", hitBoxRight )

run()