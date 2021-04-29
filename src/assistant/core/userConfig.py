from ..exec.parser import is_default_command
from .errors import IllegalCommandException
import hashlib, json, os

class UserConfig(object):

    __user_commands = dict()

    def __init__(self, language = "en-us"):
        self.__language = language
        self.__load_user_commands()

    def __filter_commands(self, commands):
        user_commands, default_commands = dict(), dict()

        for key, value in commands.items():
            if not is_default_command(key, self.__language): user_commands[key] = value
            else: default_commands[key] = value

        return user_commands, default_commands

    def __get_user_commands_filename(self):
        original_filename = "virtual-assistant-{}-commands.json".format(self.__language)
        filename = "va-" + hashlib.md5(original_filename.encode()).hexdigest()
        return os.path.join(os.environ["LOCALAPPDATA"], filename)

    def __load_user_commands(self):
        filename = self.__get_user_commands_filename()
        if not os.path.exists(filename): self.__save_user_commands()

        with open(filename) as file:
            commands = json.load(file)
            self.__user_commands = self.__filter_commands(commands)[0]

    def __save_user_commands(self, ignore_errors = True):
        filename = self.__get_user_commands_filename()
        self.__user_commands, default_commands = self.__filter_commands(self.__user_commands)

        if not ignore_errors and default_commands:
            illegal_command = list(default_commands)[0]
            raise IllegalCommandException(illegal_command)

        with open(filename, "w") as file:
            json.dump(self.__user_commands, file)

    def delete_user_commands(self):
        self.__user_commands = dict()
        os.remove(self.__get_user_commands_filename())

    def get_user_commands(self):
        return self.__user_commands.copy()

    def set_user_commands(self, user_commands):
        self.__user_commands = user_commands
        self.__save_user_commands(ignore_errors = False)
