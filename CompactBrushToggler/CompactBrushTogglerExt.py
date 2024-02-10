 
from krita import *
from .CompactBrushTogglerExt import *

class CompactBrushTogglerExt(Extension):
    def __init__(self, parent):
        super().__init__(parent) 


    def setup(self):
        pass

    def createActions(self, window):
       action2 = window.createAction("compactBrushToggler", "Compact Brush Toggler", "tools/scripts")

# And add the extension to Krita's list of extensions:
app = Krita.instance()
extension = CompactBrushTogglerExt(parent=app) #instantiate your class
app.addExtension(extension)
