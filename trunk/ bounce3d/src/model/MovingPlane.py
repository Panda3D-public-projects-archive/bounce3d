
from pandac.PandaModules import (
        Quat,OdeBody, OdeMass, OdeBoxGeom, BitMask32)
from math import sin

class MovingPlane:
        ''' moving plane '''
        id = 0
        
        def __init__(self, space, pos, dim):
		''' Hauska Bugi: kirjoita 1.0 eika 1 '''
                MovingPlane.id += 1
                self.id = id
                self.dim = dim # dimension
                self.pos = pos # position
                self.h = ( dim[0]/2, dim[1]/2, dim[2]/2 )
                self.t = 0

                self.geom = OdeBoxGeom( space, dim[0], dim[1], dim[2])

                self.model = loader.loadModel("box")
                self.model.setScale( dim[0], dim[1], dim[2] )
                self.model.flattenLight()
                self.model.reparentTo(render)

                self.updateModelNode()

        def updateModelNode(self):
                self.t = self.t + 0.03
                pos = self.pos
                h = self.h

                rot = pos[2] + sin( self.t )

                self.geom.setPosition( pos[0], pos[1], rot)
                self.model.setPos(pos[0]-h[0], pos[1]-h[1], rot-h[2])

	def getId(self):
		return id;
	
	def getGeom(self):
		return self.geom