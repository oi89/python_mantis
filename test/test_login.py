def test_login(app):
    username = app.config["webadmin"]['username']
    password = app.config["webadmin"]['password']

    app.session.login(username, password)

    assert app.session.is_logged_in_as(username)
