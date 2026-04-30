from qgis.PyQt.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtCore import QDateTime, QDate
from qgis.core import QgsProject

def convertToQDateTime(input):
    format_string = "dd/MM HH:mm:ss"
    q_date_time = QDateTime.fromString(input, format_string)

    current_year = QDate.currentDate().year() 
    q_date_time.setDate(QDate(current_year, q_date_time.date().month(), q_date_time.date().day()))
    return q_date_time

api_defaults = []

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

        self.reloadOverlays()

    def import_temporal_overlay(self,overlay):
        name = overlay.get("name")
        title = overlay.get("title")
        timestamps = overlay.get("timestamps")

        root = QgsProject.instance().layerTreeRoot()
        group = root.insertGroup(0, title)

        for iteration in timestamps:
            subLayer = timestamps[iteration]

            dateTime = subLayer.get("date")
            endTime = dateTime.addSecs(3600)
            nextLayer = timestamps.get(iteration+1,None)
            if nextLayer is not None:
                endTime = nextLayer.get("date",endTime)

            self.controller.qgis.refreshWmsCache(f"https://engine.tygron.com/web/wms?token={self.controller.client.session.api_key}")
            result= self.controller.client.apiGet(url=f"https://engine.tygron.com/web/wms?REQUEST=GetCapabilities&token={self.controller.client.session.api_key}")
            uri = self.controller.client.session.get_wms_uri(f"{name}-{iteration}")
            layer = self.controller.qgis.loadWMSLayer(uri,f"{title} - i{iteration}")

            self.controller.qgis.enable_temporal_layer(layer,dateTime,endTime)
            group.addChildNode(root.findLayer(layer.id()))
            

    def import_overlay(self,overlay):
        name = overlay.get("name")
        title = overlay.get("title")

        self.controller.qgis.refreshWmsCache(f"https://engine.tygron.com/web/wms?token={self.controller.client.session.api_key}")
        result= self.controller.client.apiGet(url=f"https://engine.tygron.com/web/wms?REQUEST=GetCapabilities&token={self.controller.client.session.api_key}")
        uri = self.controller.client.session.get_wms_uri(name)
        self.controller.qgis.loadWMSLayer(uri,title)

    def selectOverlay(self,overlay):
        if overlay.get("timestamps",None) is not None:
            self.import_temporal_overlay(overlay)
        else:
            self.import_overlay(overlay)
        

    def sort_overlays(self,available_list):
        available_overlays = self.controller.client.session.fetch_available_overlays()
        standard_layers = self.controller.client.constants.DEFAULT_OVERLAYS

        timestamps = {}
        endlist = {}

        for overlay in available_overlays:
            identifiable = overlay.get("name")

            if identifiable in standard_layers:
                endlist[identifiable] = {"title":overlay.get("title"),"name":overlay.get("name")}
                continue

            dash = identifiable.find("-")
            if (dash>-1):
                iteration = identifiable[dash+1:]
                identifiable = identifiable[0:dash]

                if timestamps.get(identifiable,None) is None:
                    timestamps[identifiable] = {}
                timestamps[identifiable][int(iteration)] = {"date":"","title":overlay.get("title")}
            else:
                endlist[identifiable] = {"title":overlay.get("title"),"name":overlay.get("name")}
        
        for id in timestamps.keys():

            fullName = endlist[id].get("title")

            for iteration in timestamps[id]:
                entry = timestamps[id][iteration]
                entry["date"] = convertToQDateTime(entry["title"].replace(str(fullName),"")[2:-1])

            endlist[id]["timestamps"] = timestamps[id]


        return endlist

                

            



            


    def reloadOverlays(self):

        # remove existing buttons from container
        container = self.get("ContainerLayout")
        layout = container.layout()
        self.controller.qgis.clearContainer(layout)

        available_overlays = self.sort_overlays(self.controller.client.session.fetch_available_overlays())
        print(available_overlays)
        for overlayId in available_overlays:
            overlay = available_overlays[overlayId]
            btn = QPushButton(f"{overlay.get("title")} ({overlay.get("name")})")
        
            btn.clicked.connect(lambda _, overlay=overlay: self.selectOverlay(overlay))   

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

