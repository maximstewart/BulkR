# Python imports
import os
import sys

# lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from mixins import CommonWidgetGeneratorMixin
from .change_view import ChangeView
from .widgets import *




class Controller(Gtk.Box, CommonWidgetGeneratorMixin):
    def __init__(self, args, unknownargs):
        super(Controller, self).__init__()

        # # Add header
        self.change_view       = None
        self.copy_window       = None
        self.store             = None
        self.combo_box         = None
        self.action_collection = []

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()

        if unknownargs:
            for arg in unknownargs:
                if os.path.isdir(arg):
                    event_system.emit("set-active-path", (arg,))

        if args.path and os.path.isdir(args.path):
            event_system.emit("set-active-path", (args.path,))


    def _setup_styling(self):
        self.set_spacing(20)
        self.set_margin_top(5)
        self.set_margin_bottom(10)
        self.set_margin_left(15)
        self.set_margin_right(15)
        self.set_orientation(1)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("handle-gui-event", self._handle_gui_event)

    def _load_widgets(self):
        self.change_view = ChangeView()
        action_bar       = Gtk.Box()

        file_choser      = Gtk.FileChooserButton(title="Directory Chooser", action=2) # 2 = SELECT_FOLDER
        file_filter      = Gtk.FileFilter()
        file_choser.show()
        file_choser.set_filename(USER_HOME)
        file_filter.add_mime_type("inode/directory")
        file_choser.add_filter(file_filter)

        label = Gtk.Label(label="Bulk Action Type:  ")
        data  = ["Insert", "Replace", "Remove", "Remove From / To", "Move Substring", "Case", "Time"]
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
        actions_scroll_view.set_vexpand(True)

        self.copy_window = Gtk.Box()

        self.add(file_choser)
        self.add(action_bar)
        self.add(self.change_view)
        self.add(actions_scroll_label)
        self.add(actions_scroll_view)
        self.add(run_button)


    def update_dir_path(self, widget):
        path = widget.get_filename()
        event_system.emit("set-active-path", (path,))

    def _handle_gui_event(self, type, target, parameters):
        for i, action in enumerate(self.action_collection):
            if action == target:
                if type == "move-up":
                    if i > 0:
                        parent = target.get_parent()
                        parent.remove(target)
                        parent.destroy()
                        self.actions_list_view.insert(target, (i - 1))
                        self.action_collection[i-1], self.action_collection[i] = self.action_collection[i], self.action_collection[i - 1]
                if type == "move-down":
                    if i < len(self.action_collection):
                        parent = target.get_parent()
                        parent.remove(target)
                        parent.destroy()
                        self.actions_list_view.insert(target, (i + 1))
                        self.action_collection[i+1], self.action_collection[i] = self.action_collection[i], self.action_collection[i + 1]

                if type == "delete":
                    self.action_collection.remove(target)
                    target.delete()
                if type == "run":
                    target.run()

                break


    def _add_action(self, widget):
        itr    = self.combo_box.get_active_iter()
        text   = self.store.get(itr, 0)[0]
        widget = self._str_to_class( self._clean_text(text) )

        print(f"Adding:  {self._clean_text(text)}")
        self.actions_list_view.add(widget)
        self.action_collection.append(widget)

    def _test_all(self, widget=None):
        event_system.emit("reset-to-view")
        for action in self.action_collection:
            action.run()

        event_system.emit("update-to")

    def _reset_to_view(self, widget):
        event_system.emit("reset-to-view")

    def _run_all(self, widget):
        dir = event_system.emit_and_await("get-active-path")
        if not dir:
            print("No active path set. Returning...")
            return

        self._test_all()
        to_changes = event_system.emit_and_await("get-to")
        for i, file in enumerate(event_system.emit_and_await("get-from")):
            fPath = f"{dir}/{file}"
            tPath = f"{dir}/{to_changes[i]}"
            if fPath != tPath:
                try:
                    os.rename(fPath, tPath)
                except Exception as e:
                    print(f"Cant Move:   {fPath}\nTo File:   {tPath}")

        event_system.emit("reset-from-view")

    def _clean_text(self, text):
        return text.replace(" ", "") \
                    .replace("/", "")

    def _str_to_class(self, class_name):
        return getattr(sys.modules[__name__], class_name)()

    # NOTE: Yes, this exists in CommonActionsMixin. But, I don't want to add a while mixin just for one method
    def _has_method(self, obj, name):
        ''' Checks if a given method exists. '''
        return callable(getattr(obj, name, None))
