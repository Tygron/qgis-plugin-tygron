from qgis.PyQt.QtWidgets import QComboBox,QTabWidget,QPushButton,QLineEdit,QWidget, QHBoxLayout,QVBoxLayout, QLabel,QSpacerItem,QScrollArea,QSizePolicy
from tygron.TygronClient.constants import *
from qgis.utils import plugins
from pathlib import Path

plugin_name = "qgis-plugin-tygron"

def makeEntryForAttribute(attributeName: str, defaultValue: any, parent_widget: QWidget):
    row_container = QWidget(parent_widget)
    layout = QHBoxLayout(row_container)
    
    label = QLabel(attributeName, row_container)
    
    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    
    line_edit = QLineEdit(row_container)
    line_edit.setText(str(defaultValue) if defaultValue is not None else "")
    line_edit.setObjectName(attributeName)
    layout.addWidget(label)
    layout.addItem(spacer) 
    layout.addWidget(line_edit)

    layout.setContentsMargins(5, 2, 5, 2)

    return row_container,line_edit
    


def buildings(dialog, layer, feature):   
    tab_widget = dialog.findChild(QTabWidget, "tabWidget")
    combo = dialog.findChild(QComboBox, "function")
    typesCombo = dialog.findChild(QComboBox,"type")
    nameEntry = dialog.findChild(QLineEdit, "name")

    stakes = dialog.findChild(QComboBox, "owner")
    submitBtn = dialog.findChild(QPushButton, "submitButton")

    attributeTabs = dialog.findChild(QTabWidget,"attributeTabs")

    possible_fields = layer.fields().names()
    main_plugin = plugins.get(plugin_name)
    all_functions = main_plugin.client.constants.FUNCTIONS_TYPE
    all_types = main_plugin.client.constants.BUILDING_TYPES
    attribute_cat = main_plugin.client.constants.BUILDING_ATTRIBUTE_GROUPING


    chosen_function = ""
    function_data = None
    function_ids = {}
    function_codes = []

    extra_attributes = {}

    new_id = main_plugin.client.apiGet(url=f"session/items/buildings/size/?f=JSON&token={main_plugin.client.session.api_key}")

    #print(new_id)


    def get(instanceName):
        return getattr(dialog,instanceName, None)
    
    def submitData():
        
        print("Submitting values")
        
        feature["function"] = combo.currentText()
        feature["owner"] = stakes.currentText()
        feature["name"] = nameEntry.text()
        feature["type"] = typesCombo.currentText()
        feature["id"] = new_id

        for index in extra_attributes.keys():
            value = extra_attributes[index].text()
            feature.setAttribute(index, value)
        
    def loadAttributes():
        nonlocal function_data
        attributeTabs.clear()
        extra_attributes.clear()

        for category_name in attribute_cat.keys():
            new_tab = QWidget()
            tabLayout = QVBoxLayout(new_tab)
            tabLayout.setContentsMargins(0, 0, 0, 0)

            scrollbox = QScrollArea()
            scrollbox.setWidgetResizable(True) 
            tabLayout.addWidget(scrollbox)

            scrollContent = QWidget()
            contentLayout = QVBoxLayout(scrollContent)
            
            for attribute in attribute_cat[category_name]:
                if attribute in possible_fields:
                    index = possible_fields.index(attribute)
                    raw_val = function_data["attributes"].get(attribute,"NULL")
                    default_value = (raw_val[0] if isinstance(raw_val, list) else raw_val) 

                    if default_value is not None: 
                        subvalue, line_edit = makeEntryForAttribute(attribute, default_value, scrollContent)
                        
                        extra_attributes[index] = line_edit
                        contentLayout.addWidget(subvalue)

            contentLayout.addStretch()
            scrollbox.setWidget(scrollContent)

            attributeTabs.addTab(new_tab, category_name)      

    
    def on_tab_changed(index):
        nonlocal chosen_function
        nonlocal function_data

        tab_name = tab_widget.tabText(index)
        #print(f"Tab gewisseld naar index {index}: {tab_name}")
        
        if tab_name != "General":
            selection = combo.currentText()
            if selection != chosen_function:
                chosen_function = selection
                # update values
                functionId = function_ids[selection]
                function_data = main_plugin.client.apiGet(url = f"session/items/functions/{functionId}/?crs=3857&f=JSON&token={main_plugin.client.session.api_key}")

                print(function_data["attributes"])
                print("------")
                print(possible_fields)

                submitData()
                loadAttributes()

                

    fields = layer.fields()
    stakeholders = []

    for item in all_functions:
        functionCode = f"{item.get("id")}_{item.get("name")}"

        function_ids[functionCode] = item.get("id")
        function_codes.append(functionCode)

    for stakeholder in main_plugin.client.session.stakeholders:
        stakeholders.append(f"{stakeholder.get("id")}_{stakeholder.get("name")}")

    
    if combo:
        combo.clear()
        combo.addItems(function_codes)
        
        val = feature.attribute("function")
        if val: 
            combo.setCurrentText(str(val))

    if typesCombo:
        typesCombo.clear()
        typesCombo.addItems(all_types)
        
        val = feature.attribute("type")
        if val: 
            typesCombo.setCurrentText(str(val))

    if stakes:
        stakes.clear()
        stakes.addItems(stakeholders)
        
        val = feature.attribute("owner")
        if val: 
            stakes.setCurrentText(str(val))

    submitBtn.clicked.connect(submitData)
    tab_widget.currentChanged.connect(on_tab_changed)

    
    