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

    def selectOverlay(self,name):
        print(name)

    def reloadOverlays(self):

        # remove existing buttons from container
        container = self.get("ContainerLayout")
        layout = container.layout()
        self.controller.qgis.clearContainer(layout)

        available_overlays = self.controller.client.session.fetch_available_overlays()

        for overlay in available_overlays:
            btn = QPushButton(f"{overlay.get("title")} ({overlay.get("name")})")
        
            btn.clicked.connect(lambda _, name=overlay.get("name"): self.selectOverlay(name))   

            layout.addWidget(btn)
           


    def open(self,**kwargs):
        self.overlayTypes = self.controller.client.constants.OVERLAYS_TYPE
        combo = self.get("TypeSelect")
        combo.clear()
        combo.addItems(self.overlayTypes)
        self.reloadOverlays()
            
        


    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller
        self.get("Return").clicked.connect(self.returnToOverview)
        self.get("Add").clicked.connect(self.processAddOverlay)

