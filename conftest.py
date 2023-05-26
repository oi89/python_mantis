import pytest
import json
import os.path

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


@pytest.fixture
def app(request):
    global fixture

    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))["web"]

    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])

    return fixture


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
