class FromTemplate:

    widget = None
    controller = None

    pageIndex = 8
    instancePrefix = "FromTemplate"

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
 