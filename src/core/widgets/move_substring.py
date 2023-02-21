# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from mixins import CommonWidgetGeneratorMixin
from mixins import CommonActionsMixin




class MoveSubstring(Gtk.Box, CommonWidgetGeneratorMixin, CommonActionsMixin):
    def __init__(self):
        super(MoveSubstring, self).__init__()
        self._name                = "Move Substring"

        self.entry_from           = Gtk.Entry()
        self.entry_to             = Gtk.Entry()
        self.spin_button_from     = self._create_spinbutton_widget()
        self.spin_button_to       = self._create_spinbutton_widget()
        self.spin_button_insert_index = self._create_spinbutton_widget()

        self.entry_from.set_hexpand(True)
        self.entry_to.set_hexpand(True)
        self.spin_button_from.set_hexpand(True)
        self.spin_button_to.set_hexpand(True)
        self.spin_button_from.set_sensitive(True)
        self.spin_button_to.set_sensitive(True)
        self.spin_button_insert_index.set_sensitive(True)

        self.entry_from.set_placeholder_text("Substring Start...")
        self.entry_to.set_placeholder_text("Substring End...")

        data  = ["Using Sub String", "Using Index"]
        self.store, self.combo_box  = self._create_combobox_widget(data)

        self.add_widgets([self.entry_from, \
                            self.entry_to, \
                            self.spin_button_from, \
                            self.spin_button_to, \
                            self.spin_button_insert_index, \
                            self.combo_box])
        self.set_spacing(20)
        self.show_all()

        self.spin_button_from.hide()
        self.spin_button_to.hide()


    def run(self):
        new_collection = []
        itr            = self.combo_box.get_active_iter()
        type           = self.store.get(itr, 0)[0]
        to_changes     = event_system.emit_and_await("get-to")
        insert_index   = self.spin_button_insert_index.get_value_as_int()

        if type == "Using Sub String":
            fsub = self.entry_from.get_text()
            tsub = self.entry_to.get_text()

            print(f"From:  {fsub}\nTo:  {tsub}\Move To index: {insert_index}")
            for name in to_changes:
                try:
                    startIndex = name.index(f"{fsub}")
                    endIndex   = name.index(f"{tsub}") + 1
                    toMove     = name[startIndex:endIndex]
                    str1       = name.replace(toMove, '')
                    new_collection.append(str1[:insert_index] + toMove + str1[insert_index:])
                except Exception as e:
                    new_collection.append(name)
        if type == "Using Index":
            fsub = self.spin_button_from.get_value_as_int()
            tsub = self.spin_button_to.get_value_as_int()

            print(f"From:  {fsub}\nTo:  {tsub}")
            for name in to_changes:
                toMove   = name[fsub:tsub]
                str1       = name.replace(toMove, '')
                new_collection.append(str1[:insert_index] + toMove + str1[insert_index:])

        event_system.emit("set-to", (new_collection,))
        event_system.emit("update-to")

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
