import pytest
import json
import os.path
import ftputil

from fixture.application import Application

fixture = None
target = None


def load_config(file):
    global target

    if target is None:
        # get directory's name of current file "conftest.py" and combine it with name of config file
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(file) as config_file:
            target = json.load(config_file)

    return target


# fixture for load config file
@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):
    global fixture

    browser = request.config.getoption("--browser")

    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)

    # fixture.session.ensure_login(username=config["webadmin"]['username'], password=config["webadmin"]['password'])

    return fixture


# fixture for change config file - hide capture for test run
@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config["ftp"]['host'], config["ftp"]['username'], config["ftp"]['password'])

    def fin():
        restore_server_configuration(config["ftp"]['host'], config["ftp"]['username'], config["ftp"]['password'])

    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        # delete renamed file if it exists
        if remote.path.isfile("config_inc.php.old"):
            remote.remove("config_inc.php.old")
        # rename original file if it exists
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.old")
        # copy local file to server
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.old"):
            # delete modified config file
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            # rename config to its original name
            remote.rename("config_inc.php.old", "config_inc.php")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


# pytest hook for add parameter to launch tests
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    # config file
    parser.addoption("--target", action="store", default="target.json")
