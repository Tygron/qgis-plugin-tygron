class ProjectSelectionPage:

    widget = None
    controller = None
    pageIndex = 2
    instancePrefix = "ProjectSelection"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)
    
    
    def onSelection(self):
        project_name = self.get("Input").text()
        comment_label = self.get("CommentLabel")
        running_session = self.controller.client.check_if_session_exists_for_project(project_name)

        if running_session:

            session_id = running_session.get("sessionID")
            joinSuccess = self.controller.client.session.join_live_session(session_id)
            if not joinSuccess:
                comment_label.setText("Could not join session!")
            else:
                self.controller.switch_to_page(self.controller.session)

        else:
            # attempt to wake session
            comment_label.setText("Waking up project...")
            joinSuccess = self.controller.client.session.start_and_join_inactive_session(project_name)
            if not joinSuccess:
                comment_label.setText("Could not create or join session!")
            else:
                #goto session screen
                self.controller.switch_to_page(self.controller.session)
                
    def returnToHome(self):
        self.controller.switch_to_page(self.controller.home)

    def open(self,presetProjectName=None,**kwargs):
        self.get("CommentLabel").setText("")

        if presetProjectName:
            self.get("Input").setText(presetProjectName)


    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.get("Button").clicked.connect(self.onSelection)
        self.get("ReturnButton").clicked.connect(self.returnToHome)