from ..TygronClient.client import *
from ..qgisController import QGISController

from .homePage import HomePage
from .login import LoginPage
from .projectSelection import ProjectSelectionPage
from .session import SessionPage
from .overlays import OverlaysPage
from .layers import LayersPage
from .newProjectChoice import NewProjectChoicePage
from .newProject import NewProject
from .fromTemplate import FromTemplate
from .apiEntry import APIEntryPage
from .measures import MeasuresPage
from .measureOverview import MeasureOverviewPage
from .overlaysOverview import OverlaysOverviewPage
import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog,QSizePolicy
from qgis.gui import (
    QgsMessageBar,
)
from qgis.core import Qgis
source = os.path.dirname(os.path.dirname(__file__)) 
test_input_prompt, _ = uic.loadUiType(os.path.join(source, 'testapiprompt.ui'))
test_result_prompt, _ = uic.loadUiType(os.path.join(source, 'testresults.ui'))

class TestAPIInputDialog(QDialog, test_input_prompt):
    def __init__(self, plugin ,parent=None):
        super().__init__(parent)

        #self.bar = QgsMessageBar(self)
        #self.bar.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )

        self.setupUi(self)
        self.parent = parent
        self.plugin = plugin
        self.pushButton.clicked.connect(self.onClick)

    def loadWFSTTest(self):
        return True

   

    def runTest(self):
        testResults = {
            "WFS-T Loading": self.loadWFSTTest(),
        }

        resultString = ""

        for task in testResults.keys():
            if testResults[task]: 
                result ="✅" 
            else:
                result = "❌"
            resultString += f"{task}: {result}"

        return resultString

    def onClick(self):
        apiKey = self.lineEdit.text().strip()
        success = self.plugin.controller.client.session.validate_session(apiKey)
        if not success:
            self.bar.pushMessage("Error", "Could not find session, please check your API Key", level=Qgis.Critical)
        else:
            testResult = self.runTest()
            if testResult:
                TestResultDialog(self.plugin,self.parent,testResult).exec_()

class TestResultDialog(QDialog, test_result_prompt):
    def __init__(self, plugin,parent=None,results = ""):
        super().__init__(parent)
        self.setupUi(self)
        self.plugin = plugin
        self.results.setText(results)
        

         
        

class widgetController:

    widget = None
    openPage = None

    def get(self,instanceName):
        return getattr(self.widget,f"{instanceName}", None)

    def __init__(self,plugin):
        self.widget = plugin.dockwidget
        self.iface = plugin.iface
        self.plugin = plugin

        # create objects for other pages
        self.login = LoginPage(self.widget,self)
        self.home = HomePage(self.widget,self)
        self.apiEntry = APIEntryPage(self.widget,self)
        self.openProject = ProjectSelectionPage(self.widget,self)
        self.session = SessionPage(self.widget,self)
        self.overlays = OverlaysPage(self.widget,self)
        self.layers = LayersPage(self.widget,self)
        self.newProjectChoice = NewProjectChoicePage(self.widget,self)
        self.newProject = NewProject(self.widget,self)
        self.fromTemplate = FromTemplate(self.widget,self)
        self.measures = MeasuresPage(self.widget,self)
        self.measureOverview = MeasureOverviewPage(self.widget,self)
        self.overlaysOverview = OverlaysOverviewPage(self.widget,self)

        self.client = plugin.client
        self.qgis = QGISController(self.widget,self.iface)

        self.get("TestButton").clicked.connect(self.setup_test)
        self.start()

    def switch_to_page(self,instance,**kwargs):
        if (instance == None):
            return

        self.widget.stackedWidget.setCurrentIndex(instance.pageIndex)
        self.openPage = instance
        instance.open(**kwargs)

    def start(self):
        self.switch_to_page(self.apiEntry)

    def setup_test(self):
        TestAPIInputDialog(self.plugin,self.widget).exec_()


    
    