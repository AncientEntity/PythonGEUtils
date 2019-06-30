"""
gameengine.blankcomponenttemplate can be copypasted and used to easily and fastly create new components
    
"""

from PythonGEUtils.engine import *


class ExampleComponent(BaseComponent):
    def __init__(self,s):
        """
        ExampleComponent() is an empty class inheriting from BaseComponent.
        It can be used as a reference to create new components fast.
        """
        self.parent = s
        self.name = "EXAMPLE"
        self.requiresStart = True
    def CreateNew(self,s):
        return ExampleComponent(s)
    def Start(self):
        pass
    def Update(self):
    	pass


componentMaster.append(ExampleComponent(None))
