from ..TygronClient.client import *

class SessionPage:


    widget = None
    controller = None
    pageIndex = 3
    instancePrefix = "Session"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)

    def killProject(self):
        if self.controller.client.session.kill():
            self.controller.switch_to_page(self.controller.home)
    
    def returnToHome(self):
        if self.controller.client.session.leave():
            self.controller.switch_to_page(self.controller.home)

    def open(self,**kwargs):
        self.controller.client.session.load_project_details()

        self.get("NameLabel").setText(f"Session {self.controller.client.session.project_name} ({self.controller.client.session.domain})")

    def toOverlays(self):
        self.controller.switch_to_page(self.controller.overlays)
    def toLayers(self):
        self.controller.switch_to_page(self.controller.layers)

    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.get("ReturnButton").clicked.connect(self.returnToHome)
        self.get("KillButton").clicked.connect(self.killProject)
        self.get("Overlays").clicked.connect(self.toOverlays)
        self.get("LayerButton").clicked.connect(self.toLayers)

