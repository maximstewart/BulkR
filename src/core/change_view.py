# Python imports
import os
import re

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

# Application imports
from mixins import CommonWidgetGeneratorMixin
from mixins import CommonActionsMixin


class ChangeView(Gtk.Box, CommonWidgetGeneratorMixin, CommonActionsMixin):
    def __init__(self):
        super(ChangeView, self).__init__()

        self._active_path  = None
        self._from_store   = None
        self._to_store     = None
        self._from_changes = []
        self._to_changes   = []

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_spacing(20)
        self.set_border_width(2)
        self.set_homogeneous(True)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("reset-from-view", self.reset_from_view)
        event_system.subscribe("reset-to-view", self.reset_to_view)
        event_system.subscribe("get-from", self.get_from_list)
        event_system.subscribe("get-to", self.get_to_list)
        event_system.subscribe("set-from", self.set_from_list)
        event_system.subscribe("set-to", self.set_to_list)
        event_system.subscribe("update-from", self.update_from_list)
        event_system.subscribe("update-to", self.update_to_list)
        event_system.subscribe("get-active-path", self._get_active_path)
        event_system.subscribe("set-active-path", self._set_active_path)


    def _load_widgets(self):
        from_container             = Gtk.Box()
        to_container               = Gtk.Box()

        from_scroll_vw, \
        self._from_store            = self._create_treeview_widget(title="From:")
        to_scroll_vw,   \
        self._to_store              = self._create_treeview_widget(title="To:")

        from_container.add(from_scroll_vw)
        to_container.add(to_scroll_vw)

        from_container.set_orientation(1)
        to_container.set_orientation(1)

        fchild = from_scroll_vw.get_children()[0]
        fchild.connect("drag-data-received", self._on_drag_data_received)
        URI_TARGET_TYPE  = 80
        uri_target       = Gtk.TargetEntry.new('text/uri-list', Gtk.TargetFlags(0), URI_TARGET_TYPE)
        targets          = [ uri_target ]
        action           = Gdk.DragAction.COPY
        fchild.enable_model_drag_dest(targets, action)
        fchild.enable_model_drag_source(0, targets, action)

        self.add(from_container)
        self.add(to_container)


    def _on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        if info == 80:
            uri = data.get_uris()[0].split("file://")[1]
            self._set_active_path(uri)


    def _get_active_path(self):
        return self._active_path

    def _set_active_path(self, _file):
        if os.path.isdir(_file) :
            self._from_changes.clear()
            self._active_path = _file
            for f in os.listdir(_file):
                self._from_changes.append(f)

            self._from_changes.sort(key=self._natural_keys)
            self._to_changes = self._from_changes

            event_system.emit("update-from")
            event_system.emit("update-to")

    def get_from_list(self):
        return self._from_changes

    def get_to_list(self):
        return self._to_changes

    def set_from_list(self, from_list):
        self._from_changes = from_list

    def set_to_list(self, to_list):
        self._to_changes = to_list

    def update_from_list(self):
        print("Updating From List...")
        if self._from_store:
            self._from_store.clear()

        for i, change in enumerate(self._from_changes):
            self._from_store.insert(i, [change])

    def update_to_list(self):
        print("Updating To List...")
        if self._to_store:
            self._to_store.clear()

        for i, change in enumerate(self._to_changes):
            self._to_store.insert(i, [change])


    def reset_to_view(self):
        self._to_changes = self._from_changes
        event_system.emit("update-to")

    def reset_from_view(self):
        self._set_active_path(self._active_path)


    def _atoi(self, text):
        return int(text) if text.isdigit() else text

    def _natural_keys(self, text):
        return [ self._atoi(c) for c in re.split('(\d+)',text) ]
