class NewProject:

    widget = None
    controller = None

    pageIndex = 7
    instancePrefix = "NewProject"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)

    def returnToHome(self):
        self.controller.switch_to_page(self.controller.home)

    def open(self,**kwargs):
        pass

    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.get("ReturnButton").clicked.connect(self.returnToHome)
