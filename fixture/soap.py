from suds.client import Client
from suds import WebFault

from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app
        self.client = Client(self.app.base_url + "api/soap/mantisconnect.php?wsdl")

    def can_login(self, username, password):
        try:
            self.client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self):
        projects_list = []
        username = self.app.config["webadmin"]['username']
        password = self.app.config["webadmin"]['password']

        try:
            projects_data = self.client.service.mc_projects_get_user_accessible(username, password)
        except WebFault:
            return None

        for project in projects_data:
            projects_list.append(Project(name=project["name"], description=project["description"]))

        return projects_list
