#!/usr/bin/python3


# Python imports
import argparse
import faulthandler
from setproctitle import setproctitle
import signal

# Gtk imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# Application imports
from __builtins__ import *
from app import Application




if __name__ == "__main__":
    try:
        setproctitle('{app_name}')
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit)
        faulthandler.enable()  # For better debug info
        parser = argparse.ArgumentParser()
        # Add long and short arguments
        parser.add_argument("--path", "-p", default=None, help="Path to folder.")

        # Read arguments (If any...)
        args, unknownargs = parser.parse_known_args()

        Application(args, unknownargs)
        Gtk.main()
    except Exception as e:
        print( repr(e) )
