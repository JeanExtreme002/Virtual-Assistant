from .commands import reserved_commands
from .errors import IncompatibleLanguageException, ReservedCommandException
from ..parser.command import Command

class CommandList(object):

    def __init__(self, language):
        self.__language = language.lower()
        self.__reserved_command_list = reserved_commands[self.__language].copy()
        self.__user_command_list = dict()

    def __contains__(self, voice_command):
        return voice_command.lower().replace(".", "").replace(",", "") in self.get_all_commands()

    def __getitem__(self, voice_command):
        return self.get_command_instance_by_voice_command(voice_command)

    def __len__(self):
        return len(self.get_all_commands())

    def __iadd__(self, command_list):
        self.__validate_command_list(command_list)

        for voice_command, command in command_list.get_user_commands().items():
            self.set_user_command(voice_command, command)
        return self

    def __iter__(self):
        return iter(self.get_all_commands())

    def __validate_command_list(self, command_list):
        if not isinstance(command_list, CommandList):
            raise TypeError("a CommandList is required (got {})".format(type(command_list)))

        if not command_list.get_language() == self.get_language():
            raise IncompatibleLanguageException("The command list language must be '{}'.".format(self.get_language()))

    def set_user_command(self, voice_command, command):
        voice_command = voice_command.lower().replace(".", "").replace(",", "")

        if not self.is_user_command(voice_command): raise ReservedCommandException(voice_command)
        self.__user_command_list[voice_command] = command if isinstance(command, Command) else Command(**command)

    def get_all_commands(self):
        command_list = self.__reserved_command_list.copy()
        command_list.update(self.__user_command_list)
        return command_list

    def get_command_instance_by_voice_command(self, voice_command):
        return self.get_all_commands()[voice_command.lower().replace(".", "").replace(",", "")]

    def get_language(self):
        return self.__language

    def get_user_commands(self):
        return self.__user_command_list

    def is_user_command(self, voice_command):
        return not voice_command in self.__reserved_command_list

    def remove_user_command(self, voice_command):
        if not self.is_user_command(voice_command): raise ReservedCommandException(voice_command)
        return self.__user_command_list.pop(voice_command)
