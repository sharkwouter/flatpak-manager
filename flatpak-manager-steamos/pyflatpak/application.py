import subprocess

class Version():
    UNKNOWN = "unknown"

class application():

    def __init__(self, flatpak_id, remote, name, description="", version=Version.UNKNOWN):
        self.flatpak_id = flatpak_id
        self.remote = remote
        self.name = name
        self.description = description
        self.version = version

        if not self.description:
            self.description = self.flatpak_id

    def __str__(self):
        return self.name.title()

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        names = [str(self), str(other)]
        names.sort()
        if names[0] == str(self):
            return True
        return False
