# Python imports
import os, sys, threading, time

# lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# Application imports
from mixins import CommonActionsMixin
from . import ChangeView
from .widgets import *


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True).start()
    return wrapper


class Controller(Gtk.Box, CommonActionsMixin):
    def __init__(self, args):
        super(Controller, self).__init__()

        # Add header
        self.change_view = ChangeView()
        action_bar  = Gtk.Box()
        file_choser = Gtk.FileChooserButton(title="Directory Chooser", action=2) # 2 = SELECT_FOLDER
        file_filter = Gtk.FileFilter()
        file_choser.show()
        file_choser.set_filename(event_system.USER_HOME)
        file_filter.add_mime_type("inode/directory")
        file_choser.add_filter(file_filter)

        label = Gtk.Label(label="Bulk Action Type:  ")
        data  = ["Insert", "Replace", "Remove", "Remove From / To", "Case"]
        self.store, self.combo_box  = self._create_combobox_widget(data)

        add_button      = Gtk.Button(label="Add Action")
        test_all_button = Gtk.Button(label="Preview")
        reset_button    = Gtk.Button(label="Reset")
        run_button      = Gtk.Button(label="Run")

        action_bar.add(label)
        action_bar.add(self.combo_box)
        action_bar.add(add_button)
        action_bar.add(test_all_button)
        action_bar.add(reset_button)
        action_bar.set_homogeneous(True)
        action_bar.set_spacing(20)
        action_bar.show_all()

        run_button.connect("clicked", self._run_all)
        add_button.connect("clicked", self._add_action)
        test_all_button.connect("clicked", self._test_all)
        reset_button.connect("clicked", self._reset_to_view)
        file_choser.connect("file-set", self.update_dir_path)

        actions_scroll_label = Gtk.Label(label="Actions:")
        actions_scroll_label.set_xalign(-20)
        actions_scroll_view, self.actions_list_view = self._create_listBox_widget()

        self.set_spacing(20)
        self.set_margin_top(5)
        self.set_margin_bottom(10)
        self.set_margin_left(15)
        self.set_margin_right(15)
        self.set_orientation(1)

        self.add(file_choser)
        self.add(action_bar)
        self.add(self.change_view)
        self.add(actions_scroll_label)
        self.add(actions_scroll_view)
        self.add(run_button)
        self.show_all()

        self.gui_event_observer()
        self.action_collection = []


    @threaded
    def gui_event_observer(self):
        while True:
            time.sleep(event_sleep_time)
            event = event_system.consume_gui_event()
            if event:
                try:
                    type, target, data = event
                    if type:
                        method = getattr(self.__class__, "_handle_gui_event")
                        GLib.idle_add(method, *(self, type, target, data))
                    else:
                        method = getattr(self.__class__, target)
                        GLib.idle_add(method, *(self, *data,))
                except Exception as e:
                    print(repr(e))


    def update_dir_path(self, widget):
        path = widget.get_filename()
        event_system.set_active_path(path)

    def _handle_gui_event(self, type, target, parameters):
        if type == "update-from":
            self.change_view.update_from_list()
            return

        if type == "update-to":
            self.change_view.update_to_list()
            return

        for action in self.action_collection:
            if action == target:
                if type == "delete":
                    self.action_collection.remove(target)
                    target.delete()
                if type == "run":
                    target.run()


    def _add_action(self, widget):
        itr    = self.combo_box.get_active_iter()
        text   = self.store.get(itr, 0)[0]
        widget = self._str_to_class( self._clean_text(text) )

        print(f"Adding:  {self._clean_text(text)}")
        self.actions_list_view.add(widget)
        self.action_collection.append(widget)

    def _test_all(self, widget=None):
        event_system.block_to_update = True
        event_system.reset_to_view()
        for action in self.action_collection:
            action.run()

        event_system.block_to_update = False
        event_system.push_gui_event(["update-to", self, ()])

    def _reset_to_view(self, widget):
        event_system.reset_to_view()

    def _run_all(self, widget):
        if not event_system.active_path:
            print("No active path set. Returning...")
            return

        self._test_all()
        dir = event_system.active_path
        for i, file in enumerate(event_system.from_changes):
            fPath = f"{dir}/{file}"
            tPath = f"{dir}/{event_system.to_changes[i]}"
            if fPath != tPath:
                try:
                    os.rename(fPath, tPath)
                except Exception as e:
                    print(f"Cant Move:   {fPath}\nTo File:   {tPath}")

        event_system.reset_from_view()

    def _clean_text(self, text):
        return text.replace(" ", "") \
                    .replace("/", "")

    def _str_to_class(self, class_name):
        return getattr(sys.modules[__name__], class_name)()
