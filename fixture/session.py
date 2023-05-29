from selenium.webdriver.common.by import By


class SessionHelper:
    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd
        self.app.open_home_page()

        wd.find_element(By.NAME, "username").click()
        wd.find_element(By.NAME, "username").clear()
        wd.find_element(By.NAME, "username").send_keys(username)
        wd.find_element(By.NAME, "password").click()
        wd.find_element(By.NAME, "password").clear()
        wd.find_element(By.NAME, "password").send_keys(password)
        wd.find_element(By.XPATH, "//input[@value='Login']").click()

    def ensure_login(self, username, password):
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:  # is logged in by another user
                self.logout()
        self.login(username, password)

    def is_logged_in(self):
        wd = self.app.wd
        # check if there are logout links on the page
        return len(wd.find_elements(By.LINK_TEXT, "Logout")) > 0

    def is_logged_in_as(self, username):
        # check if there are correct username in the top of the page
        return self.get_logged_username() == username

    def get_logged_username(self):
        wd = self.app.wd
        return wd.find_element(By.XPATH, "//td[@class='login-info-left']/span[1]").text

    def logout(self):
        wd = self.app.wd
        wd.find_element(By.LINK_TEXT, "Logout").click()
        # wait for appearance of login form
        wd.find_element(By.NAME, "username")

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()
