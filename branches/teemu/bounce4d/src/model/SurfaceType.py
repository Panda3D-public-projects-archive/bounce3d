
class SurfaceType:
	
	BALL  = 0x0
	COIN  = 0x1
	FLOOR = 0x2
	SAND  = 0x3
	#ICE   = 0x4
	
	def load(self, world):
		'''
			Tutorials:
			http://www.panda3d.org/apiref.php?page=OdeWorld#setSurfaceEntry
			http://www.panda3d.org/wiki/index.php/Collision_Detection_with_ODE
		'''
		world.initSurfaceTable(num_surfaces = 4)

		mu = 0.8
		bounce = 0.0
		bounce_vel = 9.1
		soft_erp = 0.9
		soft_cfm = 0.00001
		slip = 100.0
		dampen = 0.002
		
		world.setSurfaceEntry(SurfaceType.BALL, SurfaceType.COIN,
			mu, bounce, bounce_vel, soft_erp, soft_cfm, slip, dampen)
		world.setSurfaceEntry(SurfaceType.BALL, SurfaceType.FLOOR,
			mu, bounce, bounce_vel, soft_erp, soft_cfm, slip, dampen)
		world.setSurfaceEntry(SurfaceType.BALL, SurfaceType.SAND,
			1.0, bounce, bounce_vel, 0.0, soft_cfm, 0.0, 0.0)			
		
		world.setSurfaceEntry(SurfaceType.COIN, SurfaceType.COIN,
			mu, bounce, bounce_vel, soft_erp, soft_cfm, slip, dampen)
		world.setSurfaceEntry(SurfaceType.COIN, SurfaceType.FLOOR,
			mu, bounce, bounce_vel, soft_erp, soft_cfm, slip, dampen)
		world.setSurfaceEntry(SurfaceType.COIN, SurfaceType.SAND,
			mu, bounce, bounce_vel, soft_erp, soft_cfm, slip, dampen)