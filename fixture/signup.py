from selenium.webdriver.common.by import By
import re


class SignupHelper:

    def __init__(self, app):
        self.app = app

    def add_new_user(self, username, email, password):
        wd = self.app.wd

        # open page for new user and type their username and email
        wd.get(self.app.base_url + "/signup_page.php")
        wd.find_element(By.NAME, "username").send_keys(username)
        wd.find_element(By.NAME, "email").send_keys(email)
        wd.find_element(By.XPATH, "//input[@value='Signup']").click()

        mail = self.app.mail.get_mail(username, password, "[MantisBT] Account registration")
        url = self.extract_confirmation_url(mail)

        # open confirmation link and set the password
        wd.get(url)
        wd.find_element(By.NAME, "password").send_keys(password)
        wd.find_element(By.NAME, "password_confirm").send_keys(password)
        wd.find_element(By.XPATH, "//input[@value='Update User']").click()

    def extract_confirmation_url(self, text):
        # .* - any symbol repeated any times, $ - end of the line, MULTILINE - show that $ is end of the line
        return re.search("http://.*$", text, re.MULTILINE).group(0)
