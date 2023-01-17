# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from mixins import CommonWidgetGeneratorMixin
from mixins import CommonActionsMixin




class Replace(Gtk.Box, CommonWidgetGeneratorMixin, CommonActionsMixin):
    def __init__(self):
        super(Replace, self).__init__()

        self.entry_from = Gtk.Entry()
        self.entry_to   = Gtk.Entry()

        self.entry_from.set_hexpand(True)
        self.entry_to.set_hexpand(True)
        self.entry_from.set_placeholder_text("Replace From...")
        self.entry_to.set_placeholder_text("Replace To...")

        self.add_widgets([self.entry_from, self.entry_to])

        self.set_spacing(20)
        self.show_all()


    def run(self):
        fsub       = self.entry_from.get_text()
        tsub       = self.entry_to.get_text()
        to_changes = event_system.emit_and_await("get-to")

        if fsub and tsub:
            new_collection = []
            print(f"From:  {fsub}\nTo:  {tsub}")
            for name in to_changes:
                new_collection.append(name.replace(fsub, tsub))

            event_system.emit("set-to", (new_collection,))
            event_system.emit("update-to")
