import datetime
import random

from model.project import Project


def test_delete_project(app):
    username = app.config["webadmin"]['username']
    password = app.config["webadmin"]['password']

    app.session.login(username, password)

    old_projects = app.soap.get_projects_list(username, password)

    if len(old_projects) == 0:
        current_time = datetime.datetime.now()
        new_project = Project(name=current_time.strftime("%d%m%Y %H%M%S"), description="")
        app.project.add_project(new_project)
        old_projects.append(new_project)

    project = random.choice(old_projects)
    app.project.delete_project(project)
    old_projects.remove(project)
    new_projects = app.soap.get_projects_list(username, password)

    assert sorted(new_projects, key=Project.compare_projects) == sorted(old_projects, key=Project.compare_projects)
