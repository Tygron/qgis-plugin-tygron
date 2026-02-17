class NewProjectChoicePage:

    widget = None
    controller = None

    pageIndex = 6
    instancePrefix = "NoT"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)

    def returnToHome(self):
        self.controller.switch_to_page(self.controller.home)

    def newProject(self):
        self.controller.switch_to_page(self.controller.newProject)
    def fromTemplate(self):
        self.controller.switch_to_page(self.controller.fromTemplate)

    def open(self,**kwargs):
        pass

    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.get("ReturnButton").clicked.connect(self.returnToHome)
        self.get("NewButton").clicked.connect(self.newProject)
        self.get("FromTemplate").clicked.connect(self.fromTemplate)
