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
