# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from mixins import CommonWidgetGeneratorMixin
from mixins import CommonActionsMixin




class Remove(Gtk.Box, CommonWidgetGeneratorMixin, CommonActionsMixin):
    def __init__(self):
        super(Remove, self).__init__()
        self._name      = "Remove"

        self.entry_from = Gtk.Entry()

        data  = ["All", "Word Start", "Word End", "First Instance", "Last Instance", "RegEx"]
        self.store, self.combo_box  = self._create_combobox_widget(data)

        self.entry_from.set_hexpand(True)
        self.entry_from.set_placeholder_text("Remove...")

        self.add_widgets([self.entry_from, self.combo_box])
        self.set_spacing(20)
        self.show_all()


    def run(self):
        from_str = self.entry_from.get_text()
        if from_str:
            new_collection = []
            itr            = self.combo_box.get_active_iter()
            type           = self.store.get(itr, 0)[0]
            to_changes     = event_system.emit_and_await("get-to")

            print(f"To Remove:  {from_str}")
            if type == "All":
                for name in to_changes:
                    new_collection.append(name.replace(from_str, ''))
            if type == "Word Start":
                print("Stub...")
            if type == "Word End":
                print("Stub...")
            if type == "First Instance":
                for name in to_changes:
                    new_collection.append( name.replace(from_str, "", 1) )
            if type == "Last Instance":
                for name in to_changes:
                    new_collection.append( self._replace_last(name, from_str, "") )
            if type == "RegEx":
                print("Stub...")

            event_system.emit("set-to", (new_collection,))
            event_system.emit("update-to")
