import datetime


def get_date_string():
    current_time = datetime.datetime.now()
    return current_time.strftime("%d%m%Y_%H%M%S")


def test_signup_new_account(app):
    username = "u_" + get_date_string()
    email = username + "@localhost"
    password = "test"

    app.james.ensure_user_exists(username, password)
    app.signup.add_new_user(username, email, password)

    assert app.soap.can_login(username, password)
