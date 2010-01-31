
from direct.task import Task

class GameLoop:
	''' Game Loop on eras kontrolli '''

	def __init__(self, model):
		self.model = model

	def simulationTask(self, hud):
		''' contains the main loop '''

		# Setup the contact joints
		self.model.space.autoCollide()

		dt = globalClock.getDt()
		self.model.world.quickStep( dt )

		self.model.updateObjects()

		# Clear the contact joints
		self.model.contactgroup.empty()
		hud.updateHUD()
		return Task.cont
