#!/usr/bin/python3


# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from __builtins__ import Builtins
from Window import Window
from controller import Controller


class Main(Window):
    """docstring for Main."""

    def __init__(self, args):
        super(Main, self).__init__(args)
