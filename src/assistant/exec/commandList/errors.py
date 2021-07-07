class ReservedCommandException(Exception):

    def __init__(self, command):
        self.__command = command

    def __str__(self):
        return "'{}' is a reserved command and cannot be changed or removed".format(self.__command)

class IncompatibleLanguageException(Exception): pass
