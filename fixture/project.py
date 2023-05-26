from selenium.webdriver.common.by import By

from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def get_projects_list(self):
        wd = self.app.wd
        self.open_projects_page()

        projects = []
        table = wd.find_elements(By.XPATH, "//table[@class= 'width100']")[1]
        rows = table.find_elements(By.TAG_NAME, "tr")[2:]
        for row in rows:
            td0 = row.find_elements(By.TAG_NAME, "td")[0]
            name = td0.find_element(By.TAG_NAME, "a").text
            description = row.find_elements(By.TAG_NAME, "td")[4].text
            projects.append(Project(name=name, description=description))

        return projects

    def add_project(self, project):
        self.open_projects_page()
        self.click_new_project_button()
        self.fill_project_form(project)
        self.click_add_project_button()
        self.click_proceed_link()

    def open_projects_page(self):
        wd = self.app.wd
        menu = wd.find_element(By.XPATH, "//td[@class='menu']")
        menu.find_element(By.LINK_TEXT, "Manage").click()
        wd.find_element(By.LINK_TEXT, "Manage Projects").click()

    def click_new_project_button(self):
        wd = self.app.wd
        wd.find_element(By.XPATH, "//input[@value='Create New Project']").click()

    def fill_project_form(self, project):
        self.change_field_value("name", project.name)
        self.change_field_value("description", project.description)

    def change_field_value(self, element_name, text):
        wd = self.app.wd
        element = wd.find_element(By.NAME, element_name)
        element.click()
        element.clear()
        element.send_keys(text)

    def click_add_project_button(self):
        wd = self.app.wd
        wd.find_element(By.XPATH, "//input[@value='Add Project']").click()

    def click_proceed_link(self):
        wd = self.app.wd
        wd.find_element(By.LINK_TEXT, "Proceed").click()
