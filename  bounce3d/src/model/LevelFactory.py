
from model.SurfaceType import SurfaceType	

class LevelFactory:
	'''
		Jokaisen tason tiedot voitaisiin ladata erillisesta tiedostosta.
		http://www.panda3d.org/apiref.php?page=NodePath
	'''
	MODEL_EGG =[
		"../egg/level0_1_visual.egg",
		"../egg/level0_2_visual.egg",
		"../egg/level0_3_visual.egg" ]
	
	COLLISION_EGG =[
		"../egg/level0_1_collision.egg",
		"../egg/level0_2_collision.egg",
		"../egg/level0_3_collision.egg"]

	def __init__(self):
		pass
		
	def load( self, level, mapNo ):
		if(mapNo == 0):
			level.ball.limitYMovement(-33.0,162.0)
			level.ball.limitZMovement(-30.0,50.0)
			level.ball.setPosition( (0.0,-20.0,10.0) )
			level.addCoin( (0.0, -5.1, 4.9) )
			level.addCoin( (0.0, 10.0, 3.1) )
			level.addCoin( (0.0, 32.1, 2.1) )
			level.addCoin( (0.0, 35.7, 5.1) )
			level.addCoin( (0.0, 31.5, 9.2) )
			level.addCoin( (0.0, 38.4, 17.1) )
			level.addCoin( (0.0, 43.7, 1.9) )
			level.addCoin( (0.0, 58.0, 1.9) )
			level.addCoin( (0.0, 66.3, 6.0) )
			level.addCoin( (0.0, 55.8, 7.2) )
			level.addCoin( (0.0, 90.9, 4.0) )
			level.addCoin( (0.0, 130.8, 7.4) )
			level.addCoin( (0.0, 152.1, 4.1) )
			level.addExit( (0.0, 156.0, 9.4) )
			level.loadLevelEntity( self.MODEL_EGG[mapNo], self.COLLISION_EGG[mapNo] )

		elif (mapNo == 1):
			level.ball.limitYMovement(-28.0,432.0)
			level.ball.limitZMovement(-290.0,50.0)
			level.ball.setPosition( (0.0,-20.0,10.0) )
			level.addCoin( (0.0, 18.4, .5) )
			level.addCoin( (0.0, 69.6, -29.2) )
			level.addCoin( (0.0, 152.3, -95.1) )
			level.addCoin( (0.0, 185.9, -96.1) )
			level.addCoin( (0.0, 263.9, -173.0) )
			level.addCoin( (0.0, 309.0, -209.2) )
			level.addCoin( (0.0, 373.0, -223.7) )
			level.addExit( (0.0, 414.1, -222.2) )
			level.loadLevelEntity( self.MODEL_EGG[mapNo], self.COLLISION_EGG[mapNo] )
			
		elif(mapNo == 2):
			self._TestLevel(level)
		else:
			raise Error
			
	def _TestLevel(self, level):
		level.ball.setPosition( (0.0, 1.0, 1.0) )
		
		dim = (2.0, 5.0, 0.5)
		
		for x in xrange(1,5):
			level.addPlane( (0.0, 5.0*x, 5.0*x), dim, SurfaceType.FLOOR ) # steps
		
		for x in xrange(0,5):
			level.addPlane( (0.0, 5.0*x, 0.0), dim, SurfaceType.SAND ) # floor
			level.addPlane( (0.0, 5.0*x, 20.0), dim, SurfaceType.FLOOR ) # ceiling

		dim = (2.0, 0.6, 3)
		
		for z in xrange(0, 5):
			level.addPlane( (0.0, -3.0, 5.0*z), dim, SurfaceType.FLOOR ) # left wall
			level.addPlane( (0.0, 23.0, 5.0*z), dim, SurfaceType.FLOOR ) # right wall
			
		level.addCoin( (0.0, 5.0, 15.0 ) )
		level.addCoin( (0.0, 10.0, 17.0 ) )
		
		level.addExit( (0.0, 14.0, 18.0) )
		
		level.addTrigger( 'TriggerBallNode', (0.0, 8.0, 2.0), 1.0 )
		
		level.onTrigger = level.onTrigger
		