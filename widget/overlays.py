from ..TygronClient.client import *

class OverlaysPage:


    widget = None
    controller = None
    pageIndex = 4
    instancePrefix = "Overlays"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)
    
    def returnToSession(self):
        self.controller.switch_to_page(self.controller.session)
            
    def open(self,**kwargs):
        pass

    def addSatellite(self):
        uri = self.controller.client.session.get_wms_uri("SATELLITE")
        self.controller.qgis.loadWMSLayer(uri,"Satellite View")
    def addWater(self):
        pass
    def addTerrain(self):
        uri = self.controller.client.session.get_wfs_uri("terrains")
        self.controller.qgis.loadWFSVector(uri,"Terrain Vector","terrain_type")
    def addBuildings(self):
        uri = self.controller.client.session.get_wfs_uri("buildings")
        self.controller.qgis.loadWFSVector(uri,"Buildings Vector","function")
    def addMeasures(self):
        uri = self.controller.client.session.get_wfs_uri("measures")
        self.controller.qgis.loadWFSVector(uri,"Measures Vector")

    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.get("ReturnButton").clicked.connect(self.returnToSession)

        self.get("QuickSatellite").clicked.connect(self.addSatellite)
        self.get("QuickWater").clicked.connect(self.addWater)
        self.get("QuickBuildings").clicked.connect(self.addBuildings)
        self.get("QuickTerrain").clicked.connect(self.addTerrain)
        self.get("QuickMeasures").clicked.connect(self.addMeasures)