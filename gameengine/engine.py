import pygame
import gameengine
import random
import time
from gameengine import mathf

gameRunning = False
componentMaster = []
objects = []
properties = {}
events = []
camera = ""

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
        self.index = lastObjectID
        self.name = name
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
        self.sprite = pygame.image.load("error.png")
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
    def __str__(self):
        return self.name
    def IsCollidedWith(self,other):
        self.whereCollision = [False,False,False,False]
        otherData = other.GetColliderData()
        selfData = self.parent.GetColliderData()
        #print(other.name,otherData)
        #print(GetObject(self.parent).name,selfData)
        #Left
        leftX = (otherData[0] >= selfData[0] and otherData[0] <= selfData[0]+selfData[2])
        leftYtop = (otherData[1] >= selfData[1] and otherData[1] <= selfData[1]+selfData[3])

        rightX = (otherData[0]+otherData[2] >= selfData[0] and otherData[0]+otherData[2] <= selfData[0]+selfData[2])
        rightYbottom = (otherData[1]+otherData[3] >= selfData[1] and otherData[1]+otherData[3] <= selfData[1]+selfData[3])

        #Save where it is colliding
        if(leftX and leftYtop): #Top Left
            self.whereCollision[0] = True
        if(rightX and leftYtop): #Top Right
            self.whereCollision[1] = True
        if(leftX and rightYbottom): #Bottom Left
            self.whereCollision[2] = True
        if(rightX and rightYbottom): #Bottom Right
            self.whereCollision[3] = True

        #Do Final Return
        if((leftX or rightX) and (leftYtop or rightYbottom)):
            #print(self.parent.name,self.parent.components[self.parent.GetComponent("COLLIDER")].whereCollision)
            return True

        #If colliding with nothing
        return False
    def ApplyFriction(self):
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
                        other.components[other.GetComponent("RIGIDBODY")].velocity[1] = mathf.Clamp(other.components[other.GetComponent("RIGIDBODY")].velocity[1]-0.05,0,10000)
                        self.ApplyFriction()
                    self.collidingWith.append(other)
                    continue
        if(len(self.collidingWith) > 0):
            if(self.parent.GetComponent("RIGIDBODY") != None):
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
        self.locked = False
    def CreateNew(self,s):
        return Rigidbody(s)
    def Update(self):
        global properties, deltaTime
        if(self.locked == False):
            self.velocity[1] += properties["GRAVITY"]
            #print("TEST")
        else:
            self.velocity = [0,0]


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
    for obj in objects:
        if(obj.GetComponent("RENDERER") != None):
            objsWithRenderers.append(obj)
    for obj in sorted(objsWithRenderers, key=lambda x: x.components[obj.GetComponent("RENDERER")].sortingLayer, reverse=False):
        #print(obj.GetComponent("RENDERER"))
        if(obj.GetComponent("RENDERER") != "" and obj.GetComponent("RENDERER") != None):
            #print(obj.components)
            scaled = obj.components[obj.GetComponent("RENDERER")].sprite
            scaled = pygame.transform.rotate(scaled,obj.rotation)
            #scaled = scaled.fill(obj.components[obj.GetComponent("RENDERER")].color,special_flags=pygame.BLEND_ADD)
            scaled = pygame.transform.scale(scaled,(scaled.get_width() * obj.scale[0],scaled.get_height() * obj.scale[1]))
            #screen.blit(scaled,(obj.position[0]-(scaled.get_width()/2),obj.position[1]-(scaled.get_height()/2))) #Center it
            screen.blit(scaled,obj.position)
    pygame.display.update()

def DoPhysics():
    global objects
    for obj in objects:
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

def DoComponentSpecialFunctions():
    global objects
    for obj in objects:
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



class GameInfo():
    def __init__(self,name,properties,components,objects):
        self.name = name
        self.properties = properties
        self.objects = objects
        self.components = components
        #Do default settings
        if("RESOLUTION" not in self.properties):
            self.properties["RESOLUTION"] = (800,600)
        if("GRAVITY" not in self.properties):
            self.properties["GRAVITY"] = -0.035
        if("KEYREPEAT" not in self.properties):
            self.properties["KEYREPEAT"] = (50,50)
            
            
    
def LaunchGame(GameInfo):
    global objects
    global properties
    global gameRunning
    global events
    if(gameRunning):
        return "Game Already Running"
    gameRunning = True
    objects = GameInfo.objects
    properties = GameInfo.properties
    
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
    