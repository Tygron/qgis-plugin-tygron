from qgis.PyQt.QtWidgets import QPushButton, QVBoxLayout

class MeasuresPage:

    widget = None
    controller = None
    pageIndex = 10
    instancePrefix = "Measures"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)

    def returnToSession(self):
        self.controller.switch_to_page(self.controller.session)

    def createMeasure(self):
        self.controller.client.session.add_measure_layer(0)
        self.open()
        
    def clearContainer(self,layout):
        # Clear existing buttons so they don't stack up
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def select_measure(self,measureId):
        if measureId is None:
            return
        
        self.controller.switch_to_page(self.controller.measureOverview,measureId = measureId)


    def open(self,**kwargs):
        measures = self.controller.client.session.fetch_measures()

        container = self.get("Widget")
        layout = container.layout()

        self.clearContainer(layout)

        for _m in measures:
            btn = QPushButton(f"{_m.get("name")} ({_m.get("id")})")
        
            btn.clicked.connect(lambda _, m_id=_m.get("id"): self.select_measure(m_id))   

            layout.addWidget(btn)

       



    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller
        self.get("Return").clicked.connect(self.returnToSession)
        self.get("Button").clicked.connect(self.createMeasure)

