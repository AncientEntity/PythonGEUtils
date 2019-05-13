from gameengine.engine import *
import time

scenes = []
flappyScene = Scene("Flappy Scene",[])

#COMPONENTS
class PlayerController(BaseComponent):
    def __init__(self,s):
        self.parent = s
        self.name = "PLAYERCONTROLLER"
        self.requiresStart = False
        self.points = 0
        self.pipeIn = 0
    def CreateNew(self,s):
        return PlayerController(s)
    def Update(self):
    	for event in self.events:
    		if(event.type == pygame.KEYDOWN):
    			if(event.key == pygame.K_SPACE):
    				self.parent.components[self.parent.GetComponent("RIGIDBODY")].velocity[1] = 1
    	#Check for lose
    	for obj in self.parent.components[self.parent.GetComponent("COLLIDER")].collidingWith:
    		if(obj.tag == "death"):
    			GetObjectByTag("scoring").components[GetObjectByTag("scoring").GetComponent("UITEXT")].text = ("You Lose With " +str(self.points) + " points.")
    			
    			for obj in GetObjectsByTag("death"):
    				if(obj.name == "Ground"):
    					continue
    				obj.Destroy()

    			GetObjectByName("SadFace").active = True

    			self.parent.Destroy()


    		elif(obj.tag == "flag"):
    			self.points += 1
    			obj.Destroy()
    	#Spawn Pipes
    	self.pipeIn -= 0.01
    	#print(self.pipeIn)
    	if(self.pipeIn < 0):
    		self.pipeIn = 1.5
    		GetObjectByTag("scoring").components[GetObjectByTag("scoring").GetComponent("UITEXT")].text = str(self.points)
    		CreatePipe()
componentMaster.append(PlayerController(None))
#END OF COMPONENTS



#PREFAB
scoreText = GameObject("ScoreText")
scoreText.AddComponent("UITEXT")
scoreText.components[scoreText.GetComponent("UITEXT")].text = "0"
scoreText.components[scoreText.GetComponent("UITEXT")].centered = True
scoreText.tag = "scoring"
scoreText.position = [400,100]

sadFace = GameObject("SadFace")
sadFace.AddComponent("UITEXT")
sadFace.components[sadFace.GetComponent("UITEXT")].text = ":("
sadFace.components[sadFace.GetComponent("UITEXT")].centered = True
sadFace.components[sadFace.GetComponent("UITEXT")].size = 80
sadFace.tag = "sadFace"
sadFace.position = [400,175]
sadFace.active = False

flappy = GameObject("Flappy")
flappy.position = [200,250]
flappy.tag = "player"
flappy.AddComponent("RENDERER")
flappy.AddComponent("COLLIDER")
flappy.AddComponent("RIGIDBODY")
flappy.AddComponent("PLAYERCONTROLLER")
flappy.scale = [2,2]
flappy.components[flappy.GetComponent("RENDERER")].sprite = pygame.image.load("flappy.png")
flappy.components[flappy.GetComponent("COLLIDER")].SetAsImage()
flappy.components[flappy.GetComponent("RIGIDBODY")].lockedX = True
flappy.components[flappy.GetComponent("COLLIDER")].trigger = True
#flappy.components[flappy.GetComponent("PLAYERCONTROLLER")].scoreText = scoreText
bird = Prefab("Flappy Bird",flappy)

pipe = GameObject("Pipe")
pipe.position = [600,0]
pipe.AddComponent("RENDERER")
pipe.AddComponent("COLLIDER")
pipe.AddComponent("RIGIDBODY")
pipe.AddComponent("CONSTANTMOVEMENT")
pipe.components[pipe.GetComponent("RENDERER")].sprite = pygame.image.load("pipe.png")
pipe.components[pipe.GetComponent("COLLIDER")].size = [40,212]
pipe.components[pipe.GetComponent("RIGIDBODY")].lockedY = True
pipe.components[pipe.GetComponent("COLLIDER")].trigger = True
pipe.components[pipe.GetComponent("CONSTANTMOVEMENT")].constantVelocity = [1.5,0]
pipe.tag = "death"
pipePrefab = Prefab("Pipe Prefab",pipe)

ground = GameObject("Ground")
ground.AddComponent("RENDERER")
ground.AddComponent("RIGIDBODY")
ground.AddComponent("COLLIDER")
ground.tag = "death" 
ground.position = [0,500]
ground.scale = [1,1]
ground.components[ground.GetComponent("RENDERER")].sprite = pygame.image.load("ground.png")
ground.components[ground.GetComponent("RENDERER")].sortingLayer = 5
ground.components[ground.GetComponent("RIGIDBODY")].lockedY = True
ground.components[ground.GetComponent("COLLIDER")].trigger = True
ground.components[ground.GetComponent("COLLIDER")].SetAsImage()
groundPrefab = Prefab("Ground",ground)


#END OF PREFABS

def CreatePipe():
	offset = random.randint(-130,130)
	flappyScene.AddObject(pipePrefab.CreateInstance([900,0+offset],0,[1,1]))
	flappyScene.AddObject(pipePrefab.CreateInstance([900,380+offset],180 ,[1,1]))
	flag = GameObject("PIPE FLAG")
	flag.tag = "flag"
	flag.position = [900,216+offset]
	flag.AddComponent("COLLIDER")
	flag.components[flag.GetComponent("COLLIDER")].size = [40,164]
	flag.AddComponent("RIGIDBODY")
	flag.components[flag.GetComponent("RIGIDBODY")].lockedY = True
	flag.components[flag.GetComponent("COLLIDER")].trigger = True
	flag.AddComponent("CONSTANTMOVEMENT")
	flag.components[flag.GetComponent("CONSTANTMOVEMENT")].constantVelocity = [1.5,0]

	flappyScene.AddObject(flag)


#SCENE SETUP
flappyScene.AddObject(bird.CreateInstance([200,300],0,[2,2]))
g = groundPrefab.CreateInstance([0,500],0,[30,7])
g.components[ground.GetComponent("COLLIDER")].SetAsImage()
flappyScene.AddObject(g)
flappyScene.AddObject(scoreText)
flappyScene.AddObject(sadFace)
#CreatePipe()


#SCENE END


scenes.append(flappyScene)
game = gameengine.engine.GameInfo("Game Test 1", {"RESOLUTION":(800,600),"GRAVITY":-0.012,"KEYREPEAT":(0,0)},componentMaster,scenes,0)

LaunchGame(game)
