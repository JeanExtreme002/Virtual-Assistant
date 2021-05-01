from .errors import InvalidEventException

class Events(object):

    __events = [
        "on_chat",
        "on_execution_end",
        "on_execution_error",
        "on_listen",
        "on_recognition",
        "on_recognition_error",
        "on_speak"
    ]

    def __init__(self):
        for event in self.__events:
            self.__set_event(event)

    def __setattr__(self, attribute, value):
        if attribute.lower().startswith("on_"): self.add_event(attribute, value)
        else: self.__dict__[attribute] = value

    def __set_event(self, event, function = lambda *args: None):
        self.__dict__[event.lower()] = function

    def add_event(self, event, function):
        if not callable(function):
            raise TypeError("'{}' is not a function".format(type(function).__name__))

        if not event in self.__events:
            raise InvalidEventException(event)

        self.__set_event(event, function)
