
class EventType:
	PLAYER_MOVE_RIGHT_ON  = "Player Move Right On"
	PLAYER_MOVE_RIGHT_OFF = "Player Move Right Off"
	PLAYER_MOVE_LEFT_ON   = "Player Move Left On"
	PLAYER_MOVE_LEFT_OFF  = "Player Move Left Off"
	PLAYER_JUMP_ON        = "Player Jump On"
	PLAYER_JUMP_OFF       = "Player Jump Off"
	
	RESTART    = 0x123123
	NEXT_LEVEL = 0x453453
	UPDATE_HUD = 0xa34434
	MENU = 0x0000ff
	CONTROL_CHANGE = 0x00ff00
	CONTROL_HIDE = 0xff0000
	MENU_HS = 0x0f0f0f
	EXIT = 0xff00ff
	BR_MENU = 0x1295ff
	INFO_M = 0x1295fe
	
	ODE_COLLISION = "ode-collision"