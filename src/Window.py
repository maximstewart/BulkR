#!/usr/bin/python3


# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from __builtins__ import Builtins
from controller import Controller


class Window(Gtk.Window, Builtins):
    """docstring for Main."""

    def __init__(self, args):
        super(Window, self).__init__()

        self.add(Controller(args))
        self.connect("delete-event", Gtk.main_quit)
        self.set_default_size(850, 600)
        self.set_title(f"{app_name}")
        self.set_icon_from_file("/usr/share/bulkr/bulkr.png")
        self.set_gravity(5)  # 5 = CENTER
        self.set_position(3) # 4 = CENTER_ALWAYS
        self.show_all()
