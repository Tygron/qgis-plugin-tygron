from ..TygronClient.client import *

class LayersPage:


    widget = None
    controller = None
    focusedLayer = None
    pageIndex = 5
    instancePrefix = "LayerControl"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)
    
    def start_edit(self):
        if self.focusedLayer is None:
            return
        
        self.controller.qgis.make_layer_editable(self.focusedLayer)
        self.controller.qgis.enable_topology()

    def commit(self):
        if self.focusedLayer is None:
            return
        
        if self.controller.qgis.validate_layer_changes(self.focusedLayer):
            self.controller.qgis.commit_layer_edits(self.focusedLayer)
            self.controller.qgis.reload_target_wms("Gray")


    def returnToSession(self):
        self.controller.switch_to_page(self.controller.session)

    def setFocusedLayer(self,layer=None):
        # set self.get("LayerName").setText() to qgis layer name
        # self.focusedLayer = layer
        self.focusedLayer = layer
        
        label = self.get("LayerName")
        if self.focusedLayer:
            # Update the UI with the name of the layer in QGIS
            label.setText(self.focusedLayer.name())
        else:
            label.setText("None")

    def cancelChanges(self):
        if not self.focusedLayer:
            return
        if not self.controller.qgis.confirmBox("Cancel Changes?","Are you sure you want to revert your changes on this layer?"):
            return
        
        if self.focusedLayer.isEditable():
            success = self.focusedLayer.rollBack()
            if success:
                self.focusedLayer.triggerRepaint()

    def editMode(self):
        self.controller.qgis.enableVertexTool()
    def drawMode(self):
        self.controller.qgis.enableAddFeature()


    def on_snap_toggle(self,state):
        is_enabled = state == 2
        if is_enabled:
            self.controller.qgis.toggle_snapping(True)
        else:
            self.controller.qgis.toggle_snapping(False)

    def refreshLayer(self):
        if self.focusedLayer is None:
            return
        self.controller.qgis.refresh_layer(self.focusedLayer)     

    def open(self,**kwargs):
        current = self.controller.iface.layerTreeView().currentLayer()
        self.setFocusedLayer(current)

    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.controller.iface.layerTreeView().currentLayerChanged.connect(self.setFocusedLayer)

        self.get("ReturnButton").clicked.connect(self.returnToSession)
        self.get("StartEdit").clicked.connect(self.start_edit)
        self.get("Commit").clicked.connect(self.commit)
        self.get("CancelButton").clicked.connect(self.cancelChanges)
        self.get("Snapping").stateChanged.connect(self.on_snap_toggle)
        self.get("Refresh").clicked.connect(self.refreshLayer)

        self.get("Edit").clicked.connect(self.editMode)
        self.get("Draw").clicked.connect(self.drawMode)