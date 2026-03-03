from ..TygronClient.client import *

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

    def importProject(self):
        # Step one, add base layer. using the provided gray layer for soft colors and readability
        self.controller.qgis.loadWMSLayer(self.controller.client.session.get_wms_uri("GRAY"),"GrayLayer")

        # step two, load in buildings
        def classifyBuildings(layer):
            self.controller.qgis.apply_style_to_layer(layer,"Buildings")
        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("buildings"),"Buildings Vector",classifyBuildings)

        # step three, load in terrain
        def classifyTerrain(layer):
            self.controller.qgis.apply_style_to_layer(layer,"Terrain")
        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("terrains"),"Terrain Vector",classifyTerrain)


        # step four, load in areas
        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("areas"),"Areas Vector")

        # step four, load in areas
        def classifyNeighborhoods(layer):
            self.controller.qgis.apply_style_to_layer(layer,"Neighborhoods")
            self.controller.qgis.classify(layer,"name")

        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("neighborhoods"),"Neighborhoods Vector",classifyNeighborhoods)



    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.get("ReturnButton").clicked.connect(self.returnToHome)
        self.get("Overlays").clicked.connect(self.toOverlays)
        self.get("LayerButton").clicked.connect(self.toLayers)
        self.get("Measures").clicked.connect(self.toMeasures)
        self.get("EditButton").clicked.connect(self.toEdits)
        self.get("Import").clicked.connect(self.importProject)

