# Python imports
import pathlib

# lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports


class CommonActionsMixin:
    def add_widgets(self, widgets):
        for widget in widgets:
            self.add(widget)

        test_button   = Gtk.Button(label="Test")
        remove_button = Gtk.Button(label="X")
        up_button     = Gtk.Button()
        down_button   = Gtk.Button()

        up_button.set_image(Gtk.Image.new_from_icon_name("up", 4))
        down_button.set_image(Gtk.Image.new_from_icon_name("down", 4))

        up_button.set_size_request(32, 32)
        down_button.set_size_request(32, 32)
        remove_button.set_size_request(32, 32)
        test_button.set_size_request(96, 32)

        up_button.connect("clicked", self._move_up)
        down_button.connect("clicked", self._move_down)
        remove_button.connect("clicked", self._remove_self)
        test_button.connect("clicked", self._do_run)

        self.add(test_button)
        self.add(up_button)
        self.add(down_button)
        self.add(remove_button)

    def delete(self):
        self.get_parent().destroy()

    def _move_up(self, widget):
        event_system.push_gui_event(["move-up", self, ()])

    def _move_down(self, widget):
        event_system.push_gui_event(["move-down", self, ()])

    def _has_method(self, obj, name):
        ''' Checks if a given method exists. '''
        return callable(getattr(obj, name, None))

    def get_file_parts(self, name):
        file_extension = pathlib.Path(name).suffix
        base = name.split(file_extension)[0]
        return base, file_extension

    def _replace_last(self, string, find, replace):
        reversed = string[::-1]
        replaced = reversed.replace(find[::-1], replace[::-1], 1)
        return replaced[::-1]




    def _remove_self(self, widget):
        event_system.push_gui_event(["delete", self, ()])

    def _do_run(self, widget):
        event_system.push_gui_event(["run", self, ()])
