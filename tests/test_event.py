import os, random, sys
sys.path.append(os.getcwd())

from src.assistant.events.errors import InvalidEventException
from src.assistant.events import Events

events = Events()
on_speak_code = random.randint(0, 10000)
on_listen_code = random.randint(0, 10000)

def test_set_event():
    events.on_speak = lambda: on_speak_code
    events.set_event("on_listen", lambda: on_listen_code)

def test_call_event():
    events.on_execution_error("arg1", "arg2", "arg3") # Tests default function
    assert events.on_listen() == on_listen_code
    assert events.on_speak() == on_speak_code

def test_prevent_setting_invalid_value():
    try:
        events.on_listen = "invalid"
        raise AssertionError("An illegal value type has been accepted to the event")
    except TypeError: pass

def test_prevent_setting_invalid_event():
    try:
        events.on_this_is_an_invalid_event = lambda x: None
        raise AssertionError("An invalid event has been registered")
    except InvalidEventException: pass

    try:
        events.ON_LISTEN = lambda x: None
        raise AssertionError("An uppercase event has been registered")
    except InvalidEventException: pass
