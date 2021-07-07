from .command import Command
from .util import sort_dict

class VoiceCommandParser(object):

    __replacing_list = {
        "en-us": dict(),
        "pt-br": {
            "open": {
                "bloco de notas": "notepad",
                "calculadora": "calculator"
            }
        }
    }

    def __init__(self, command_list):
        self.__command_list = command_list

    def __get_messages(self, command_obj, args):
        exec_msg = command_obj.exec_message.replace("{args}", args)
        success_msg = command_obj.success_message.replace("{args}", args)
        error_msg = command_obj.error_message.replace("{args}", args)
        return exec_msg, success_msg, error_msg

    def __translate_args(self, command, args):
        replacing_list = self.__replacing_list[self.__command_list.get_language()].get(command, dict())
        return replacing_list.get(args, args)

    def parse(self, voice_command):
        user_voice_command = voice_command.lower().strip()
        voice_command, command_obj = None, None

        # Sorts to check first commands with more words, example: ["do something like", "do something", "do"]
        command_dict = sort_dict(self.__command_list, reverse = True)

        # Looks for the command in the command list and gets its command instance.
        for cmd in command_dict:
            if user_voice_command.startswith(cmd):
                voice_command, command_obj = cmd, command_dict[cmd]
                break

        # Returns None if no command has been found.
        if not voice_command: return None

        args = user_voice_command.replace(voice_command, "", 1).strip()
        exec_msg, success_msg, error_msg = self.__get_messages(command_obj, args)
        args = self.__translate_args(command_obj.system_command, args)

        parsed_command = Command(
            system_command = command_obj.system_command,
            terminal_command = command_obj.terminal_command,
            args = args,
            info = command_obj.info,
            exec_message = exec_msg,
            success_message = success_msg,
            error_message = error_msg,
            error_code = command_obj.error_code
        )
        return parsed_command
