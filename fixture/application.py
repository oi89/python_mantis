from selenium import webdriver

from fixture.session import SessionHelper
from fixture.project import ProjectHelper


class Application:
    def __init__(self, browser, base_url):
        if browser == 'firefox':
            self.wd = webdriver.Firefox()
        elif browser == 'chrome':
            self.wd = webdriver.Chrome()
        else:
            raise ValueError(f"Unrecognized browser {browser}")

        self.base_url = base_url
        self.wd.implicitly_wait(5)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)

    def is_valid(self):
        try:
            # try to get current url; if done - fixture is valid
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        self.wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()
