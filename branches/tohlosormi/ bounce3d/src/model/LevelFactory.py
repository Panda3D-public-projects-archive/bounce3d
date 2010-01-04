
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
			level.ball.setPosition( (0.0,-20.0,10.0) )
			level.addExit( (0.0, 60.0, 7.0) )
			level.loadLevelEntity( self.MODEL_EGG[mapNo], self.COLLISION_EGG[mapNo] )
			
		elif (mapNo == 1):
			level.ball.setPosition( (0.0,-20.0,10.0) )
			level.addExit( (0.0,60.0,7.0) )
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
		