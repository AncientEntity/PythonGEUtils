from gameengine.engine import *
import time

#COMPONENTS MADE

class BoxController(BaseComponent):
	def __init__(self,s):
		self.parent = s
		self.name = "BOXCONTROLLER"
		self.requiresStart = False
		self.alive = True
	def CreateNew(self,s):
		return BoxController(s)
	def Update(self):
	    global curScene
	    if(self.alive == False):
	        return False
	    for obj in self.parent.components[self.parent.GetComponent("COLLIDER")].collidingWith:
		    if(obj.tag == "enemy"):
		        self.alive = False
		        self.parent.RemoveComponent("RENDERER")
	    for event in self.events:
		    if(event.type == pygame.KEYDOWN):
		    	if(event.key == pygame.K_UP):
		    		self.parent.position[1] -= 5
		    	elif(event.key == pygame.K_LEFT):
		    		self.parent.position[0] -= 5
		    	elif(event.key == pygame.K_RIGHT):
		    		self.parent.position[0] += 5
		    	elif(event.key == pygame.K_DOWN):
		    		self.parent.position[1] += 5


class EnemyController(BaseComponent):
	def __init__(self,s):
		self.parent = s
		self.name = "ENEMY"
		self.requiresStart = False
	def CreateNew(self,s):
		return EnemyController(s)
	def Update(self):
                if(self.parent.position[0] < -85):
                    self.parent.position[0] = 720
                elif(self.parent.position[0] > 740):
                	self.parent.position[0] = -45
                #print(self.parent.position[0])


componentMaster.append(BoxController(None))
componentMaster.append(EnemyController(None))


#COMPONENTS OVER

sprites = [pygame.image.load("background.png"),pygame.image.load("redbox.png"),pygame.image.load(errorImage),pygame.image.load("ground.png")]
scenes = []

SceneOne = Scene("Scene One",[])
scenes.append(SceneOne)

background = GameObject("Back")
background.AddComponent("RENDERER")
background.position = [-25,0]
background.components[background.GetComponent("RENDERER")].sprite = 0
background.components[background.GetComponent("RENDERER")].sortingLayer = -10
background.scale = [4,4]
SceneOne.AddObject(background)

obj2 = GameObject("Enemy Prefab")
obj2.AddComponent("RENDERER")
obj2.AddComponent("RIGIDBODY")
obj2.AddComponent("COLLIDER")
obj2.AddComponent("ENEMY")
obj2.position = [150,85]
obj2.scale = [1,1]
obj2.components[obj2.GetComponent("RENDERER")].sprite = 1
obj2.components[obj2.GetComponent("RENDERER")].sortingLayer = 10
obj2.components[obj2.GetComponent("RIGIDBODY")].lockedY = False
obj2.components[obj2.GetComponent("COLLIDER")].SetAsImage(sprites[1])
obj2.components[obj2.GetComponent("COLLIDER")].trigger = True
obj2.AddComponent("CONSTANTMOVEMENT")
obj2.components[obj2.GetComponent("CONSTANTMOVEMENT")].constantVelocity = [12,0]
obj2.tag = "enemy"
enemy = Prefab("Enemy",obj2)

SceneOne.AddObject(enemy.CreateInstance([100,100],0,[1,1]))
SceneOne.AddObject(enemy.CreateInstance([200,375],0,[1,1]))
SceneOne.AddObject(enemy.CreateInstance([400,210],0,[1,1]))

boxC = enemy.CreateInstance([300,25],0,[1,1])
boxC.name = "lol"
boxC.AddComponent("BOXCONTROLLER")
boxC.components[boxC.GetComponent("RENDERER")].sprite = 2
boxC.components[boxC.GetComponent("COLLIDER")].SetAsImage(sprites[2])
boxC.components[boxC.GetComponent("COLLIDER")].trigger = False
boxC.components.pop(boxC.GetComponent("CONSTANTMOVEMENT"))
SceneOne.AddObject(boxC)

obj4 = GameObject("Ground")
obj4.AddComponent("RENDERER")
obj4.AddComponent("RIGIDBODY")
obj4.AddComponent("COLLIDER")
obj4.position = [0,500]
obj4.scale = [30,7]
obj4.components[obj4.GetComponent("RENDERER")].sprite = 3
obj4.components[obj4.GetComponent("RENDERER")].sortingLayer = 5
obj4.components[obj4.GetComponent("RIGIDBODY")].lockedY = True
obj4.components[obj4.GetComponent("COLLIDER")].SetAsImage(sprites[3])
print(obj4.components[obj4.GetComponent("COLLIDER")].size)

obj5 = GameObject("Ground")
obj5.AddComponent("RENDERER")
obj5.AddComponent("RIGIDBODY")
obj5.AddComponent("COLLIDER")
obj5.position = [0,0]
obj5.scale = [30,7]
obj5.components[obj5.GetComponent("RENDERER")].sprite = 3
obj5.components[obj5.GetComponent("RENDERER")].sortingLayer = 5
obj5.components[obj5.GetComponent("RIGIDBODY")].lockedY = True
obj5.components[obj5.GetComponent("COLLIDER")].SetAsImage(sprites[3])
print(obj5.components[obj5.GetComponent("COLLIDER")].size)
SceneOne.AddObject(obj4)
SceneOne.AddObject(obj5)

SceneTwo = Scene("Scene Two", [])
SceneTwo.AddObject(boxC)
scenes.append(SceneTwo)


game = gameengine.engine.GameInfo("Game Test 1", {"RESOLUTION":(800,600),"GRAVITY":0,"KEYREPEAT":(50,50)},componentMaster,scenes,0,sprites)

LaunchGame(game)
