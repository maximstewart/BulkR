# Python imports

# lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports


class CommonWidgetGeneratorMixin:
    def _create_spinbutton_widget(self):
        spin_button = Gtk.SpinButton()
        spin_button.set_numeric(True)
        spin_button.set_wrap(True)
        spin_button.set_digits(0)
        spin_button.set_increments(1.0, 1.0)
        spin_button.set_range(0, 1000000)
        spin_button.set_sensitive(False)

        return spin_button

    def _create_combobox_widget(self, data):
        cell  = Gtk.CellRendererText()
        store = Gtk.ListStore(str)

        for row in data:
            store.append([row])

        combo_box  = Gtk.ComboBox()
        combo_box.set_model(store)
        combo_box.pack_start(cell, True)
        combo_box.add_attribute(cell, 'text', 0)
        combo_box.set_active(0)

        if self._has_method(self, "_combo_box_changed"):
            combo_box.connect("changed", self._combo_box_changed)

        return store, combo_box

    def _create_treeview_widget(self, title = "Not Set"):
        scroll = Gtk.ScrolledWindow()
        grid   = Gtk.TreeView()
        store  = Gtk.ListStore(str)
        column = Gtk.TreeViewColumn(title)
        name   = Gtk.CellRendererText()
        selec  = grid.get_selection()

        grid.set_model(store)
        selec.set_mode(2)

        column.pack_start(name, True)
        column.add_attribute(name, "text", 0)
        column.set_expand(False)

        grid.append_column(column)
        grid.set_search_column(0)
        grid.set_headers_visible(True)
        grid.set_enable_tree_lines(False)

        grid.show_all()
        scroll.add(grid)
        grid.columns_autosize()
        scroll.set_size_request(360, 240)
        return scroll, store

    def _create_listBox_widget(self,):
        scroll   = Gtk.ScrolledWindow()
        grid     = Gtk.ListBox()
        viewport = Gtk.Viewport()

        grid.show_all()
        viewport.add(grid)
        scroll.add(viewport)

        scroll.set_size_request(360, 200)
        return scroll, grid
