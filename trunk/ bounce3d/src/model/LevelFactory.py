
from model.MovingPlane import MovingPlane
from model.SurfaceType import SurfaceType
from model.Coin import Coin

class LevelFactory:
	'''
		Hiukan kesken
		Parempi tapa olisi ladata kentta dynaamisesti
		erillisesta tiedosta
	'''
	
	def __init__(self):
		pass
		
	def load( self, level, number ):
		'''represents currently level 2'''
		
		ball = level.ball
		planes = level.planes
		coins = level.coins
		world = level.world
		s = level.space

		''' Testing Level '''
		y = 0.0
		
		ball.setPosition( (y, 1.0,1.0) )
		
		dim = (2.0, 5.0, 0.5)
		plane = MovingPlane( s, (y,0.0,5.0),   dim )
		plane.rotate = True
		planes.append( plane )
		
		for x in xrange(1,5):
			planes.append( MovingPlane( s, (y, 5.0*x, 5.0*x), dim ) )
		
		floor = 0.0
		ceiling = 20.0
		for x in xrange(0,5):
			planes.append( MovingPlane( s, (y, 5.0*x, floor), dim, SurfaceType.SAND ) )
			planes.append( MovingPlane( s, (y, 5.0*x, ceiling), dim ) )

		# Walls
		for z in xrange(1, 4):
			planes.append( MovingPlane( s, (y, -2.5, 5.0*z), (2.0, 0.5, 2) ) )
			planes.append( MovingPlane( s, (y, 20.0, 5.0*z), (2.0, 0.5, 2) ) )
			
		coins.append( Coin(world, s, (y,5.0,15.0) ) )
		coins.append( Coin(world, s, (y,10.0,17.0) ) )
		
		# http://www.panda3d.org/apiref.php?page=NodePath
		
		# we will not update exit, it remains static
		level.exit.setPosition( (y, 10.0, 18.0) )
		
		#base.accept('open_door', triggerEvent )
		#messenger.send('open_door')