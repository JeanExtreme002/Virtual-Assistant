from .functions import browser, net, system, window
from .commandList import CommandList
from .parser import VoiceCommandParser

__all__ = ("Executor",)

class Executor(object):

    __command_functions = {
        "": lambda terminal_cmd, args: system.exec_command(terminal_cmd.replace("{args}", args)),
        "close window": lambda terminal_cmd, args: (-1, window.close_window(args)),
        "close": lambda terminal_cmd, args: (-1, window.close_active_window()),
        "repeat": lambda terminal_cmd, args: (-1, args),
        "maximize window": lambda terminal_cmd, args: (-1, window.maximize_window(args)),
        "maximize": lambda terminal_cmd, args: (-1, window.maximize_active_window()),
        "minimize window": lambda terminal_cmd, args: (-1, window.minimize_window(args)),
        "minimize": lambda terminal_cmd, args: (-1, window.minimize_active_window()),
        "open folder": lambda terminal_cmd, args: (-1, system.open_directory(args)),
        "open file": lambda terminal_cmd, args: (-1, system.open_file(args)),
        "open": lambda terminal_cmd, args: (-1, system.run_program(args)),
        "search": lambda terminal_cmd, args: (-1, browser.search_on_google(args)),
        "show ip": lambda terminal_cmd, args: (-1, net.get_private_ip()),
        "write": lambda terminal_cmd, args: (-1, system.write(args)),
    }

    __execution_error_message = {
        "en-us": "Sorry, but I don't have capacity to do it.",
        "pt-br": "Sinto muito, mas eu não tenho capacidade para fazer isso."
    }

    def __init__(self, command_list):
        self.__command_list = self.__validate_command_list(command_list)

    def __parse_command(self, voice_command):
        command_parser = VoiceCommandParser(self.__command_list)
        return command_parser.parse(voice_command)

    def __send_execution_error(self, error_callback):
        error_callback(self.__execution_error_message[self.__command_list.get_language()])

    def __validate_command_list(self, command_list):
        if not isinstance(command_list, CommandList):
            raise TypeError("a CommandList is required (got {})".format(type(command_list)))
        return command_list

    def execute(self, voice_command, msg_callback, error_callback):
        command = self.__parse_command(voice_command)
        if not command: return self.__send_execution_error(error_callback)

        system_command, args = command.system_command, command.args
        terminal_command = command.terminal_command
        msg_callback(command.exec_message)

        try:
            exit_code, output = self.__command_functions[system_command](terminal_command, args)

            if exit_code == command.error_code:
                error_callback(command.error_message.replace("{output}", str(output) if output else ""))
            else:
                msg_callback(command.success_message.replace("{output}", str(output) if output else ""))
        except:
            error_callback(command.error_message)
