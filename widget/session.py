from ..TygronClient.client import *
from qgis.core import QgsEditorWidgetSetup
class SessionPage:


    widget = None
    controller = None
    pageIndex = 3
    instancePrefix = "Session"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)

    def returnToHome(self):
        self.controller.client.session.validate_session(None)
        self.controller.switch_to_page(self.controller.apiEntry)

    def open(self,**kwargs):
        self.controller.client.session.update_project()
        self.get("NameLabel").setText(f"Session {self.controller.client.session.project_name} ({self.controller.client.session.domain})")

    def toOverlays(self):
        self.controller.switch_to_page(self.controller.overlaysOverview)
    def toLayers(self):
        self.controller.switch_to_page(self.controller.overlays)
    def toMeasures(self):
        self.controller.switch_to_page(self.controller.measures)
    def toEdits(self):
        self.controller.switch_to_page(self.controller.layers)
    def runTest(self):
        pass

    def importProject(self):
        self.controller.client.session.get_functions()
        self.controller.client.session.get_terrains()
        orderlist = [None] * 5

        graylayer = self.controller.qgis.loadWMSLayer(self.controller.client.session.get_wms_uri("GRAY"),"GrayLayer")
        def setOrder(layer,order):
            orderlist[order] = layer
            if None not in orderlist:
                self.controller.qgis.set_layer_order(orderlist)
                pass
        def processareas(layer):
            setOrder(layer,0)


        def classifyBuildings(layer):
            self.controller.qgis.apply_style_to_layer(layer,"Buildings")
            self.controller.qgis.setup_custom_ui(layer,"buildings")
            setOrder(layer,2)

        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("buildings"),"Buildings Vector",classifyBuildings)

        def classifyTerrain(layer):
            self.controller.qgis.apply_style_to_layer(layer,"Terrain")
            self.controller.qgis.setup_custom_ui(layer,"terrain")
            setOrder(layer,3)

        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("terrains"),"Terrain Vector",classifyTerrain)

        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("areas"),"Areas Vector",processareas)

        def classifyNeighborhoods(layer):
            self.controller.qgis.apply_style_to_layer(layer,"Neighborhoods")
            self.controller.qgis.classify(layer,"name")
            setOrder(layer,1)
        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("neighborhoods"),"Neighborhoods Vector",classifyNeighborhoods)
        setOrder(graylayer,4)



    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.get("ReturnButton").clicked.connect(self.returnToHome)
        self.get("Overlays").clicked.connect(self.toOverlays)
        #self.get("LayerButton").clicked.connect(self.toLayers)
        self.get("TestButton").clicked.connect(self.runTest)
        self.get("EditButton").clicked.connect(self.toEdits)
        self.get("Import").clicked.connect(self.importProject)

