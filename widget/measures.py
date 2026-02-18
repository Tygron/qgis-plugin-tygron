class MeasuresPage:

    widget = None
    controller = None
    pageIndex = 10
    instancePrefix = "Measures"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)

    

    def open(self,**kwargs):
        pass

    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

