# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from mixins import CommonActionsMixin


class RemoveFromTo(Gtk.Box, CommonActionsMixin):
    def __init__(self):
        super(RemoveFromTo, self).__init__()

        label              = Gtk.Label(label="Remove From / To:  ")
        self.entry_from    = Gtk.Entry()
        self.entry_to      = Gtk.Entry()

        self.entry_from.set_hexpand(True)
        self.entry_to.set_hexpand(True)
        self.entry_from.set_placeholder_text("From...")
        self.entry_to.set_placeholder_text("To...")

        self.add_widgets([label, self.entry_from, self.entry_to])

        self.set_spacing(20)
        self.show_all()


    def run(self):
        fsub = self.entry_from.get_text()
        tsub = self.entry_to.get_text()

        if fsub and tsub:
            new_collection = []
            print(f"From:  {fsub}\nTo:  {tsub}")
            for name in event_system.to_changes:
                startIndex = name.index(fsub) + 1
                endIndex   = name.index(tsub)
                toRemove   = name[startIndex:endIndex]
                new_collection.append(name.replace(toRemove, ''))

            event_system.to_changes = new_collection
            event_system.push_gui_event(["update-to", self, ()])
