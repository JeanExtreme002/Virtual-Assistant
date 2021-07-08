class InvalidEventException(Exception):

    def __init__(self, event):
        self.__event = event

    def __str__(self):
        return "The event '{}' does not exist".format(self.__event)
