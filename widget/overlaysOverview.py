from qgis.PyQt.QtWidgets import QPushButton, QVBoxLayout

class OverlaysOverviewPage:

    widget = None
    controller = None
    pageIndex = 12
    instancePrefix = "Overlays"

    overlayTypes = None

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)

    def returnToOverview(self):
        self.controller.switch_to_page(self.controller.session)

    def processAddOverlay(self):
        selected_option = self.get("TypeSelect").currentText()
        self.controller.client.session.add_overlay(selected_option)


    def open(self,**kwargs):
        self.overlayTypes = self.controller.client.constants.OVERLAYS_TYPE
        combo = self.get("TypeSelect")
        combo.clear()
        combo.addItems(self.overlayTypes)
            
        


    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller
        self.get("Return").clicked.connect(self.returnToOverview)
        self.get("Add").clicked.connect(self.processAddOverlay)

