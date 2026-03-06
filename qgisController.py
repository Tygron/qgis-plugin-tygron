from qgis.core import ( # type: ignore
    QgsCategorizedSymbolRenderer, 
    QgsRendererCategory, 
    QgsFillSymbol,
    QgsVectorDataProvider,
    QgsRasterLayer, 
    QgsProject, 
    QgsRectangle,
    QgsVectorLayer,
    QgsTask, 
    QgsApplication,
    QgsSettings,
    Qgis
)  

from qgis.PyQt.QtGui import QColor # type: ignore
from qgis.PyQt.QtWidgets import QInputDialog # type: ignore
import random,os

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
                print(f"Applied style: {style_name}")
            else:
                print(f"Failed to apply style: {message}")
        else:
            print(f"Style file not found at: {style_path}")

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
        if layer.isValid():
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
            print("Layer is now editable. Move a polygon to test!")
        else:
            print("This WFS provider doesn't seem to allow editing.")

    def select_option(self,text = "Choose Option:",options = ["Yes","No"]):
        item, ok = QInputDialog.getItem(
            self.widget, "Select", text, 
            options, 0, False
        )
        
        if ok and item:
            return item
        return options[0]

    def commit_layer_edits(self, layer):
        if layer.isEditable():
            success = layer.commitChanges()
            
            if not success:
                print(f"Error saving: {layer.commitErrors()}")
                layer.rollBack()

    def loadWFSVector(self,uri,QGISName,callback = None):
        def run():
            return QgsVectorLayer(uri, QGISName, "wfs")
        def complete(result):
            self.addLayer(result)
            if callback is not None:
                callback(result)

            if task in self.tasks:
                self.tasks.remove(task)
        
        task = PluginTask(f"Loading WFS: '{QGISName}'",run,complete)
        self.tasks.append(task)
        QgsApplication.taskManager().addTask(task)

    def loadWMSLayer(self,uri,QGISName):
        layer = QgsRasterLayer(uri, QGISName, "wms")
        self.addLayer(layer)

