# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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

        self.set_spacing(20)
        self.set_border_width(2)
        self.set_homogeneous(True)
        self.add(from_container)
        self.add(to_container)
        self.show_all()


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
