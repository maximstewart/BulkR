# Python imports
import builtins, os, re
from os import path

# Lib imports

# Application imports


class Builtins:
    """ Create an pub/sub systems. """

    def __init__(self):
        self.USER_HOME         = path.expanduser('~')
        self.block_from_update = False
        self.block_to_update   = False
        self.active_path       = None
        self.from_changes      = []
        self.to_changes        = []

        # NOTE: The format used is list of [type, target, (data,)] Where:
        #             type is useful context for control flow,
        #             target is the method to call,
        #             data is the method parameters to give
        #       Where data may be any kind of data
        self._gui_events    = []
        self._module_events = []


    # Makeshift fake "events" type system FIFO
    def _pop_gui_event(self):
        if len(self._gui_events) > 0:
            return self._gui_events.pop(0)
        return None

    def _pop_module_event(self):
        if len(self._module_events) > 0:
            return self._module_events.pop(0)
        return None


    def set_active_path(self, _file):
        if os.path.isdir(_file) :
            self.from_changes.clear()
            self.active_path = _file
            for f in os.listdir(_file):
                self.from_changes.append(f)

            self.from_changes.sort(key=self._natural_keys)
            self.to_changes = self.from_changes
            event_system.push_gui_event(["update-from", None, ()])
            event_system.push_gui_event(["update-to", None, ()])

    def reset_to_view(self):
        self.to_changes = self.from_changes
        event_system.push_gui_event(["update-to", None, ()])

    def reset_from_view(self):
        self.set_active_path(self.active_path)

    def push_gui_event(self, event):
        if len(event) == 3:
            self._gui_events.append(event)
            return None

        raise Exception("Invald event format! Please do:  [type, target, (data,)]")

    def push_module_event(self, event):
        if len(event) == 3:
            self._module_events.append(event)
            return None

        raise Exception("Invald event format! Please do:  [type, target, (data,)]")

    def read_gui_event(self):
        return self._gui_events[0]

    def read_module_event(self):
        return self._module_events[0]

    def consume_gui_event(self):
        return self._pop_gui_event()

    def consume_module_event(self):
        return self._pop_module_event()

    def _atoi(self, text):
        return int(text) if text.isdigit() else text

    def _natural_keys(self, text):
        return [ self._atoi(c) for c in re.split('(\d+)',text) ]



# NOTE: Just reminding myself we can add to builtins two different ways...
# __builtins__.update({"event_system": Builtins()})
builtins.app_name          = "BulkR"
builtins.event_system      = Builtins()
builtins.event_sleep_time  = 0.1
builtins.debug             = False
builtins.trace_debug       = False
