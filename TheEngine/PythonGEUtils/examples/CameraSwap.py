import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../')
from PythonGEUtils import *
from PythonGEUtils.engine import *
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
        #global objects
        #self.parent.position = [pygame.mouse.get_pos()[0] + self.offset[0],pygame.mouse.get_pos()[1]+self.offset[1]]
        for e in self.events:
            if(e.type == pygame.KEYDOWN):
                if(e.key == pygame.K_w):
                    c1 = GetObjectByTag("Main Camera")
                    c2 = GetObjectByTag("cam2")
                    c1.tag = "cam2"
                    c2.tag = "Main Camera"
                    print("SWAP")
                if(e.key == pygame.K_s):
                    o = Instantiate(obj2)
                    o.position = ScreenToWorldPoint([pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]])
                    print(ScreenToWorldPoint([pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]))
                if(e.key == pygame.K_SPACE):
                    for obj in GetObjectsByTag("falling"):
                        obj.AddComponent("RIGIDBODY")
                    print("reee")
componentMaster.append(ToMouseTest(None))


#COMPONENTS OVER

sprites = [pygame.image.load("background.png"),pygame.image.load("redbox.png"),pygame.image.load(errorImage),pygame.image.load("ground.png")]
scenes = []

SceneOne = Scene("Scene One",[])
scenes.append(SceneOne)

background = GameObject("Back")
background.AddComponent("RENDERER")
background.AddComponent("TOMOUSETEST")
background.position = [-25,0]
background.components[background.GetComponent("RENDERER")].sprite = 0
background.components[background.GetComponent("RENDERER")].sortingLayer = -10
background.scale = [4,4]
SceneOne.AddObject(background)

obj2 = GameObject("Falling Object Prefab")
obj2.AddComponent("RENDERER")
obj2.tag = "falling"
#obj2.AddComponent("RIGIDBODY")
obj2.AddComponent("COLLIDER")
obj2.position = [150,85]
obj2.scale = [1,1]
obj2.components[obj2.GetComponent("RENDERER")].sprite = 1
obj2.components[obj2.GetComponent("RENDERER")].sortingLayer = 10
#obj2.components[obj2.GetComponent("RIGIDBODY")].lockedY = False
obj2.components[obj2.GetComponent("COLLIDER")].SetAsImage(sprites[1])
obj2.components[obj2.GetComponent("COLLIDER")].trigger = True
fallingObjectPrefab = Prefab("Falling Object",obj2)

cam = GameObject("Cam 2")
cam.tag = "cam2"
cam.AddComponent("CAMERA")
cam.position = [200,200]
SceneOne.AddObject(cam)

SceneOne.AddObject(fallingObjectPrefab.CreateInstance([100,100],0,[1,1]))
SceneOne.AddObject(fallingObjectPrefab.CreateInstance([200,375],0,[1,1]))
SceneOne.AddObject(fallingObjectPrefab.CreateInstance([400,100],0,[1,1]))


SceneTwo = Scene("Scene Two", [])
scenes.append(SceneTwo)


game = GameInfo("Game Test 1", {"RESOLUTION":(800,600),"GRAVITY":-0.03,"KEYREPEAT":(50,50)},componentMaster,scenes,0,sprites)

LaunchGame(game)
