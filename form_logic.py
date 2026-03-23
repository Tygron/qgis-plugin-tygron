from qgis.PyQt.QtWidgets import QComboBox
from tygron.TygronClient.constants import *
from qgis.utils import plugins


def buildings(dialog, layer, feature):    
    combo = dialog.findChild(QComboBox, "function")
    main_plugin = plugins.get('tygron')
    functions = main_plugin.client.constants.FUNCTIONS_TYPE

    to_list = []

    for item in functions:
        print(item)
        to_list.append(f"{item.get("id")}_{item.get("name")}")
    
    if combo:
        combo.clear()
        combo.addItems(to_list)
        
        if feature['function']:
            combo.setCurrentText(str(feature['function']))