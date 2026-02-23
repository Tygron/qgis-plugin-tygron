from qgis.PyQt.QtWidgets import QPushButton, QVBoxLayout

class MeasureOverviewPage:

    widget = None
    controller = None
    pageIndex = 11
    instancePrefix = "MOverview"
    activeMeasure = None

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)

    def returnToOverview(self):
        self.controller.switch_to_page(self.controller.measures)

    def open(self,measureId = 0,**kwargs):
       self.activeMeasure = self.controller.client.session.fetch_measure_data(measureId)
       
       if self.activeMeasure is not None:
           self.get("Label").setText(f"{self.activeMeasure.get("name")} - ID: {self.activeMeasure.get("id")}")

       



    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller
        self.get("Return").clicked.connect(self.returnToOverview)

