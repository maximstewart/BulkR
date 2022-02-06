# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk

# Application imports
from mixins import CommonActionsMixin


class ChangeView(Gtk.Box, CommonActionsMixin):
    def __init__(self):
        super(ChangeView, self).__init__()

        from_container             = Gtk.Box()
        to_container               = Gtk.Box()
        from_scroll_vw, \
        self.from_store            = self._create_treeview_widget(title="From:")
        to_scroll_vw,   \
        self.to_store              = self._create_treeview_widget(title="To:")

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

        self.set_spacing(20)
        self.set_border_width(2)
        self.set_homogeneous(True)
        self.add(from_container)
        self.add(to_container)
        self.show_all()

    def _on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        if info == 80:
            uri = data.get_uris()[0].split("file://")[1]
            event_system.set_active_path(uri)



    def update_from_list(self):
        if event_system.block_from_update:
            return

        print("Updating From List...")
        if self.from_store:
            self.from_store.clear()

        for i, change in enumerate(event_system.from_changes):
            self.from_store.insert(i, [change])

    def update_to_list(self):
        if event_system.block_to_update:
            return

        print("Updating To List...")
        if self.to_store:
            self.to_store.clear()

        for i, change in enumerate(event_system.to_changes):
            self.to_store.insert(i, [change])
