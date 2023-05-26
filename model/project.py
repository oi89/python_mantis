class Project:

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"{self.name}:{self.description}"

    def __eq__(self, other):
        return self.name == other.name

    def compare_projects(self):
        return self.name
