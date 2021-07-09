from .exec.commandList import CommandList
from .exec.parser.command import Command
import hashlib, json, os

class UserCommandStorage(object):

    def __init__(self, language = "en-us"):
        self.__language = language.lower()

    def __get_command_list_from(self, command_dict):
        command_list = CommandList(self.__language)

        for voice_command, command_data in command_dict.items():
            if command_list.is_user_command(voice_command):
                command_list.set_user_command(voice_command, command_data)
        return command_list

    def __get_user_command_dict_from(self, command_list):
        user_commands = dict()

        for voice_command, command in command_list.get_user_commands().items():
            user_commands[voice_command] = command.to_dict()
        return user_commands

    def __save_to_file(self, command_dict):
        with open(self.get_user_command_filename(), "w") as file:
            json.dump(command_dict, file)

    def __validate_command_list(self, command_list):
        if not isinstance(command_list, CommandList):
            raise TypeError("a CommandList is required (got {})".format(type(command_list)))

    def delete_user_commands(self):
        try: os.remove(self.get_user_command_filename())
        except FileNotFoundError: pass

    def get_command_list(self):
        filename = self.get_user_command_filename()
        if not os.path.exists(filename): return CommandList(self.__language)

        with open(filename) as file:
            return self.__get_command_list_from(json.load(file))

    def get_user_command_filename(self):
        original_filename = "virtual-assistant-{}-commands.json".format(self.__language)
        filename = "va-" + hashlib.md5(original_filename.encode()).hexdigest()
        return os.path.join(os.environ["LOCALAPPDATA"], filename)

    def save_user_commands(self, command_list):
        self.__validate_command_list(command_list)
        if len(command_list.get_user_commands()) == 0: return self.delete_user_commands()

        user_commands = self.__get_user_command_dict_from(command_list)
        self.__save_to_file(user_commands)
