class IllegalCommandException(Exception):

    def __init__(self, command):
        self.__command = command

    def __str__(self):
        return "'{}' is a default command".format(self.__command)

class InvalidEventException(Exception):

    def __init__(self, event):
        self.__event = event

    def __str__(self):
        return "The event '{}' does not exist".format(self.__event)

class LanguageNotSupportedError(Exception):

    def __init__(self, language, allowed_languages):
        self.__language = language
        self.__allowed_languages = allowed_languages

    def __str__(self):
        return "'{}' is not supported. Choose one of these languages {}".format(self.__language, self.__allowed_languages)
