from .core import default_commands

class CommandParser(object):

    def __init__(self, user_commands = dict(), language = "en-us"):
        self.__default_commands = self.__sort_dict(default_commands[language], reverse = True)
        self.__user_commands = self.__sort_dict(user_commands, reverse = True)

    def __sort_dict(self, dict_obj, key = None, reverse = False):
        new_dict = dict()

        for key in sorted(dict_obj, key = key, reverse = reverse):
            new_dict[key] = dict_obj[key]
        return new_dict

    def __get_command(self, voice_command, command_list):
        for command in command_list:
            if voice_command.startswith(command):

                # Separates the command and the arguments.
                args = voice_command.replace(command, "", 1).strip()

                # Add the arguments to the messages.
                exec_msg = command_list[command].get("exec_msg", "").replace("{}", args, 1)
                error_msg = command_list[command].get("error_msg", "").replace("{}", args, 1)

                success_msg = command_list[command].get("success_msg", "")
                info = command_list[command]["info"]
                terminal_command = command_list[command].get("terminal_cmd")
                command = command_list[command]["command"]
                return command, terminal_command, args, info, exec_msg, error_msg, success_msg

        return [None for i in range(7)]

    def parse(self, voice_command):
        voice_command = voice_command.lower().strip()
        command_data = self.__get_command(voice_command, self.__default_commands)

        if command_data[0]: return command_data
        return self.__get_command(voice_command, self.__user_commands)
