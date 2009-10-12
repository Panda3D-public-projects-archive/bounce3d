from direct.directbase import DirectStart
from direct.task import Task
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

#class Kontrollit(DirectObject):

# Physical world
world = OdeWorld()
world.setGravity(0, 0, -9.81)
 
# Surface
world.initSurfaceTable(1)
world.setSurfaceEntry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)

# Space/contactgroup
space = OdeSimpleSpace()
space.setAutoCollideWorld(world)
contactgroup = OdeJointGroup()
space.setAutoCollideJointGroup(contactgroup)
 
# Obj model
obj = loader.loadModel("egg/paahahmo")
obj.setPos(0,0,0)
obj.setScale(1,1,1)



# 		Physx
objNP = obj.copyTo(render)
objNP.setPos(0,0,5)
# Body and mass
objBody = OdeBody(world)
M = OdeMass()
M.setSphereTotal(5, 1)
objBody.setMass(M)
objBody.setPosition(objNP.getPos(render))
objBody.setQuaternion(objNP.getQuat(render))
# ObjGeom
objGeom = OdeSphereGeom(space, 1)
objGeom.setCollideBits(BitMask32(0x00000002))
objGeom.setCategoryBits(BitMask32(0x00000001))
objGeom.setBody(objBody)

#-----------------------------------------------
#Kentan orientaatio
tasoHpr = VBase3(0, 0, 0)

tasoCollideHpr = VBase3(0,0,0)
tasoCollideHpr.setX(tasoHpr.getX()+90)
tasoCollideHpr.setY(-tasoHpr.getY())
tasoCollideHpr.setZ(-tasoHpr.getZ())

tasoCollideScale = VBase3(1, 1, 1)

# Obj taso
taso = loader.loadModel("egg/testimaa")
taso.reparentTo(render)
taso.setPos(0,0,0)
taso.setScale(1,1,1)
taso.setHpr(tasoHpr)

# Collision plane
matriisi = Mat3()

composeMatrix(matriisi, tasoCollideScale, tasoCollideHpr)
modelTrimesh = OdeTriMeshData(taso, True)
modelGeom = OdeTriMeshGeom(space, modelTrimesh)
modelGeom.setRotation(matriisi)
#-----------------------------------------------

# Set the camera position
base.disableMouse()
base.camera.setPos(30,0,0.1)
base.camera.lookAt(0,0,2)

# Simulation task	
def simulationTask(task):
  space.autoCollide()
  world.quickStep(globalClock.getDt())
  objNP.setPosQuat(render, objGeom.getPosition(), Quat(objGeom.getQuaternion()))
  contactgroup.empty()
  return task.cont
 
taskMgr.doMethodLater(1, simulationTask, "Physics Simulation")
#taskMgr.add( __init__, "Testi")


# Valot

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

run()