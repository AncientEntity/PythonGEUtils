from gameengine.engine import *
import time

sprites = [pygame.image.load("flappy.png"),pygame.image.load("background.png")]
sprites.append(pygame.image.load("ground.png"))
sprites.append(pygame.image.load("pipe.png"))
sprites.append(pygame.image.load("panel.png"))

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
componentMaster.append(PlayerController(None))
#END OF COMPONENTS

game = GameObject("Game")
game.AddComponent("PLAYERCONTROLLER")
mainScene.AddObject(CloneGameObject(game))

block = GameObject("Button")
#block.AddComponent("RENDERER")
block.AddComponent("UIBUTTON")
block.DirectComponent("UIBUTTON").sprite = 4
block.DirectComponent("UIBUTTON").functions.append("self.parent.Destroy()")
block.scale = [5,5]

blockPrefab = Prefab("Block",block)



#SCENE SETUP
for x in range(12):
	for y in range(12):
		new = blockPrefab.CreateInstance([x*50+25,y*50+25],0,[5,5])
		mainScene.AddObject(new)




scenes.append(mainScene)
game = gameengine.engine.GameInfo("Game Test 1", {"RESOLUTION":(600,600),"GRAVITY":-0.028,"KEYREPEAT":(0,0)},componentMaster,scenes,0,sprites)

LaunchGame(game)
