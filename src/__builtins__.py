# Python imports
import builtins
import threading
from os import path


# Lib imports

# Application imports
from utils.event_system import EventSystem



# NOTE: Threads WILL NOT die with parent's destruction.
def threaded_wrapper(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=False).start()
    return wrapper

# NOTE: Threads WILL die with parent's destruction.
def daemon_threaded_wrapper(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True).start()
    return wrapper



# NOTE: Just reminding myself we can add to builtins two different ways...
# __builtins__.update({"event_system": Builtins()})
builtins.app_name          = "BulkR"
builtins.USER_HOME         = path.expanduser('~')
builtins.event_system      = EventSystem()
builtins.debug             = False
builtins.trace_debug       = False
