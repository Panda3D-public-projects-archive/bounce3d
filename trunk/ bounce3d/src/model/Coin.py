
from pandac.PandaModules import (
	Quat,OdeBody, OdeMass, OdeBoxGeom, BitMask32)
	
class Coin:
    """
    An object that a ball collects.
    """
    
    collectable = 0
    
    def __init__(self, world, space, pos):
	    Coin.collectable += 1
            self.world = world
            self.space = space
            self.addBox(pos)
            
            self.isCollected = False
    
    def collect(self):
            if not self.isCollected:
                    self.isCollected = True
                    self.box.setColor(1,0,0)
		    Coin.collectable -= 1
            
    def addBox(self, pos):
            
            lx,ly,lz = 1,1,1   # dimension
            px,py,pz = pos # position
            
            self.box = loader.loadModel("box")
            self.box.setPos(-0.5,-0.5,-0.5)
            self.box.flattenLight() # ApplyTransform
            self.box.reparentTo(render)
            
            # Make sure its center is at 0, 0, 0 like OdeBoxGeom
            self.box.setPos( px -lx/2, py -ly/2, pz -lz/2)
            self.box.setScale( lx, ly, lz )
            self.box.setHpr( 0, 50, 0 )
            
            # define mass
            mass = OdeMass()
            mass.setBox( 500, lx, ly, lz)
            
            self.boxBody = OdeBody( self.world )
            self.boxBody.setPosition( self.box.getPos(render) )
            self.boxBody.setQuaternion( self.box.getQuat(render) )
            self.boxBody.setMass( mass )
            
            geom = OdeBoxGeom( self.space, lx, ly, lz)
            geom.setBody( self.boxBody )
            
    def updateModelNode(self):
            self.box.setPos( render, self.boxBody.getPosition() )
            self.box.setQuat(render, Quat(self.boxBody.getQuaternion() ) )
            
    def getBody(self):
            return self.boxBody
    
    def removeNode(self):
	    if not self.isCollected:
		Coin.collectable -= 1
	    self.box.removeNode()
    
