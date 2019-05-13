import pygame
import gameengine
import random
import time
import copy
import os
from gameengine import mathf


gameRunning = False
componentMaster = []
objects = []
prefabs = []
properties = {}
events = []
scenes = []
curScene = -1
camera = ""
GEPath = gameengine.__path__.__dict__["_path"][0]

errorImage = pygame.image.load(GEPath+"\\images\\error.png")

deltaTime = 0.0

lastObjectID = 0

def GetObject(indexOf):
    global objects
    for obj in objects:
        if(obj.index == indexOf):
            return obj
    return None


class GameObject():
    def __init__(self,name="New GameObject"):
        global lastObjectID
        self.active = True
        self.index = lastObjectID
        self.name = name
        self.tag = "untagged"
        self.position = [0.0,0.0]
        self.rotation = 360
        self.scale = [1,1]
        self.components = []
        lastObjectID += 1
    def AddComponent(self,componentName):
        for c in componentMaster:
            if(c.name == componentName):
                self.components.append(c.CreateNew(self))
    def GetComponent(self,componentName):
        for comp in range(len(self.components)):
            if(self.components[comp].name == componentName):
                return comp
        return None
    def __str__(self):
        return self.name
    def Destroy(self):
        global objects
        objects.remove(self)
    def GetColliderData(self):
        if(self.GetComponent("COLLIDER") == None):
            return None
        else:
            scale = self.scale
            offset = self.components[self.GetComponent("COLLIDER")].offset
            return (self.position[0]+offset[0],self.position[1]+offset[1],self.components[self.GetComponent("COLLIDER")].size[0],self.components[self.GetComponent("COLLIDER")].size[1])

class Prefab():
    def __init__(self,name, gO):
        global prefabs
        self.name = name
        self.gameObject = gO
        prefabs.append(self)
    def CreateInstance(self,position,rotation,scale):
        global objects, lastObjectID
        instance = GameObject()
        img = errorImage
        if(self.gameObject.components[self.gameObject.GetComponent("RENDERER")] != None):
            img = self.gameObject.components[self.gameObject.GetComponent("RENDERER")].sprite
            self.gameObject.components[self.gameObject.GetComponent("RENDERER")].sprite = ""
        instance = copy.deepcopy(self.gameObject)
        if(instance.components[instance.GetComponent("RENDERER")] != None):
            instance.components[instance.GetComponent("RENDERER")].sprite = img
            self.gameObject.components[self.gameObject.GetComponent("RENDERER")].sprite = img
        instance.position = position
        instance.rotation = rotation
        instance.scale = scale
        instance.index = lastObjectID
        lastObjectID += 1
        #objects.append(instance)
        return instance

class Scene():
    def __init__(self,name="New Scene",objects=[]):
        self.name = name
        self.objects = objects
    def AddObject(self,gO):
        global objects
        instance = GameObject()
        img = errorImage
        if(gO.GetComponent("RENDERER") != None):
            img = gO.components[gO.GetComponent("RENDERER")].sprite
            gO.components[gO.GetComponent("RENDERER")].sprite = ""
        instance = copy.deepcopy(gO)
        if(instance.GetComponent("RENDERER") != None):
            instance.components[instance.GetComponent("RENDERER")].sprite = img
            gO.components[gO.GetComponent("RENDERER")].sprite = img
        self.objects.append(instance)
        objects.append(instance)
    def AddObjects(self,gOs):
        for o in gOs:
            self.AddObject(o)

class BaseComponent():
    def __init__(self,s):
        self.parent = s
        self.name = "BASECOMPONENT"
        self.requiresStart = True
        self.events = []
    def CreateNew(self,s):
        raise BaseException("Component Error: Component doesn't have it's own CreateNew() and is relying on BaseComponent")
        #return BaseComponent()
    def Update(self):
        return False
    def Start(self):
        return False
    def __str__(self):
        return self.name

class Renderer(BaseComponent):
    def __init__(self,s):
        self.parent = s
        self.name = "RENDERER"
        self.requiresStart = False
        self.sprite = errorImage
        self.sortingLayer = 0
        self.color = [255,255,255,255]
    def CreateNew(self,s):
        return Renderer(s)

class Collider(BaseComponent):
    def __init__(self,s):
        self.parent = s
        self.name = "COLLIDER"
        self.requiresStart = False
        self.collidingWith = []
        self.size = [1,1]
        self.offset = [0,0]
        self.whereCollision = [False,False,False,False] #TopLeft/TopRight/BottomLeft/BottomRight
        self.friction = 0.065
        self.trigger = False
    def __str__(self):
        return self.name
    def IsCollidedWith(self,other):
        self.whereCollision = [False,False,False,False]
        otherData = pygame.Rect(other.GetColliderData())
        selfData = pygame.Rect(self.parent.GetColliderData())

        if(selfData.colliderect(otherData)):
            return True

        #If colliding with nothing
        return False
    def CollidingWithCollider(self):
            for col in self.collidingWith:
                if(col.components[col.GetComponent("COLLIDER")].trigger):
                    return True

            return False
    def ApplyFriction(self):
        if(self.trigger):
            return
        curVelocity = self.parent.components[self.parent.GetComponent("RIGIDBODY")].velocity
        if(self.whereCollision[0] == True or self.whereCollision[1] == True):
            if(curVelocity[0] < 0):
                curVelocity[0] += curVelocity[0] * self.friction
            elif(curVelocity[0] > 0):
                curVelocity[0] -= curVelocity[0] * self.friction
        self.parent.components[self.parent.GetComponent("RIGIDBODY")].velocity = curVelocity
    def CreateNew(self,s):
        return Collider(s)
    def Update(self):
        global objects
        self.collidingWith = []
        for other in objects:
            if(other.GetComponent("COLLIDER") != None and other.index != self.parent.index):
                if(self.IsCollidedWith(other)):
                    if(other.GetComponent("RIGIDBODY") != None):
                        blockCollision = True
                        if(other.GetComponent("COLLIDER") != None and other.components[other.GetComponent("COLLIDER")].trigger == True):
                            blockCollision = False
                        if(self.parent.GetComponent("COLLIDER") != None and self.parent.components[self.parent.GetComponent("COLLIDER")].trigger == True):
                            blockCollision = False

                        if(blockCollision):
                            other.components[other.GetComponent("RIGIDBODY")].velocity[1] = mathf.Clamp(other.components[other.GetComponent("RIGIDBODY")].velocity[1]-0.05,0,10000)
                            self.ApplyFriction()
                    self.collidingWith.append(other)
                    continue
        if(len(self.collidingWith) > 0 and self.trigger == False):
            if(self.parent.GetComponent("RIGIDBODY") != None and self.CollidingWithCollider()):
                self.parent.components[self.parent.GetComponent("RIGIDBODY")].velocity[1] = mathf.Clamp(other.components[other.GetComponent("RIGIDBODY")].velocity[1]-0.05,0,10000)
                self.ApplyFriction()
        #print(self.collidingWith,self.parent.name)
    def SetAsImage(self):
        global objects
        #print(self.parent)
        img = self.parent.components[self.parent.GetComponent("RENDERER")].sprite
        self.size[0] = img.get_width() * self.parent.scale[0]
        self.size[1] = img.get_height() * self.parent.scale[1]


                
class Rigidbody(BaseComponent):
    def __init__(self,s):
        self.parent = s
        self.name = "RIGIDBODY"
        self.requiresStart = True
        self.velocity = [0.0,0.0]
        self.lockedY = False
        self.lockedX= False
    def CreateNew(self,s):
        return Rigidbody(s)
    def Update(self):
        global properties, deltaTime, objects
        if(self.lockedY == False):
            self.velocity[1] += properties["GRAVITY"]
            #print("TEST")
            #if(self.parent.components[self.parent.GetComponent("COLLIDER")].whereCollision[2] or self.parent.components[self.parent.GetComponent("COLLIDER")].whereCollision[3]):
            #    objects[self.parent.index].position[1] += 10
        else:
            self.velocity[1] = 0
        if(self.lockedX == True):
            self.velocity[0] = 0

class ConstantMovement(BaseComponent):
    def __init__(self,s):
        self.parent = s
        self.name = "CONSTANTMOVEMENT"
        self.requiresStart = False
        self.constantVelocity = [1,0]
    def CreateNew(self,s):
        return ConstantMovement(s)
    def Update(self):
        self.parent.components[self.parent.GetComponent("RIGIDBODY")].velocity = self.constantVelocity

class UIText(BaseComponent):
    def __init__(self,s):
        self.parent = s
        self.name = "UITEXT"
        self.text = "New Text"
        self.font = "Comic Sans MS"
        self.size = 30
        self.requiresStart = True
        self.generatedFont = ""
        self.generatedRender = ""
        self.centered = False
        self.lastTextGenerated = ""
    def CreateNew(self,s):
        return UIText(s)
    def GenerateText(self):
        self.generatedFont = pygame.font.SysFont(self.font,self.size)
        self.generatedRender = self.generatedFont.render(self.text,True,(0,0,0))
        self.lastTextGenerated = self.text
    def Start(self):
        self.GenerateText()
    def Update(self):
        if(self.lastTextGenerated != self.text):
            self.GenerateText()


def GetObjectByName(name):
    global objects
    for obj in objects:
        if(obj.name == name):
            return obj
    return None

def GetObjectsByName(name):
    found = []
    global objects
    for obj in objects:
        if(obj.name == name):
            found.append(obj)
    return found

def GetObjectByTag(tag):
    global objects
    for obj in objects:
        if(obj.tag == tag):
            return obj
    return None

def GetObjectsByTag(tag):
    found = []
    global objects
    for obj in objects:
        if(obj.tag == tag):
            found.append(obj)
    return found

def CreateComponentSeperate(componentName):
    for c in componentMaster:
        if(c.name == componentName):
            return(c.CreateNew(None))

def CloneGameObject(gO):
    instance = GameObject()
    img = errorImage
    if(gO.GetComponent("RENDERER") != None):
        img = gO.components[gO.GetComponent("RENDERER")].sprite
        gO.components[gO.GetComponent("RENDERER")].sprite = ""
    instance = copy.deepcopy(gO)
    if(instance.GetComponent("RENDERER") != None):
        instance.components[instance.GetComponent("RENDERER")].sprite = img
        gO.components[gO.GetComponent("RENDERER")].sprite = img
    return instance

def FindAllComponents(typeof):
    comp = []
    for obj in objects:
        if(typeof in obj.components):
            comp.append(obj.components[typeof])
    return comp

def RenderEngine(screen):
    global objects
    screen.fill((255,255,255))
    objsWithRenderers = []
    uiObjs = []
    for obj in objects:
        if(obj.GetComponent("RENDERER") != None):
            objsWithRenderers.append(obj)
        elif(obj.GetComponent("UITEXT") != None):
            uiObjs.append(obj)
    #Main Objects
    for obj in sorted(objsWithRenderers, key=lambda x: x.components[x.GetComponent("RENDERER")].sortingLayer, reverse=False):
        if(obj.active == False):
            continue
        #print(obj.GetComponent("RENDERER"))
        if(obj.GetComponent("RENDERER") != "" and obj.GetComponent("RENDERER") != None):
            #print(obj.components)
            scaled = obj.components[obj.GetComponent("RENDERER")].sprite
            scaled = pygame.transform.rotate(scaled,obj.rotation)
            #scaled = scaled.fill(obj.components[obj.GetComponent("RENDERER")].color,special_flags=pygame.BLEND_ADD)
            scaled = pygame.transform.scale(scaled,(scaled.get_width() * obj.scale[0],scaled.get_height() * obj.scale[1]))
            #screen.blit(scaled,(obj.position[0]-(scaled.get_width()/2),obj.position[1]-(scaled.get_height()/2))) #Center it
            screen.blit(scaled,obj.position)
    #UI Objects
    for obj in uiObjs:
        if(obj.active == False):
            continue
        if(obj.GetComponent("UITEXT") != None):
            scaled = obj.components[obj.GetComponent("UITEXT")].generatedRender
            scaled = pygame.transform.rotate(scaled,obj.rotation)
            scaled = pygame.transform.scale(scaled,(scaled.get_width() * obj.scale[0],scaled.get_height() * obj.scale[1]))
            if(obj.components[obj.GetComponent("UITEXT")].centered):
                screen.blit(scaled,[obj.position[0]-scaled.get_width()/2,obj.position[1]-scaled.get_height()/2])
            else:
                screen.blit(scaled,obj.position)

    pygame.display.update()

def DoPhysics():
    global objects
    for obj in objects:
        if(obj.active == False):
            continue
        if(obj.GetComponent("RIGIDBODY") != None):
            obj.position[1] -= obj.components[obj.GetComponent("RIGIDBODY")].velocity[1]
            obj.position[0] -= obj.components[obj.GetComponent("RIGIDBODY")].velocity[0]
            #print(obj)

def InputSystem():
    global events
    e = pygame.event.get()
    for event in e:
        if(event.type == pygame.QUIT):
            exit(0)
    return e

def LoadScene(sceneIndex):
    global objects, scenes, curScene
    objects = []
    #objects = scenes[sceneIndex].objects
    for obj in scenes[sceneIndex].objects:
        objects.append(CloneGameObject(obj))
    curScene = sceneIndex
    print("Scene Loaded: " + scenes[sceneIndex].name)



def DoComponentSpecialFunctions():
    global objects
    for obj in objects:
        if(obj.active == False):
            continue
        for component in obj.components:
            component.parent = obj
            component.events = events
            component.Update()
            if(component.requiresStart == True):
                component.Start()
                component.requiresStart = False


#FINALIZATION
componentMaster.append(BaseComponent(None))
componentMaster.append(Renderer(None))
componentMaster.append(Collider(None))
componentMaster.append(Rigidbody(None))
componentMaster.append(ConstantMovement(None))
componentMaster.append(UIText(None))


class GameInfo():
    def __init__(self,name,properties,components,scenes,defaultSceneIndex):
        self.name = name
        self.properties = properties
        self.scenes = scenes
        self.components = components
        self.defaultSceneIndex = defaultSceneIndex
        #Do default settings
        if("RESOLUTION" not in self.properties):
            self.properties["RESOLUTION"] = (800,600)
        if("GRAVITY" not in self.properties):
            self.properties["GRAVITY"] = -0.035
        if("KEYREPEAT" not in self.properties):
            self.properties["KEYREPEAT"] = (50,50)
            
            

def LaunchGame(GameInfo):
    global scenes
    global properties
    global gameRunning
    global events
    global curScene
    if(gameRunning):
        return "Game Already Running"
    gameRunning = True
    #objects = GameInfo.objects
    scenes = GameInfo.scenes
    properties = GameInfo.properties
    LoadScene(GameInfo.defaultSceneIndex)
    #curScene = GameInfo.defaultSceneIndex

    pygame.font.init()
    screen = pygame.display.set_mode((GameInfo.properties["RESOLUTION"]))
    pygame.display.set_caption(GameInfo.name)
    renderStart = 0
    pygame.key.set_repeat(properties["KEYREPEAT"][0],properties["KEYREPEAT"][1])
    while gameRunning:
        renderStart = time.time()
        events = InputSystem()
        DoComponentSpecialFunctions()
        DoPhysics()
        RenderEngine(screen)
        deltaTime = time.time() - renderStart
    
