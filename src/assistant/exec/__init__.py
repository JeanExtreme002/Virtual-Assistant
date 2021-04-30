from .functions import browser
from .functions import system
from .functions import window
from .parser import CommandParser, default_commands
import math

__all__ = ("Executor",)

class Executor(object):

    __commands = {
        "#user_command": lambda terminal_cmd, args: None,
        "close window": lambda terminal_cmd, args: window.close_window_by_title(args),
        "close": lambda terminal_cmd, args: window.close_active_window(),
        "open folder": lambda terminal_cmd, args: system.open_directory(args),
        "open file": lambda terminal_cmd, args: system.open_file(args),
        "open": lambda terminal_cmd, args: system.run_program(args),
        "search": lambda terminal_cmd, args: browser.search_on_google(args),
    }

    __execution_error_message = {
        "en-us": "Sorry, but I don't have capacity to do it.",
        "pt-br": "Sinto muito, mas eu não tenho capacidade para fazer isso."
    }
    __user_commands = dict()

    def __init__(self, language = "en-us"):
        self.__language = language

    def __send_execution_error(self, error_callback):
        error_callback(self.__execution_error_message[self.__language])

    def __parse_command(self, voice_command):
        command_parser = CommandParser(self.__user_commands, self.__language)
        return command_parser.parse(voice_command)

    def execute(self, voice_command, msg_callback, error_callback):
        command, terminal_cmd, args, info, exec_msg, success_msg, error_msg = self.__parse_command(voice_command)
        if not command: return self.__send_execution_error(error_callback)

        msg_callback(exec_msg)

        try:
            output = str(self.__commands[command](terminal_cmd, args))
            msg_callback(success_msg.replace("{}", output if output else ""))
        except: error_callback(error_msg)

    def get_all_commands(self):
        commands = default_commands[self.__language].copy()
        commands.update(self.__user_commands)
        return commands

    def set_user_commands(self, commands):
        self.__user_commands = commands.copy()
