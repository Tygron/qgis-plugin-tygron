class APIEntryPage:

    widget = None
    controller = None
    pageIndex = 9
    instancePrefix = "TokenEntry"

    def get(self,instanceName):
        return getattr(self.widget,f"{self.instancePrefix}{instanceName}", None)

    # attempt to fetch data with api key
    def onValidate(self):
        # strip slop from the string
        key = self.get("KeyEntry").text().strip()

        success = self.controller.client.session.validate_session(key)

        if (not success):
            self.controller.qgis.ErrorMessage("Could not validate token!")
        else:
            self.controller.switch_to_page(self.controller.session)


    def open(self,**kwargs):
        pass

    def __init__(self,widget,controller):
        self.widget = widget
        self.controller = controller

        self.get("Validate").clicked.connect(self.onValidate)