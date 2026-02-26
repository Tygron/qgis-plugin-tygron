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


    def open(self,**kwargs):
        self.overlayTypes = self.controller.client.constants.OVERLAYS_TYPE

        combo = self.get("TypeSelect")
    
        if combo:
            combo.clear()
            combo.addItems(self.overlayTypes)
        


    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller
        self.get("Return").clicked.connect(self.returnToOverview)

