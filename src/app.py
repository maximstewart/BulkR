#!/usr/bin/python3


# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from core.window import Window


class Application(Window):
    """docstring for Application."""

    def __init__(self, args, unknownargs):
        super(Application, self).__init__(args, unknownargs)
