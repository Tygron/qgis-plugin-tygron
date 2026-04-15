from qgis.core import ( # type: ignore
    QgsCategorizedSymbolRenderer, 
    QgsRendererCategory, 
    QgsFillSymbol,
    QgsVectorDataProvider,
    QgsRasterLayer, 
    QgsProject, 
    QgsVectorLayer,
    QgsTask, 
    QgsApplication,
    QgsSettings,
    Qgis,
    QgsEditFormConfig,
    QgsNetworkAccessManager, 
    QgsNetworkReplyContent
)  

from qgis.PyQt.QtWidgets import QMessageBox,QInputDialog # type: ignore
from qgis.PyQt.QtCore import QTimer,QUrl, QEventLoop # type: ignore
from qgis.PyQt.QtGui import QColor # type: ignore
from PyQt5.QtNetwork import QNetworkRequest
import random,os,time

plugin_dir = os.path.dirname(__file__)

logic_path = os.path.normpath(os.path.join(plugin_dir, "form_logic.py")).replace("\\", "/")

class PluginTask(QgsTask):
    def __init__(self, description, background_fn, callback_fn=None):
        super().__init__(description, QgsTask.CanCancel)
        self.background_fn = background_fn
        self.callback_fn = callback_fn     
        self.data = None

    def run(self):
        try:
            self.data = self.background_fn()
            return True
        except Exception as e:
            print(f"Task failed: {e}")
            return False
    
    def finished(self, result):
        if result and self.callback_fn:
            self.callback_fn(self.data)

class QGISController():

    def ErrorMessage(self,text):
        self.iface.messageBar().pushMessage(
            "Error", 
            text, 
            level=Qgis.Critical, 
            duration=5
        )

    def clearContainer(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def apply_style_to_layer(self, layer, style_name="Buildings"):
        style_path = self.get_style_path(style_name)
        
        if os.path.exists(style_path):
            success, message = layer.loadNamedStyle(style_path)
            
            if success:
                layer.triggerRepaint()
                if self.controller.iface:
                    self.controller.iface.layerTreeView().refreshLayerSymbology(layer.id())
                    return
        print(f"Could not load style {style_name}")
        

    def get_style_path(self, style_name):
        plugin_dir = os.path.dirname(__file__)
        return os.path.join(plugin_dir, 'LayerStyles', f'{style_name}.qml')

    def save_credentials(self, username, password):
        settings = QgsSettings()
        settings.setValue("tygron/username", username)
        settings.setValue("tygron/password", password)

    def load_credentials(self):
        settings = QgsSettings()
        username = settings.value("tygron/username", "")
        password = settings.value("tygron/password", "")
        return username, password

    def __init__(self,widget,iface):
        self.tasks = []
        self.widget = widget
        self.iface = iface
        pass

    def addLayer(self,layer):
        print(layer.isValid())
        
        if True: #layer.isValid():
            
            QgsProject.instance().addMapLayer(layer)
            return layer
        
    def classify(self, layer, field_name='function'):
        field_index = layer.fields().indexFromName(field_name)
        if field_index == -1:
            print(f"Field {field_name} not found!")
            return

        unique_values = layer.uniqueValues(field_index)
        
        categories = []
        for value in unique_values:
            symbol = QgsFillSymbol.createSimple({'outline_color': 'black'})
            
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            symbol.setColor(color)
            
            category = QgsRendererCategory(value, symbol, str(value))
            categories.append(category)

        renderer = QgsCategorizedSymbolRenderer(field_name, categories)
        layer.setRenderer(renderer)
        layer.setOpacity(0.15)
        
        layer.triggerRepaint()
        self.iface.layerTreeView().refreshLayerSymbology(layer.id())


    def make_layer_editable(self, layer):
        if layer.dataProvider().capabilities() & QgsVectorDataProvider.EditingCapabilities:
            layer.startEditing()
        else:
            print("WFS Can not be edited")

    def select_option(self,text = "Choose Option:",options = ["Yes","No"]):
        item, ok = QInputDialog.getItem(
            self.widget, "Select", text, 
            options, 0, False
        )
        
        if ok and item:
            return item
        return options[0]

    def commit_layer_edits(self, layer):
        print("Comitting!")
        if layer.isEditable():
            print("Editable!")
            success = layer.commitChanges()
            print(success)
            if not success:
                print(f"Error saving: {layer.commitErrors()}")
                layer.rollBack()

    def loadWFSVector(self, uri, QGISName, callback=None):
        def run():
            time.sleep(0.1) 
            return True
        
        def complete(success):
            if success:
                layer = QgsVectorLayer(uri, QGISName, "wfs")
                
                if layer.isValid():
                    self.addLayer(layer)
                    if callback is not None:
                        QTimer.singleShot(100, lambda: callback(layer))
                else:
                    print(f"Failed to load WFS layer {QGISName}")

            if task in self.tasks:
                self.tasks.remove(task)
        
        task = PluginTask(f"Loading WFS: '{QGISName}'", run, complete)
        self.tasks.append(task)
        QgsApplication.taskManager().addTask(task)

    def validate_layer_changes(self,layer):
        for feature in layer.getFeatures():
            if not feature.geometry().isGeosValid():
                self.ErrorMessage("Could not submit layer changes!")
                return False
        return True
    
    def enable_topology(self):
        project = QgsProject.instance()    
        project.setTopologicalEditing(True)

    def confirmBox(self,mainText = "Are you sure?",subText = ""):
        reply = QMessageBox.question(
            self.widget, 
            mainText,
            subText,
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )

        return reply == QMessageBox.Yes

    def reload_target_wms(self, name):
        layers = QgsProject.instance().mapLayersByName(name)
        if layers:
            wms_layer = layers[0]
            wms_layer.triggerRepaint() 
            print(f"Refreshed WMS Layer: {name}")

    def refreshWmsCache(self, wms_url):

        capabilities_url = f"{wms_url}&SERVICE=WMS&REQUEST=GetCapabilities"
        
        nam = QgsNetworkAccessManager.instance()
        request = QNetworkRequest(QUrl(capabilities_url))
        
        request.setAttribute(QNetworkRequest.CacheLoadControlAttribute, QNetworkRequest.AlwaysNetwork)
        
        loop = QEventLoop()
        reply = nam.get(request)
        reply.finished.connect(loop.quit)
        loop.exec_()
        
    def fetch_attributeForm(self,formName):
        if not formName:
            return
        plugin_dir = os.path.dirname(__file__)
        return os.path.join(plugin_dir, 'AttributeForms', f'{formName}.ui')
    
    def setLayerForm(self,layer,formName):
        config = layer.editFormConfig()
        config.setInitFunction("buildings_form_init")



    def loadWMSLayer(self,uri,QGISName):
        print(f"Loading new layer {QGISName} at {uri}")
        layer = QgsRasterLayer(uri, QGISName, "wms")
        print(layer)
        self.addLayer(layer)
        return layer

    def setup_custom_ui(self,fileName,layer):
        ui_path = os.path.normpath(os.path.join(plugin_dir, "AttributeForms", f"{fileName}.ui"))
        ui_path = ui_path.replace("\\", "/")
        config = layer.editFormConfig()
        
        config.setLayout(QgsEditFormConfig.UiFileLayout)
        config.setUiForm(ui_path)

        config.setInitCodeSource(QgsEditFormConfig.CodeSourceFile)
        
        config.setInitFunction(fileName)
        config.setInitFilePath(logic_path)
        
        layer.setEditFormConfig(config)

        print("Loaded custom ui!")

