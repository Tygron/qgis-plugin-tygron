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

class widgetController:

    widget = None
    openPage = None

    def __init__(self,plugin):
        self.widget = plugin.dockwidget
        self.iface = plugin.iface

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

        self.client = plugin.client
        self.qgis = QGISController(self.widget,self.iface)

        self.start()

    def switch_to_page(self,instance,**kwargs):
        if (instance == None):
            return

        self.widget.stackedWidget.setCurrentIndex(instance.pageIndex)
        self.openPage = instance
        instance.open(**kwargs)

    def start(self):
        self.switch_to_page(self.apiEntry)


    
    