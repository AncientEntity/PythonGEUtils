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

objects = []

background = GameObject("Back")
background.AddComponent("RENDERER")
background.position = [-25,0]
background.components[background.GetComponent("RENDERER")].sprite = pygame.image.load("background.png")
background.components[background.GetComponent("RENDERER")].sortingLayer = -10
background.scale = [4,4]
objects.append(background)

obj2 = GameObject("Falling Box Object3")
obj2.AddComponent("RENDERER")
obj2.AddComponent("RIGIDBODY")
obj2.AddComponent("COLLIDER")
obj2.position = [150,85]
obj2.scale = [1,1]
obj2.components[obj2.GetComponent("RENDERER")].sprite = pygame.image.load("redbox.png")
obj2.components[obj2.GetComponent("RENDERER")].sortingLayer = 10
obj2.components[obj2.GetComponent("RIGIDBODY")].locked = False
obj2.components[obj2.GetComponent("COLLIDER")].SetAsImage()
objects.append(obj2)

obj2 = GameObject("Falling Box Object2")
obj2.AddComponent("RENDERER")
obj2.AddComponent("RIGIDBODY")
obj2.AddComponent("COLLIDER")
obj2.position = [405,85]
obj2.scale = [1,1]
obj2.components[obj2.GetComponent("RENDERER")].sprite = pygame.image.load("redbox.png")
obj2.components[obj2.GetComponent("RENDERER")].sortingLayer = 10
obj2.components[obj2.GetComponent("RIGIDBODY")].locked = False
obj2.components[obj2.GetComponent("COLLIDER")].SetAsImage()
objects.append(obj2)

obj2 = GameObject("Falling Box Object1")
obj2.AddComponent("RENDERER")
obj2.AddComponent("RIGIDBODY")
obj2.AddComponent("COLLIDER")
obj2.AddComponent("BOXCONTROLLER")
obj2.position = [0,85]
obj2.scale = [1,1]
obj2.components[obj2.GetComponent("RENDERER")].sprite = pygame.image.load("redbox.png")
obj2.components[obj2.GetComponent("RENDERER")].sortingLayer = 10
obj2.components[obj2.GetComponent("RIGIDBODY")].locked = False
obj2.components[obj2.GetComponent("COLLIDER")].SetAsImage()
objects.append(obj2)

obj3 = GameObject("Moving Object")
obj3.AddComponent("RENDERER")
obj3.AddComponent("RIGIDBODY")
obj3.AddComponent("COLLIDER")
obj3.position = [0,50]
obj3.scale = [5,5]
obj3.components[obj3.GetComponent("RENDERER")].sprite = pygame.image.load("error.png")
obj3.components[obj3.GetComponent("RENDERER")].sortingLayer = 10
obj3.position = [400,150]
obj3.components[obj3.GetComponent("RIGIDBODY")].locked = True
obj3.AddComponent("TOMOUSETEST")
obj3.components[obj3.GetComponent("TOMOUSETEST")].offset = [-obj3.components[obj3.GetComponent("RENDERER")].sprite.get_width()/2,-obj3.components[obj3.GetComponent("RENDERER")].sprite.get_height()/2]
obj3.components[obj3.GetComponent("COLLIDER")].SetAsImage()
objects.append(obj3)



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
objects.append(obj4)


game = gameengine.engine.GameInfo("Game Test 1", {"RESOLUTION":(800,600),"GRAVITY":-0.03,"KEYREPEAT":(50,50)},componentMaster,objects)

LaunchGame(game)
