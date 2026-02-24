from krita import DockWidgetFactory, DockWidgetFactoryBase
from .CompactBrushToggler import CompactBrushToggler


DOCKER_NAME = 'CompactBrushToggler'
DOCKER_ID = 'pykrita_compactbrushtoggler'


Application.addDockWidgetFactory(
    DockWidgetFactory(DOCKER_ID, DockWidgetFactoryBase.DockPosition.DockRight,
        CompactBrushToggler))

 

 