class Controller(object):

    def __init__(self, application):
        if self.__class__ is Controller:
            raise TypeError("Controller is an abstract class")

        self.__application = application
        self.__assistant = None

    def get_application(self):
        return self.__application

    def get_assistant(self):
        return self.__assistant

    def set_assistant(self, assistant):
        self.__assistant = assistant
