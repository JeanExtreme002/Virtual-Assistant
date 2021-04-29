import os, sys
sys.path.append(os.getcwd())

from src.assistant.core import errors as assistant_errors
from src.assistant.core.events import Events

events = Events()

def test_default_event():
    events.on_listen("arg_1", "arg_2", "arg_3")

def test_set_event():
    events.on_listen = lambda x: None
    events.add_event("on_listen", lambda x: None)

def test_block_invalid_value():
    try:
        events.on_listen = "invalid"
        raise AssertionError("An illegal value type has been accepted to the event.")
    except TypeError: pass

def test_block_invalid_event():
    try:
        events.on_this_is_an_invalid_event = lambda x: None
        raise AssertionError("An invalid event has been registered.")
    except assistant_errors.InvalidEventException: pass

    try:
        events.ON_LISTEN = lambda x: None
        raise AssertionError("An upper case event has been registered.")
    except assistant_errors.InvalidEventException: pass
