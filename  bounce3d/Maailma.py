from direct.directbase import DirectStart
from direct.task.Task import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import *

import Kontrollit

class Maailma(DirectObject):

   def __init__(self):
   
      self.Kontrollit = Kontrollit.Kontrollit()
      space,world,objNP,objGeom, contactgroup = self.alustusTask()
      taskMgr.doMethodLater(1,self.simulationTask,
		"Simulation", extraArgs=[space,world,objNP,objGeom,contactgroup])

   def alustusTask(task):
   
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
      obj = loader.loadModel("models/smiley.egg")
      obj.setPos(0,0,0)
      obj.setScale(1,1,1)

      #    Phys
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
      
      # Collision plane
      cm = CardMaker("ground")
      cm.setFrame(-20, 20, -20, 20)
      ground = render.attachNewNode(cm.generate())
      ground.setPos(0, 0, 0); ground.lookAt(0, 0, -1)
      groundGeom = OdePlaneGeom(space, Vec4(0, 0, 1, 0))
      groundGeom.setCollideBits(BitMask32(0x00000001))
      groundGeom.setCategoryBits(BitMask32(0x00000002))
      
      # Set the camera position
      base.disableMouse()
      base.camera.setPos(30,0,0.1)
      base.camera.lookAt(0,0,2)
      
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
      
      return space, world, objNP, objGeom, contactgroup
   
   def simulationTask(task, space, world, objNP, objGeom, contactgroup):
      
      space.autoCollide()
      world.quickStep(globalClock.getDt())
      objNP.setPosQuat(render, objGeom.getPosition(), Quat(objGeom.getQuaternion()))
      contactgroup.empty()
      
      return Task.cont
   
m = Maailma()
run()