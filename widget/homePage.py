class HomePage:

    widget = None
    controller = None

    pageIndex = 1

    def onLogout(self):
        self.controller.client.log_out()
        self.controller.switch_to_page(self.controller.login)

    def openProject(self):
        self.controller.switch_to_page(self.controller.openProject,presetProjectName = self.controller.client.account_details.get("last_project"))

    def newProject(self):
        self.controller.switch_to_page(self.controller.newProjectChoice)

    def updateLabels(self):
        details = self.controller.client.fetch_account_details()

        self.widget.HomeLabel.setText(f"Welcome, {details.get("first_name","User")}!")
        self.widget.HomeLastProjectLabel.setText(f"Last project: {details.get("last_project","-")}")

    def open(self,**kwargs):
        self.updateLabels()

    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.widget.LogoutButton.clicked.connect(self.onLogout)
        self.widget.HomeOpenProject.clicked.connect(self.openProject)
        self.widget.NewProjectButton.clicked.connect(self.newProject)