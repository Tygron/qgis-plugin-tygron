import base64
import json
import requests
from .session import Session
from . import constants

ROOT_URL = "https://engine.tygron.com/api/"

class TygronClient():

    username = None
    login_key = None
    authentication_header = None
    authenticated = False
    constants = constants
    account_details = {
        "last_project": None,
        "first_name": None,
    }

    session = None

    def _process_fetch(self,response):
        if response.status_code == 200 or response.status_code == 204:
            try:
                return response.json()
            except:
                return response
        else:
            print(f"Error {response.status_code}")
            return None

    def _url(self,append):
        return f"{ROOT_URL}{append}"
    
    def apiGet(self,url = None,payload = None,header = False,raw_url = False):
        urlToSend = self._url(url)
        if raw_url:
            urlToSend = url

        return self._process_fetch(requests.get(urlToSend,headers=header,data=payload))
    
    def apiPost(self,url = None,payload = None,header = False, raw_url = False):
        urlToSend = self._url(url)
        if raw_url:
            urlToSend = url
            
        return self._process_fetch(requests.post(urlToSend,headers=header,data=payload))
        
    def log_in(self,username,password):
        if not (username and password):
            return
        
        # auth argument of request didnt work so whatever bro
        auth_header = {"Authorization":f"Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}"}

        loginKey = self.apiPost(url="event/user/get_my_login_key/?f=JSON",header=auth_header)
        if loginKey:
            self.username = username
            self.login_key = loginKey
            self.authentication_header = {"Authorization":f"Basic {base64.b64encode(f"{username}:{loginKey}".encode()).decode()}"}
            self.authenticated = True

        return self.authenticated
    
    def log_out(self):
        self.username = None
        self.login_key = None
        self.authentication_header = None
        self.authenticated = False

    def fetch_account_details(self):
        if not self.authenticated:
            return
        
        accountData = self.apiGet("myuser/?f=JSON",header=self.authentication_header)
        if accountData:
            self.account_details["last_project"] = accountData.get("recentProjects",[])[0]
            self.account_details["first_name"] = accountData.get("firstName")
        
        return self.account_details

    def fetch_sessions(self):
        if not self.authenticated:
            return
        
        return self.apiGet(url="sessions/?f=JSON",header=self.authentication_header)


    def check_if_session_exists_for_project(self,project_name):
        if not self.authenticated:
            return
        if project_name is None:
            return
        
        sessionList = self.fetch_sessions()
        if sessionList is None:
            return
        
        for session in sessionList:
            name = session.get("name","")
            if name == project_name:
                return session

    def __init__(self):
        self.session = Session(self)
        
    


    