
from pandac.PandaModules import Vec4

# lights
from pandac.PandaModules import AmbientLight
from pandac.PandaModules import DirectionalLight

class GameView:
	def __init__(self, engine):
		self.engine = engine
		
		self.engine.disableMouse()
		self.engine.camera.lookAt(0, 0, 6)
		self.engine.setBackgroundColor(0,0.3,0.5)
		self.engine.camera.setPos(40, 0, 2)
		self.setLights()
		
	def setLights(self):
		# Ambient Light
		ambientLight = AmbientLight( 'ambientLight' )
		ambientLight.setColor( Vec4( 0.1, 0.1, 0.1, 1 ) )
		ambientLightNP = render.attachNewNode( ambientLight.upcastToPandaNode() )
		render.setLight(ambientLightNP)

		# Directional light 01
		directionalLight = DirectionalLight( "directionalLight" )
		directionalLight.setColor( Vec4( 1, 1, 1, 1 ) )
		directionalLightNP = render.attachNewNode( directionalLight.upcastToPandaNode() )
		directionalLightNP.setPos(10,-20,20)
		directionalLightNP.lookAt(0,0,0)
		render.setLight(directionalLightNP)

		# Directional light 02
		directionalLight = DirectionalLight( "directionalLight" )
		directionalLight.setColor( Vec4( 1, 1, 1, 1 ) )
		directionalLightNP = render.attachNewNode( directionalLight.upcastToPandaNode() )
		directionalLightNP.lookAt(0,0,0)
		directionalLightNP.setPos(10,20,20)
		render.setLight(directionalLightNP)
		
		