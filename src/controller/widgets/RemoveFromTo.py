# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from mixins import CommonWidgetGeneratorMixin, CommonActionsMixin


class RemoveFromTo(Gtk.Box, CommonWidgetGeneratorMixin, CommonActionsMixin):
    def __init__(self):
        super(RemoveFromTo, self).__init__()

        self.entry_from       = Gtk.Entry()
        self.entry_to         = Gtk.Entry()
        self.spin_button_from = self._create_spinbutton_widget()
        self.spin_button_to   = self._create_spinbutton_widget()

        self.entry_from.set_hexpand(True)
        self.entry_to.set_hexpand(True)
        self.spin_button_from.set_hexpand(True)
        self.spin_button_to.set_hexpand(True)
        self.spin_button_from.set_sensitive(True)
        self.spin_button_to.set_sensitive(True)
        self.entry_from.set_placeholder_text("Start...")
        self.entry_to.set_placeholder_text("End...")

        data  = ["Using Sub String", "Using Index"]
        self.store, self.combo_box  = self._create_combobox_widget(data)

        self.add_widgets([self.entry_from, \
                            self.entry_to, \
                            self.spin_button_from, \
                            self.spin_button_to, \
                            self.combo_box])
        self.set_spacing(20)
        self.show_all()

        self.spin_button_from.hide()
        self.spin_button_to.hide()


    def run(self):
        new_collection = []
        itr            = self.combo_box.get_active_iter()
        type           = self.store.get(itr, 0)[0]

        if type == "Using Sub String":
            fsub = self.entry_from.get_text()
            tsub = self.entry_to.get_text()

            print(f"From:  {fsub}\nTo:  {tsub}")
            for name in event_system.to_changes:
                startIndex = name.index(fsub) + 1
                endIndex   = name.index(tsub)
                toRemove   = name[startIndex:endIndex]
                new_collection.append(name.replace(toRemove, ''))
        if type == "Using Index":
            fsub = self.spin_button_from.get_value_as_int()
            tsub = self.spin_button_to.get_value_as_int()

            print(f"From:  {fsub}\nTo:  {tsub}")
            for name in event_system.to_changes:
                toRemove   = name[fsub:tsub]
                new_collection.append(name.replace(toRemove, ''))

            event_system.to_changes = new_collection
            event_system.push_gui_event(["update-to", self, ()])

    def _combo_box_changed(self, widget, eve=None):
        itr  = widget.get_active_iter()
        type = self.store.get(itr, 0)[0]

        if type == "Using Sub String":
            self.entry_from.show()
            self.entry_to.show()
            self.spin_button_from.hide()
            self.spin_button_to.hide()
        else:
            self.entry_from.hide()
            self.entry_to.hide()
            self.spin_button_from.show()
            self.spin_button_to.show()
