from telnetlib import Telnet


class JamesHelper:

    def __init__(self, app):
        self.app = app

    def ensure_user_exists(self, username, password):
        james_config = self.app.config["james"]
        session = JamesHelper.Session(
            james_config["host"], james_config["port"], james_config["username"], james_config["password"])
        if session.is_user_registered(username):
            session.reset_password(username, password)
        else:
            session.create_user(username, password)
        session.quit()

    class Session:

        def __init__(self, host, port, username, password):
            # open telnet session
            self.telnet = Telnet(host=host, port=port, timeout=5)
            # read until receive message about login
            self.read_until("Login id:")
            # write login for telnet session (root)
            self.write(username + "\n")
            # read until receive message about password
            self.read_until("Password:")
            # write password for telnet session (root)
            self.write(password + "\n")
            # read until receive message about success
            self.read_until("Welcome root. HELP for a list of commands")

        # helper to read string in bytes
        def read_until(self, text):
            self.telnet.read_until(text.encode('ascii'), timeout=5)

        # helper to write string in bytes
        def write(self, text):
            self.telnet.write(text.encode('ascii'))

        def is_user_registered(self, username):
            self.write(f"verify {username}\n")
            # b - convert string to bytes
            res = self.telnet.expect([b"exists", b"does not exist"])
            # if find 'exists', then return 0 in first part of result, if find 'does not exist' - return 1
            return res[0] == 0

        def create_user(self, username, password):
            self.write(f"adduser {username} {password}\n")
            self.read_until(f"User {username} added")

        def reset_password(self, username, password):
            self.write(f"setpassword {username} {password}\n")
            self.read_until(f"Password for {username} reset")

        def quit(self):
            self.write("quit\n")
