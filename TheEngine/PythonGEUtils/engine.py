"""
gameengine.engine is the base library for PythonGEUtils. It is required to do
just about anything with it.


"""
import pygame
#import engine
import sys
import random
import time
import copy
import os
import PythonGEUtils.mathf
    
#print("PythonGEUtils Loaded")


gameRunning = False
componentMaster = []
objects = []
prefabs = []
properties = {}
events = []
sprites = []
scenes = []
queuedEvents = []
curScene = -1
camera = ""
GEPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(GEPath)

errorImage = (GEPath+"\\images\\error.png")

deltaTime = 0.0

lastObjectID = 0

def GetObject(indexOf):
    """
    GetObject(indexOf) allows you to get the object at a certain index.
    """
    global objects
    for obj in objects:
        if(obj.index == indexOf):
            return obj
    return None


class GameObject():
    def __init__(self,name="New GameObject"):
        """
                   Base class for all entities in a Scene. A blank GameObject cannot do much, to allow it to function as you wish you must add custom or premade components.     
        """
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
        self.oldPosition = [0.0,0.0]
    def RemoveComponent(self,componentName):
        """
        RemoveComponent(componentName) allows you to remove a component from
        the GameObject by its name.
        """
        for c in self.components:
            if(c.name == componentName):
                self.components.remove(c)
                return True
        return False
    def AddComponent(self,componentName):
        """
        AddComponent(componentName) allows you to add a component to the
        GameObject by its name"
        """
        for c in componentMaster:
            if(c.name == componentName):
                self.components.append(c.CreateNew(self))
    def GetComponent(self,componentName):
        """
        GetComponent(componentName) will return the index of a component by
        its name
        """
        for comp in range(len(self.components)):
            if(self.components[comp].name == componentName):
                return comp
        return None
    def DirectComponent(self,componentName):
        """
        GetComponent(componentName) will return a pointer to the object so
        you can edit it directly.
        """
        for comp in range(len(self.components)):
            if(self.components[comp].name == componentName):
                return self.components[comp]
        return None
    def __str__(self):
        return self.name
    def Destroy(self):
        """
        Destroy() allows you to destroy the GameObject.
        """
        global objects
        if(self in objects):
            objects.remove(self)
    def GetColliderData(self):
        """
        GetColliderData() will only work if you have a collider attached to
        the GameObject. It is suggested you do not use this function as it
        is mainly for the engine.
        """
        if(self.GetComponent("COLLIDER") == None):
            return None
        else:
            scale = self.scale
            offset = self.components[self.GetComponent("COLLIDER")].offset
            return [self.position[0]+offset[0],self.position[1]+offset[1],self.components[self.GetComponent("COLLIDER")].size[0],self.components[self.GetComponent("COLLIDER")].size[1]]

class Prefab():
    def __init__(self,name, gO):
        """
        When you want to reuse a GameObject multiple times (example: a tree) you should
        use a prefab as it allows you to create copies of a GameObject that you can
        edit certain variables afterwards.
        """
        global prefabs
        self.name = name
        self.gameObject = gO
        prefabs.append(self)
    def CreateInstance(self,position,rotation,scale):
        """
        CreateInstance(position,rotation,scale) will create a copy of the parent prefab with the parameters
        given as well as return the GameObject. This wont add it to the scene/game. You must instantiate the instance with Instantiate()!!!!
        """
        global objects, lastObjectID
        instance = GameObject()
        img = errorImage
        if(self.gameObject.GetComponent("RENDERER") != None):
            img = self.gameObject.components[self.gameObject.GetComponent("RENDERER")].sprite
            self.gameObject.components[self.gameObject.GetComponent("RENDERER")].sprite = ""
        instance = copy.deepcopy(self.gameObject)
        if(instance.GetComponent("RENDERER") != None):
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
    def __init__(self,name="New Scene",objects=[], defaultCamera=True):
        """
        Scene's are a collection of GameObjects that can be loaded/unloaded easily fast and quick. (see LoadScene())

        Scene(name,objects) can be passed through or Scene(name,objects,defaultCamera=True) can be passed. If you pass
        defaultCamera as true (which is true by default) it will automatically add the camera to your scene.
        """
        self.name = name
        self.objects = objects
        if(defaultCamera):
            cam = GameObject("Default Camera")
            cam.AddComponent("CAMERA")
            #cam.AddComponent("RIGIDBODY") #Was For Testing
            cam.tag = "Main Camera"
            self.objects.append(CloneGameObject(cam))
    def AddObject(self,gO):
        """
        AddObject(gameObject) will take the game object passed and add it to the scene, it will not be loaded into the game until the scene is loaded.
        """
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
        #objects.append(instance)
    def AddObjects(self,gOs):
        """
        AddObjects(gameObjects) will add every passed GameObject in the list given to the scene, it will not be loaded into the game until the scene is loaded.
        """
        for o in gOs:
            self.AddObject(o)

class BaseComponent():
    def __init__(self,s=None):
        """
        This is the base component of all components that come with PythonGEUtils.
        It is also suggested you use BaseComponent as the base for all of your custom
        components to prevent any issues.

        When creating a custom component you must have a custom CreateNew(self,s) function on it or the
        engine wont be able to create instances and errors will occur. Below is an example
        of what the camera uses, all you have to do is change "Camera" to the components name:


        \"\"\"

        
            def CreateNew(self,s):
                return Camera(s)

            
        \"\"\"

        
        When creating a custom component you must add it to the list componentMaster or issues will occur.
        Here are a few examples of how you must add it:

            componentMaster.append(BaseComponent(None))
            componentMaster.append(Renderer(None))
            componentMaster.append(Collider(None))
    

        Component names don't have to be in caps but were just started like that so it is suggested you continue
        as it will make reading your code easier for people.
        """
        global componentMaster
        self.parent = s
        self.name = "BASECOMPONENT"
        self.requiresStart = True
        self.events = []
    def CreateNew(self,s):
        """
        When creating a custom component you must add it's own CreateNew(self,s) function that returns itself with s being passed.
        """
        raise BaseException("Component Error: Component doesn't have it's own CreateNew() and is relying on BaseComponent")
        #return BaseComponent()
    def Update(self):
        """
        Update() runs every frame on every object that has this component.
        """
        return False
    def Start(self):
        """
        Start() runs the first frame the component is loaded.
        """
        return False
    def __str__(self):
        return self.name

class Camera(BaseComponent):
    def __init__(self,s):
        """
        This is the default Camera component for the engine. Generally you do not want to edit this.
        """
        self.parent = s
        self.name = "CAMERA"
        self.requiresStart = False
    def CreateNew(self,s):
        """
        CreateNew(self,s) creates a new Camera Object
        """
        return Camera(s)
    def SetMain(self):
        """
        SetMain() will make the Camera calling the function the main camera and all rendering will be based from
        the Camera's position.
        """
        GetObjectByTag("Main Camera").tag = "untagged"
        self.parent.tag = "Main Camera"

class Renderer(BaseComponent):
    def __init__(self,s):
        """
        The renderer allows objects to be shown on the game screen. If you attach a sprite onto it through Renderer.sprite it will be displayed.
        """
        self.parent = s
        self.name = "RENDERER"
        self.requiresStart = False
        self.sprite = errorImage
        self.sortingLayer = 0
        self.color = [255,255,255,255]
    def CreateNew(self,s):
        """
        CreateNew(self,s) creates a new Renderer Object
        """
        return Renderer(s)

class Collider(BaseComponent):
    def __init__(self,s):
        """
        A Collider allows collision between 2 or more objects to be detected as well as these can be used as triggers where the objects can pass through each other
        but they still tell you what is colliding.
        """
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
        """
        IsCollidedWith(other) will return true if you are colliding with 'other' and return false if you are not.
        """
        self.whereCollision = [False,False,False,False]
        otherData = pygame.Rect(other.GetColliderData())
        selfData = pygame.Rect(self.parent.GetColliderData())

        if(selfData.colliderect(otherData)):
            return True

        #If colliding with nothing
        return False
    def CollisionBox(self,size,offset="DEFAULT"):
        """
        This creates a temporary collision detection zone around the GameObject in the shape of a rectangle/box. It returns all objects colliding with it.
        """
        if(offset == "DEFAULT"):
            offset = [-size[0]/2,-size[1]/2]
        colliders = []
        for obj in GetObjects():
            if(obj.DirectComponent("COLLIDER") == None or obj == self.parent):
                continue
            otherData = pygame.Rect(obj.GetColliderData())
            selfData = pygame.Rect(self.parent.position[0]+offset[0],self.parent.position[1]+offset[1],size[0],size[1])
            if(selfData.colliderect(otherData)):
                colliders.append(obj)
        return colliders
    def CollidingWithCollider(self):
        for col in self.collidingWith:
            if(col.components[col.GetComponent("COLLIDER")].trigger):
                return True
        return False
    def ApplyFriction(self):
        """
        ApplyFriction() applies friction to the object. ApplyFriction() gets automatically run.
        """
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
        """
        CreateNew(self,s) creates a new instance of Collider()
        """
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
                            other.components[other.GetComponent("RIGIDBODY")].velocity[1] = PythonGEUtils.mathf.Clamp(other.components[other.GetComponent("RIGIDBODY")].velocity[1]-0.05,0,10000)
                            self.ApplyFriction()
                    self.collidingWith.append(other)
                    continue
        if(len(self.collidingWith) > 0 and self.trigger == False):
            #print(self.parent.GetComponent("RIGIDBODY"))
            if(self.parent.GetComponent("RIGIDBODY") != None and self.CollidingWithCollider() and other.GetComponent("COLLIDER") != None):
                self.parent.components[self.parent.GetComponent("RIGIDBODY")].velocity[1] = PythonGEUtils.mathf.Clamp(other.components[other.GetComponent("RIGIDBODY")].velocity[1]-0.05,0,10000)
                self.ApplyFriction()
        #print(self.collidingWith,self.parent.name)
    def SetAsImage(self,i=None):
        """
        SetAsImage() will set the collider dimensions as the image's dimensions. If an image is given as a parameter it will become the size of that image.
        """
        global objects, sprites, gameRunning, queuedEvents

        #if(gameRunning == False):
        #    queuedEvents.append(self.SetAsImage)
        #    return

        #print(self.parent)
        img = None
        if(i == None):
            if(sprites == []):
                raise("Uninitialized Games Require an input of the sprite")
            img = sprites[self.parent.components[self.parent.GetComponent("RENDERER")].sprite]
        else:
            img = i
        self.size[0] = img.get_width() * self.parent.scale[0]
        self.size[1] = img.get_height() * self.parent.scale[1]


                
class Rigidbody(BaseComponent):
    def __init__(self,s):
        """
        Rigidbody's are used to have an object undergo physics.
        """
        self.parent = s
        self.name = "RIGIDBODY"
        self.requiresStart = True
        self.velocity = [0.0,0.0]
        self.lockedY = False
        self.lockedX= False
    def CreateNew(self,s):
        """
        CreateNew(self,s) creates a new instance of Rigidbody()
        """
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
        """
        ConstantMovement will apply a constant velocity to an object.
        """
        self.parent = s
        self.name = "CONSTANTMOVEMENT"
        self.requiresStart = False
        self.constantVelocity = [1,0]
    def CreateNew(self,s):
        """
        CreateNew(self,s) creates a new instance of ConstantMovement()
        """
        return ConstantMovement(s)
    def Update(self):
        self.parent.components[self.parent.GetComponent("RIGIDBODY")].velocity = self.constantVelocity

class UIText(BaseComponent):
    def __init__(self,s):
        """
        UIText is used for when you want to create text and display it to the screen.
        """
        self.parent = s
        self.name = "UITEXT"
        self.text = "New Text"
        self.font = "Comic Sans MS"
        self.size = 30
        self.offset = [0,0]
        self.requiresStart = True
        self.generatedFont = ""
        self.generatedRender = ""
        self.centered = False
        self.lastTextGenerated = ""
        self.lastTextSize = 30
    def CreateNew(self,s):
        """
        CreateNew(self,s) creates a new instance of UIText()
        """
        return UIText(s)
    def GenerateText(self):
        """
        It is not recommended you use GenerateText() as it is mainly for the engine to use to generate
        the image of the text.

        GenerateText() will use the variables contained in UIText() and generates an image, then the image
        gets stored in self.generatedRender
        """
        self.generatedFont = pygame.font.SysFont(self.font,self.size)
        self.generatedRender = self.generatedFont.render(self.text,True,(0,0,0))
        self.lastTextGenerated = self.text
        self.lastTextSize = self.size
    def Start(self):
        self.GenerateText()
    def Update(self):
        if(self.lastTextGenerated != self.text or self.lastTextSize != self.size):
            #print("regen ---------------------------------------------------")
            self.GenerateText()

class UIButton(BaseComponent):
    def __init__(self,s):
        """
        UIButton() is used for when you want to create a button and allow for a user to click it and invoke
        an action(s).
        """
        self.parent = s
        self.name = "UIBUTTON"
        self.sprite = errorImage
        self.requiresStart = False
        self.functions = []
        self.centered = True
        self.pressed = False
    def CreateNew(self,s):
        """
        CreateNew(self,s) creates a new instance of UIButton()
        """
        return UIButton(s)
    def Update(self):
        global sprites
        x = False
        for event in self.events:
            if(event.type == pygame.MOUSEBUTTONDOWN):
                x = True
        if(x == False):
            return
        mPos = pygame.mouse.get_pos()
        loadedSprite = sprites[self.sprite]
        if(self.centered == False):
            if(mPos[0] >= self.parent.position[0] and mPos[0] <= self.parent.position[0]+(loadedSprite.get_width() * self.parent.scale[0])):
                if((mPos[1] >= self.parent.position[1] and mPos[1] <= self.parent.position[1]+(loadedSprite.get_height() * self.parent.scale[1]))):
                    for function in self.functions:
                        exec(function)
                    #print("Test")
        else:
            if(mPos[0] >= self.parent.position[0]-(loadedSprite.get_width()/2 * self.parent.scale[0]) and mPos[0] <= self.parent.position[0]+(loadedSprite.get_width()/2 * self.parent.scale[0])):
                if((mPos[1] >= self.parent.position[1]-(loadedSprite.get_width()/2 * self.parent.scale[0]) and mPos[1] <= self.parent.position[1]+(loadedSprite.get_height()/2 * self.parent.scale[1]))):
                    for function in self.functions:
                        exec(function)
                    #print("Test")
        self.pressed = True


def Instantiate(obj):
    """
    Instantiate(object) will add the object to the scene. To add a prefab you must use Prefab().CreateInstance(position,scale,rotation).
    """
    global objects
    o = CloneGameObject(obj)
    objects.append(o)
    return o

def GetObjectByName(name):
    """
    Returns the first object found with the name given. If no object of the name is found
    it returns None.
    """
    global objects
    for obj in objects:
        if(obj.name == name):
            return obj
    return None

def GetObjectsByName(name):
    """
    GetObjectsByName(name) finds all objects of a name and returns them in a list.
    """
    found = []
    global objects
    for obj in objects:
        if(obj.name == name):
            found.append(obj)
    return found

def GetObjectByTag(tag):
    """
    Returns the first object found with the tag given. If no object of the tag is found
    it returns None.
    """
    global objects
    for obj in objects:
        if(obj.tag == tag):
            return obj
    return None

def GetObjectsByTag(tag):
    """
    GetObjectsByTag(name) finds all objects of a tag and returns them in a list.
    """
    found = []
    global objects
    for obj in objects:
        if(obj.tag == tag):
            found.append(obj)
    return found

def GetObjects():
    """
    GetObjects() reeturns the list of all objects.
    """
    global objects
    return objects



def ScreenToWorldPoint(screenPoint):
    """
    ScreenToWorldPoint(screenPoint) takes a point on the screen and returns the world
    point.
    """
    cam = GetObjectByTag("Main Camera")
    camPos = [cam.position[0],cam.position[1]]
    return ([screenPoint[0]+camPos[0],screenPoint[1]+camPos[1]])


def CreateComponentSeperate(componentName):
    """
    CreateComponentSeperate(componentName) creates a component by it's name without it
    being attached to a GameObject then returns it.
    """
    for c in componentMaster:
        if(c.name == componentName):
            return(c.CreateNew(None))

def CloneGameObject(gO):
    """
    CloneGameObject(gameObject) will clone and return the given
    game object.
    """
    instance = GameObject()
    #img = errorImage
    #img2 = errorImage
    #if(gO.GetComponent("RENDERER") != None):
    #    img = gO.components[gO.GetComponent("RENDERER")].sprite
    #    gO.components[gO.GetComponent("RENDERER")].sprite = ""

    #if(gO.GetComponent("UIBUTTON") != None):
    #    img2 = gO.components[gO.GetComponent("UIBUTTON")].sprite
    #    gO.components[gO.GetComponent("UIBUTTON")].sprite = ""

    instance = copy.deepcopy(gO)
    #if(instance.GetComponent("RENDERER") != None):
    #    instance.components[instance.GetComponent("RENDERER")].sprite = img
    #    gO.components[gO.GetComponent("RENDERER")].sprite = img
    #if(instance.GetComponent("UIBUTTON") != None):
    #    instance.components[instance.GetComponent("UIBUTTON")].sprite = img2
    #    gO.components[gO.GetComponent("UIBUTTON")].sprite = img2
    return instance

def FindAllComponents(typeof):
    """
        FindAllComponents(typeof) finds all components of a certain type from
        all objects, then returns them in a list.
    """
    comp = []
    for obj in objects:
        if(typeof in obj.components):
            comp.append(obj.components[typeof])
    return comp

def RenderEngine(screen):
    """
    A Mandatory High Level game engine function. Do not edit/run/delete this unless you know what
    you are doing.

    ---

    RenderEngine() manages the rendering system.
    
    """
    global objects,sprites
    screen.fill((255,255,255))
    objsWithRenderers = []
    uiObjs = []
    for obj in objects:
        if(obj.GetComponent("RENDERER") != None):
            objsWithRenderers.append(obj)
        if(obj.GetComponent("UITEXT") != None):
            uiObjs.append(obj)
        elif(obj.GetComponent("UIBUTTON") != None):
            uiObjs.append(obj)
    #Main Objects
    for obj in sorted(objsWithRenderers, key=lambda x: x.components[x.GetComponent("RENDERER")].sortingLayer, reverse=False):
        if(obj.active == False):
            continue
        #print(obj.GetComponent("RENDERER"))
        if(obj.GetComponent("RENDERER") != "" and obj.GetComponent("RENDERER") != None):
            #print(obj.components)
            scaled = sprites[obj.components[obj.GetComponent("RENDERER")].sprite]
            scaled = pygame.transform.rotate(scaled,obj.rotation)
            #scaled = scaled.fill(obj.components[obj.GetComponent("RENDERER")].color,special_flags=pygame.BLEND_ADD)
            camPos = [-GetObjectByTag("Main Camera").position[0],-GetObjectByTag("Main Camera").position[1]]

            scaled = pygame.transform.scale(scaled,(scaled.get_width() * obj.scale[0],scaled.get_height() * obj.scale[1]))
            #screen.blit(scaled,(obj.position[0]-(scaled.get_width()/2),obj.position[1]-(scaled.get_height()/2))) #Center it
            screen.blit(scaled,[obj.position[0]+camPos[0],obj.position[1]+camPos[1]])
    #UI Objects
    for obj in uiObjs:
        if(obj.active == False):
            continue
        #UI BUTTON
        if(obj.GetComponent("UIBUTTON") != None):
            scaled = sprites[obj.components[obj.GetComponent("UIBUTTON")].sprite]
            scaled = pygame.transform.rotate(scaled,obj.rotation)

            scaled = pygame.transform.scale(scaled,(scaled.get_width() * obj.scale[0],scaled.get_height() * obj.scale[1]))

            if(obj.components[obj.GetComponent("UIBUTTON")].centered):
                screen.blit(scaled,[obj.position[0]-scaled.get_width()/2,obj.position[1]-scaled.get_height()/2])
            else:
                screen.blit(scaled,obj.position)
        #UI TEXT
        if(obj.GetComponent("UITEXT") != None):
            if(obj.components[obj.GetComponent("UITEXT")].generatedRender == ""):
                continue
            scaled = obj.components[obj.GetComponent("UITEXT")].generatedRender
            scaled = pygame.transform.rotate(scaled,obj.rotation)
            #scaled = pygame.transform.scale(scaled,(scaled.get_width() * obj.scale[0],scaled.get_height() * obj.scale[1]))
            if(obj.components[obj.GetComponent("UITEXT")].centered):
                screen.blit(scaled,[obj.position[0]-scaled.get_width()/2+obj.DirectComponent("UITEXT").offset[0],obj.position[1]-scaled.get_height()/2+obj.DirectComponent("UITEXT").offset[1]])
            else:
                screen.blit(scaled,obj.position)

    pygame.display.update()

def DoPhysics():
    """
    A Mandatory High Level game engine function. Do not edit/run/delete this unless you know what
    you are doing.

    ---

    It manages the base RigidBody actions.
    
    """
    global objects
    for obj in objects:
        if(obj.active == False):
            continue
        if(obj.GetComponent("RIGIDBODY") != None):
            obj.position[1] -= obj.components[obj.GetComponent("RIGIDBODY")].velocity[1]
            obj.position[0] -= obj.components[obj.GetComponent("RIGIDBODY")].velocity[0]
            #print(obj)

def InputSystem():
    """
    A Mandatory High Level game engine function. Do not edit/run/delete this unless you know what
    you are doing.

    ---

    It manages input from the keyboard, and defaultly sets the window's X button to closing the game.
    
    """
    global events
    e = pygame.event.get()
    for event in e:
        if(event.type == pygame.QUIT):
            exit(0)
    return e

def LoadScene(sceneIndex):
    """
    LoadScene(sceneIndex) will load the scene at the given index. It will remove all objects from the scene and reload it with the new scene.
    """
    global currentCamera
    global objects, scenes, curScene
    objects = []
    #objects = scenes[sceneIndex].objects
    for obj in scenes[sceneIndex].objects:
        objects.append(CloneGameObject(obj))
        #if(obj.tag == "Main Camera"):
        #    currentCamera = obj
    curScene = sceneIndex
    print("Scene Loaded: " + scenes[sceneIndex].name)



def DoComponentSpecialFunctions():
    """
    A Mandatory High Level game engine function. Do not edit/run/delete this unless you know what
    you are doing.

    ---

    DoComponentSpecialFunctions() manages Update() and Start()
    
    """
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
componentMaster.append(UIButton(None))
componentMaster.append(Camera(None))


class GameInfo():
    """
    GameInfo() is a class that contains your entire game that you submit using
    LaunchGame(GameInfo) to start your game.
    """
    def __init__(self,name,properties,components,scenes,defaultSceneIndex,sprites):
        self.name = name
        self.properties = properties
        self.scenes = scenes
        self.components = components
        self.defaultSceneIndex = defaultSceneIndex
        self.sprites = sprites
        #Do default settings
        if("RESOLUTION" not in self.properties):
            self.properties["RESOLUTION"] = (800,600)
        if("GRAVITY" not in self.properties):
            self.properties["GRAVITY"] = -0.035
        if("KEYREPEAT" not in self.properties):
            self.properties["KEYREPEAT"] = (50,50)
            
            

def LaunchGame(GameInfo):
    """
    LaunchGame(GameInfo) launches the game by using the GameInfo object that has been passed as a parameter.
    """
    global scenes
    global properties
    global gameRunning
    global events
    global curScene
    global sprites
    if(gameRunning):
        return "Game Already Running"
    gameRunning = True
    sprites = GameInfo.sprites
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


    #Do Engine Intro
    generatedFont = pygame.font.SysFont("Comic Sans MS",30)
    generatedRender = generatedFont.render("Python Game Engine Utils",True,(0,0,0))
    appleCenter = pygame.transform.scale(pygame.image.load(GEPath+"\\images\\apple.png"),(250,250))        
    
    for doIntro in range(0,255):
        screen.fill((255-doIntro,255-doIntro,255-doIntro))
        screen.blit(appleCenter,(GameInfo.properties["RESOLUTION"][0]//2-125,GameInfo.properties["RESOLUTION"][1]//2-125))
        screen.blit(generatedRender,(GameInfo.properties["RESOLUTION"][0]//2-125-50,GameInfo.properties["RESOLUTION"][1]//2-125+220))
        pygame.display.update()
        time.sleep(2.0/255.0) #make it last 3 seconds
    #Engine Intro End

    
    for event in queuedEvents:
        event

    while gameRunning:
        renderStart = time.time()
        events = InputSystem()
        DoComponentSpecialFunctions()
        DoPhysics()
        RenderEngine(screen)
        deltaTime = time.time() - renderStart
        #print(prefabs)
    
