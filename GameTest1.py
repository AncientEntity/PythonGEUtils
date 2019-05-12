from gameengine.engine import *
import time

#COMPONENTS MADE

class ToMouseTest(BaseComponent):
    def __init__(self,s):
        self.parent = s
        self.name = "TOMOUSETEST"
        self.requiresStart = False
        self.offset = [0,0]
    def CreateNew(self,s):
        return ToMouseTest(s)
    def Update(self):
        self.parent.position = [pygame.mouse.get_pos()[0] + self.offset[0],pygame.mouse.get_pos()[1]+self.offset[1]]
class BoxController(BaseComponent):
	def __init__(self,s):
		self.parent = s
		self.name = "BOXCONTROLLER"
		self.requiresStart = False
	def CreateNew(self,s):
		return BoxController(s)
	def Update(self):
		global curScene
		for event in self.events:
			if(event.type == pygame.KEYDOWN):
				if(event.key == pygame.K_UP):
					self.parent.components[self.parent.GetComponent("RIGIDBODY")].velocity[1] += 2
				elif(event.key == pygame.K_LEFT):
					self.parent.position[0] -= 5
				elif(event.key == pygame.K_RIGHT):
					self.parent.position[0] += 5


componentMaster.append(BoxController(None))
componentMaster.append(ToMouseTest(None))


#COMPONENTS OVER

scenes = []

SceneOne = Scene("Scene One",[])
scenes.append(SceneOne)

background = GameObject("Back")
background.AddComponent("RENDERER")
background.position = [-25,0]
background.components[background.GetComponent("RENDERER")].sprite = pygame.image.load("background.png")
background.components[background.GetComponent("RENDERER")].sortingLayer = -10
background.scale = [4,4]
SceneOne.AddObject(background)

obj2 = GameObject("Falling Object Prefab")
obj2.AddComponent("RENDERER")
obj2.AddComponent("RIGIDBODY")
obj2.AddComponent("COLLIDER")
obj2.position = [150,85]
obj2.scale = [1,1]
obj2.components[obj2.GetComponent("RENDERER")].sprite = pygame.image.load("redbox.png")
obj2.components[obj2.GetComponent("RENDERER")].sortingLayer = 10
obj2.components[obj2.GetComponent("RIGIDBODY")].locked = False
obj2.components[obj2.GetComponent("COLLIDER")].SetAsImage()
fallingObjectPrefab = Prefab("Falling Object",obj2)

SceneOne.AddObject(fallingObjectPrefab.CreateInstance([100,100],0,[1,1]))
SceneOne.AddObject(fallingObjectPrefab.CreateInstance([200,450],0,[1,1]))
SceneOne.AddObject(fallingObjectPrefab.CreateInstance([400,100],0,[1,1]))

boxC = fallingObjectPrefab.CreateInstance([550,100],0,[1,1])
boxC.AddComponent("BOXCONTROLLER")
boxC.components[boxC.GetComponent("RENDERER")].sprite = pygame.image.load("error.png")
SceneOne.AddObject(boxC)

obj4 = GameObject("Ground")
obj4.AddComponent("RENDERER")
obj4.AddComponent("RIGIDBODY")
obj4.AddComponent("COLLIDER")
obj4.position = [0,500]
obj4.scale = [30,7]
obj4.components[obj4.GetComponent("RENDERER")].sprite = pygame.image.load("ground.png")
obj4.components[obj4.GetComponent("RENDERER")].sortingLayer = 5
obj4.components[obj4.GetComponent("RIGIDBODY")].locked = True
obj4.components[obj4.GetComponent("COLLIDER")].SetAsImage()
print(obj4.components[obj4.GetComponent("COLLIDER")].size)
SceneOne.AddObject(obj4)

SceneTwo = Scene("Scene Two", [])
SceneTwo.AddObject(boxC)
scenes.append(SceneTwo)


game = gameengine.engine.GameInfo("Game Test 1", {"RESOLUTION":(800,600),"GRAVITY":-0.03,"KEYREPEAT":(50,50)},componentMaster,scenes,0)

LaunchGame(game)
