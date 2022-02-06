# Python imports
import pathlib

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from mixins import CommonActionsMixin


class Insert(Gtk.Box, CommonActionsMixin):
    def __init__(self):
        super(Insert, self).__init__()

        label              = Gtk.Label(label="Insert:  ")
        self.insert_entry  = Gtk.Entry()
        self.insert_entry.set_hexpand(True)
        self.insert_entry.set_placeholder_text("Insert...")

        data  = ["Start", "End", "Position"]
        self.store, self.combo_box  = self._create_combobox_widget(data)

        self.spin_button = self._create_spinbutton_widget()

        self.add_widgets([label, self.insert_entry, self.combo_box, self.spin_button])
        self.set_spacing(20)
        self.show_all()


    def run(self):
        new_collection = []
        insert_str     = self.insert_entry.get_text()
        itr            = self.combo_box.get_active_iter()
        type           = self.store.get(itr, 0)[0]

        print(f"Inserting...")
        if type == "Start":
            for name in event_system.to_changes:
                new_collection.append(f"{insert_str}{name}")
        if type == "End":
            for name in event_system.to_changes:
                base, file_extension = self.get_file_parts()
                new_collection.append(f"{base}{insert_str}{file_extension}")
        if type == "Position":
            position = self.spin_button.get_value_as_int()
            for name in event_system.to_changes:
                name = f"{name[:position]}{insert_str}{name[position:]}"
                new_collection.append(f"{name}")

        event_system.to_changes = new_collection
        event_system.push_gui_event(["update-to", self, ()])


    def _combo_box_changed(self, widget, eve=None):
        itr  = widget.get_active_iter()
        type = self.store.get(itr, 0)[0]

        if type == "Position":
            self.spin_button.set_sensitive(True)
        else:
            self.spin_button.set_sensitive(False)
