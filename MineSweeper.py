from gameengine.engine import *
import time
import random

sprites = [pygame.image.load("flappy.png"),pygame.image.load("background.png")]
sprites.append(pygame.image.load("ground.png"))
sprites.append(pygame.image.load("pipe.png"))
sprites.append(pygame.image.load("panel.png"))
sprites.append(pygame.image.load("bomb.png"))

scenes = []
mainScene = Scene("Main Scene",[])

#COMPONENTS
class PlayerController(BaseComponent):
	def __init__(self,s):
		self.parent = s
		self.name = "PLAYERCONTROLLER"
		self.requiresStart = True
	def CreateNew(self,s):
		return PlayerController(s)
	def Start(self):
		global objects
	def Update(self):
		pass
class Block(BaseComponent):
	def __init__(self,s):
		self.parent = s
		self.name = "BLOCK"
		self.requiresStart = True
	def CreateNew(self,s):
		return Block(s)
	def Start(self):
		global objects
	def Update(self):
		pass
	def CheckBombCount(self):
		near = self.parent.DirectComponent("COLLIDER").CollisionBox([150,150],[-75,-75])
		bombCount = 0
		for x in near:
			if(x.type == "BOMB"):
				bombCount += 1
		return str(bombCount)


componentMaster.append(PlayerController(None))
componentMaster.append(Block(None))
#END OF COMPONENTS

game = GameObject("Game")
game.AddComponent("PLAYERCONTROLLER")
mainScene.AddObject(CloneGameObject(game))



block = GameObject("Button")
#block.AddComponent("RENDERER")
block.AddComponent("COLLIDER")
block.AddComponent("UIBUTTON")
block.AddComponent("BLOCK")
block.AddComponent("UITEXT")
block.DirectComponent("UITEXT").text = ""
block.DirectComponent("UITEXT").size = 18
block.DirectComponent("UIBUTTON").sprite = 4
block.scale = [5,5]

blockPrefab = Prefab("Block",block)


#SCENE SETUP
for x in range(12):
	for y in range(12):
		new = blockPrefab.CreateInstance([x*50+25,y*50+25],0,[5,5])
		r = random.randint(0,20)
		if(r <= 4):
			new.type = "BOMB"
			new.DirectComponent("UIBUTTON").functions.append("self.parent.DirectComponent(\"UIBUTTON\").sprite = 5")
		else:
			new.type = "SPOT"
			new.DirectComponent("UIBUTTON").functions.append("self.parent.DirectComponent(\"UITEXT\").text = self.parent.DirectComponent(\"BLOCK\").CheckBombCount()")
			new.DirectComponent("UITEXT").offset = [-85,-95]
		mainScene.AddObject(new)



scenes.append(mainScene)
game = gameengine.engine.GameInfo("Game Test 1", {"RESOLUTION":(600,600),"GRAVITY":-0.028,"KEYREPEAT":(0,0)},componentMaster,scenes,0,sprites)

LaunchGame(game)
