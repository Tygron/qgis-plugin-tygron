import json

WMS_URL = "https://engine.tygron.com/web/wms"
WFS_URL = "https://engine.tygron.com/api/session/wfs"

class Session:

    api_key = None
    session_id = None
    in_session = False

    client = None
    project_name = None
    domain = None

    clients = []
    dimensions = {
        "min_x": 0,
        "min_y": 0,
        "max_x": 0,
        "max_y": 0,

        "anchor_x": 0,
        "anchor_y": 0,
    }

    # attempt to fetch data with api key to check validity
    def validate_session(self,key = None):
        self.api_key = key
        self.session_id = None
        
        if key is not None:
            # make api call to fetch data
            details = self.load_project_details()
            if details:
                self.session_id = details.get("id")

        self.in_session = self.session_id is not None

        return self.in_session


    # authenticate with login data to fetch api key with sessionId
    # connects authenticated account with session, must be disconnected later on.
    def join_live_session(self,sessionId):
        if not self.client.authenticated:
            return
        if sessionId is None:
            return
        
        payload = json.dumps([
            sessionId,
            "EDITOR",
        ])

        sessionToken = self.client.apiPost(
            url="event/io/join/?f=JSON",
            header=self.client.authentication_header,
            payload=payload)
        
        if sessionToken:
            self.api_key = sessionToken.get("apiToken")
            self.session_id = sessionId
            self.in_session = True

            return sessionToken

    def get_wms_uri(self, layer_name):
        return (
            f"authConfigId=&crs=EPSG:3857&dpiMode=7&format=image/png"
            f"&layers={layer_name}&styles=default"
            f"&url={WMS_URL}?token={self.api_key}"
    )
    def get_wfs_uri(self, type_name):
        params = [
            f"{WFS_URL}?token={self.api_key}",
            f"&typename={type_name}",
            "&version=1.1.0",
            "&override=true"
            "&srsname=EPSG:3857",
            "&ignoreAxisOrientation=1"
        ]
        return "".join(params)

    # starts session, does not join it yet.
    def start_inactive_session(self,project_name):
        if not self.client.authenticated:
            return
        if project_name is None:
            return
        
        payload = json.dumps([
            "EDITOR",
            project_name
        ])

        sessionId = self.client.apiPost(
            url="event/io/start/?f=JSON",
            header=self.client.authentication_header,
            payload=payload)
        
        return sessionId
    
    # start and join inactive session
    def start_and_join_inactive_session(self,project_name):
        if not self.client.authenticated:
            return
        if project_name is None:
            return
        
        sessionId = self.start_inactive_session(project_name)
        if sessionId is None:
            return
        
        return self.join_live_session(sessionId)

    def clear_credentials(self):
        self.in_session = False
        self.api_key = None
        self.session_id = None

    # disconnects logged in client from session
    # no use if connected solely through api key
    def leave(self):
        if not self.client.authenticated:
            return

        if not self.in_session:
            return
        
        payload = json.dumps([self.session_id,self.api_key,False,])

        success = self.client.apiPost(
            url="event/io/close/?f=JSON",
            header=self.client.authentication_header,
            payload=payload)
        
        if success is not None:
            self.clear_credentials()
            return True
        
    def load_project_details(self):
        session_data = self.client.apiGet(url=f"session/info/?f=JSON&token={self.api_key}")

        if session_data:
            self.project_name = session_data.get("name")
            self.domain = session_data.get("projectDomain")
            return session_data

    # disconnects logged in client from session
    # fully closes session on server, project will have to be restarted to join again
    # kicks out other clients
    # no use if connected solely through api key
    def kill(self):
        if not self.in_session:
            return
        
        payload = json.dumps([self.session_id,])

        success = self.client.apiPost(
            url="event/io/kill/?f=JSON",
            header=self.client.authentication_header,
            payload=payload)
                
        if success is not None:
            self.clear_credentials()
            return True


    def set_api_key(self,newKey = None):
        self.api_key = newKey

    def set_session_id(self,newId = None):
        self.session_id = newId

    def set_dimensions(self,**kwargs):
        self.dimensions.update(kwargs)

    def __init__(self,parentClass):
        self.client = parentClass