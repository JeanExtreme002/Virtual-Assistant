class Controller(object):

    def __init__(self, application):
        self.__application = application
        self.__assistant = None

    def get_application(self):
        return self.__application

    def get_assistant(self):
        return self.__assistant

    def set_assistant(self, assistant):
        self.__assistant = assistant
