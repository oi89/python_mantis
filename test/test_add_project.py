import pytest
import string
import random
import datetime

from model.project import Project


def random_string(prefix, maxlen):
    # connect letters, numbers, punctuation symbols and space
    # to get more spaces in result string, multiply " " to 10 times
    symbols = string.ascii_letters + string.digits + " " * 10
    return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def get_date_string():
    current_time = datetime.datetime.now()
    return current_time.strftime("%d%m%Y %H%M%S")


test_data = [Project(name=get_date_string(), description=random_string("", 10))]


@pytest.mark.parametrize("project", test_data, ids=[repr(x) for x in test_data])
def test_add_project(app, project):
    old_projects = app.project.get_projects_list()
    app.project.add_project(project)
    old_projects.append(project)
    new_projects = app.project.get_projects_list()

    assert sorted(new_projects, key=Project.compare_projects) == sorted(old_projects, key=Project.compare_projects)
