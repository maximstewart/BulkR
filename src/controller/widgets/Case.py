# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from mixins import CommonWidgetGeneratorMixin, CommonActionsMixin


class Case(Gtk.Box, CommonWidgetGeneratorMixin, CommonActionsMixin):
    def __init__(self):
        super(Case, self).__init__()

        data  = ["Title Case", "UPPER", "lower", "InVert CaSe --> iNvERT cAsE"]
        self.store, self.combo_box  = self._create_combobox_widget(data)

        self.combo_box.set_hexpand(True)

        self.add_widgets([self.combo_box])
        self.set_spacing(20)
        self.show_all()


    def run(self):
        new_collection = []
        itr            = self.combo_box.get_active_iter()
        type           = self.store.get(itr, 0)[0]

        print(f"Changing Case...")
        if type == "Title Case":
            for name in event_system.to_changes:
                new_collection.append(name.title())
        if type == "UPPER":
            for name in event_system.to_changes:
                new_collection.append(name.upper())
        if type == "lower":
            for name in event_system.to_changes:
                new_collection.append(name.lower())
        if type == "InVert CaSe --> iNvERT cAsE":
            for name in event_system.to_changes:
                new_collection.append(name.swapcase())

        event_system.to_changes = new_collection
        event_system.push_gui_event(["update-to", self, ()])
