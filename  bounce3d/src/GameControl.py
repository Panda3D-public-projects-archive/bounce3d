
from direct.task import Task

class GameControl:
	''' Game Loop on eras kontrolli '''

	def __init__(self, fps, model):
		# Simulaation kaytetty aika
		self.simTime = 0.0
		# frame time in seconds
		self.stepSize = 1.0 / fps
		self.model = model

	def simulationTask(self, task):
		''' contains the main loop '''
		
		model = self.model
		
		# Setup the contact joints
		model.space.autoCollide()
		
		# http://www.panda3d.org/apiref.php?page=ClockObject
		self.simTime += globalClock.getDt()
		
		while self.simTime > self.stepSize:
			self.simTime -= self.stepSize
			model.world.quickStep( self.stepSize )
		
		#
		model.updateObjects()
		
		# Clear the contact joints
		model.contactgroup.empty()
		
		return Task.cont