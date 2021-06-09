from .core import default_commands

class CommandParser(object):

    __replacing_list = {
        "en-us": dict(),
        "pt-br": {
            "open": {
                "bloco de notas": "notepad",
                "calculadora": "calculator"
            }
        }
    }

    def __init__(self, user_commands = dict(), language = "en-us"):
        self.__default_commands = self.__sort_dict(default_commands[language], reverse = True)
        self.__user_commands = self.__sort_dict(user_commands, reverse = True)
        self.__language = language

    def __get_args(self, voice_command, command):
        return voice_command.replace(command, "", 1).lower().strip()

    def __get_error_code(self, command_info):
        return int(command_info.get("error_code", -1))

    def __get_execution_data(self, command_info):
        return command_info["command"], command_info.get("terminal_command", ""), command_info.get("info", "")

    def __get_messages(self, command_info, args):
        exec_msg = command_info.get("exec_message", "").replace("{args}", args)
        error_msg = command_info.get("error_message", "").replace("{args}", args)
        success_msg = command_info.get("success_message", "").replace("{args}", args)
        return exec_msg, success_msg, error_msg

    def __get_command(self, voice_command, command_list):
        for command in command_list:
            if voice_command.startswith(command):
                return command, command_list[command]
        return None, None

    def __sort_dict(self, dict_obj, key = None, reverse = False):
        new_dict = dict()

        for key in sorted(dict_obj, key = key, reverse = reverse):
            new_dict[key] = dict_obj[key]
        return new_dict

    def __translate_args(self, command, args):
        replacing_list = self.__replacing_list[self.__language].get(command, dict())
        return replacing_list.get(args, args)

    def parse(self, voice_command):
        voice_command = voice_command.lower().strip()

        # Look for the command in the default command list and in the user command list.
        command, command_info = self.__get_command(voice_command, self.__default_commands)
        if not command: command, command_info = self.__get_command(voice_command, self.__user_commands)

        # Returns a None tuple if no command has been found.
        if not command: return [None for i in range(7)]

        args = self.__get_args(voice_command, command)
        command, terminal_command, info = self.__get_execution_data(command_info)
        exec_msg, success_msg, error_msg = self.__get_messages(command_info, args)
        error_code = self.__get_error_code(command_info)

        args = self.__translate_args(command, args)
        return command, terminal_command, args, info, exec_msg, success_msg, error_msg, error_code
