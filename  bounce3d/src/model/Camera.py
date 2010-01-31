
# http://www.panda3d.org/apiref.php?page=TaskManager
from direct.task import Task

class Camera:
	def __init__(self, base, ball):
		self.camera = base.camera
		self.angle = 0
		self.dir = 8
		self.turning = False
		self.ball = ball
		
	def updateModelNode(self):
		x,y,z = self.ball.getPosition()
		self.camera.lookAt( x,y,z + 3 )
		h,p,r = self.camera.getHpr()
		self.camera.setHpr(h,p, self.angle)
		cx,cy,cz = self.camera.getPos()
		self.camera.setPos( cx, y, z*0.75 ) # alter only y-axis
	
	# http://www.panda3d.org/wiki/index.php/Controlling_the_Camera
	def turnCameraTask(self, task):
		self.angle += self.dir
		if (self.angle >= 180):
			self.angle = 180
			self.dir = -self.dir
			self.turning = False
			return Task.done
		elif(self.angle <= 0):
			self.angle = 0
			self.dir = -self.dir
			self.turning = False
			return Task.done
		else:
			return Task.cont
	
	def turn(self):
		if( not self.turning ):
			taskMgr.add(self.turnCameraTask, "TurnCameraTask")
			self.turning = True
	