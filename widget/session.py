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

    def importProject(self):
        self.controller.client.session.get_functions()
        self.controller.client.session.get_terrains()

        self.controller.qgis.loadWMSLayer(self.controller.client.session.get_wms_uri("GRAY"),"GrayLayer")

        def classifyBuildings(layer):
            self.controller.qgis.apply_style_to_layer(layer,"Buildings")
            self.controller.qgis.setup_custom_ui("buildings",layer)

            all_functions = self.controller.client.constants.FUNCTIONS_TYPE
            value_map = {f"{item.get('id')} - {item.get('name')}": str(item.get('id')) for item in all_functions}

            field_index = layer.fields().indexOf("function")
            
            if field_index != -1:
                layer.setEditorWidgetSetup(field_index, QgsEditorWidgetSetup('ValueMap', {'map': value_map}))



        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("buildings"),"Buildings Vector",classifyBuildings)

        def classifyTerrain(layer):
            self.controller.qgis.apply_style_to_layer(layer,"Terrain")

            all_terrains = self.controller.client.constants.TERRAIN_TYPE
            value_map = {f"{item.get('id')} - {item.get('name')}": str(item.get('id')) for item in all_terrains}

            field_index = layer.fields().indexOf("terrain_type")
            
            if field_index != -1:
                layer.setEditorWidgetSetup(field_index, QgsEditorWidgetSetup('ValueMap', {'map': value_map}))

        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("terrains"),"Terrain Vector",classifyTerrain)


        self.controller.qgis.loadWFSVector(self.controller.client.session.get_wfs_uri("areas"),"Areas Vector")

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

