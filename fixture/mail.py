import poplib
import email
import time


class MailHelper:

    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        for i in range(5):
            # open POP3 session with user and password
            pop = poplib.POP3(self.app.config["james"]["host"])
            pop.user(username)
            pop.pass_(password)

            emails_count = pop.stat()[0]
            if emails_count > 0:
                for n in range(emails_count):
                    # get email by index and then its body
                    msg_lines = pop.retr(n + 1)[1]
                    # convert each line from bytes to string and join them to the whole text
                    msg_text = "\n".join(map(lambda x: x.decode("utf-8"), msg_lines))
                    # get structure of email (subject, body)
                    message = email.message_from_string(msg_text)
                    if message.get("Subject") == subject:
                        pop.dele(n + 1)  # sign email for delete
                        pop.quit()  # save changes and close connection
                        return message.get_payload()  # return email body

            # close POP3 connection and wait
            pop.close()
            time.sleep(3)

        # if user didn't receive the email
        return None
