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

    def refresh_ui(self):
        if self.activeMeasure is not None:
            self.get("Label").setText(f"{self.activeMeasure.get("name")} - ID: {self.activeMeasure.get("id")}")
            self.get("Name").setText(f"{self.activeMeasure.get("name")}")

            self.get("Stakeholder").setText(f"test")

    def open(self,measureId = 0,**kwargs):
        self.activeMeasure = self.controller.client.session.fetch_measure_data(measureId)
        self.refresh_ui()
        

    def changeNameSubmit(self):
        new_name = self.get("Name").text()
        success = self.controller.client.session.change_measure_name(self.activeMeasure.get("id"),new_name)

        if success:
            self.activeMeasure["name"] = new_name
            self.refresh_ui()


       



    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller
        self.get("Return").clicked.connect(self.returnToOverview)
        self.get("ChangeName").clicked.connect(self.changeNameSubmit)

