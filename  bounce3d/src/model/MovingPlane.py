
from pandac.PandaModules import (
	Quat,OdeBody, OdeMass, OdeBoxGeom, BitMask32)

class MovingPlane:
	def __init__(self, space, pos):
		# Hauska Bugi: kirjoita 1.0 eika 1
		lx,ly,lz = 5,5,1.0   # dimension
		px,py,pz = pos # position
	
		self.ground = loader.loadModel("box")		
		self.ground.setScale( lx, ly, lz )
		self.ground.setPos( px -lx/2, py -ly/2, pz -lz/2)
		
		self.ground.flattenLight()
		self.ground.reparentTo(render)

		geom = OdeBoxGeom( space, lx, ly, lz)
		geom.setPosition( px, py, pz)

	