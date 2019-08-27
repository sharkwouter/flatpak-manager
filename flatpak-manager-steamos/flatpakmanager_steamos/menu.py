import pygameMenu


class menu(pygameMenu.Menu):

    def remove_last_option(self):
        if len(self._submenus) > 1:
            self._submenus.remove(self._submenus[-1])

