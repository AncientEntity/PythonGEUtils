"""
gameengine.blankgametemplate can be copypasted and used to easily start up new projects without having to write the startup processes.


Uncomment the LaunchGame(game) line or it wont work.
    
"""
from PythonGEUtils.engine import *

sprites = []
scenes = []

MainScene = Scene("Scene One",[])
scenes.append(MainScene)










game = GameInfo("Game Test 1", {"RESOLUTION":(800,600),"GRAVITY":-0.03,"KEYREPEAT":(50,50)},componentMaster,scenes,0,sprites)

#LaunchGame(game)
