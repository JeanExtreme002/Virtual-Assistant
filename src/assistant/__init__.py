from .core.events import Events
from .core.userConfig import UserConfig
from .exec import Executor
from .speech import Speech

__all__ = ("Assistant",)

class Assistant(object):

    __allowed_languages = ["en-us", "pt-br"]
    __assistant_name = "Jarvis"
    __assistant_language = "en-us"
    __recognition_error_message = "I'm sorry, but I didn't understand what you said."

    def __init__(self, name = "Jarvis", language = "en-us"):
        if language.lower() in self.__allowed_languages:
            self.__assistant_language = language.lower()

        self.set_name(name)

        self.__events = Events()
        self.__speech = Speech()
        self.__executor = Executor(self.__assistant_language)

        self.__user_config = UserConfig(language = self.__assistant_language)

    def __send_error(self, text):
        self.__events.on_exec_error()
        self.__send_message(text)

    def __send_message(self, text):
        speech = self.__speech.text_to_speech(text, self.__assistant_language)
        self.__events.on_chat(text)
        self.__events.on_speak(speech)

    def __update_user_commands(self, user_commands):
        self.__user_config.set_user_commands(user_commands)
        self.__executor.set_user_commands(user_commands)

    def add_event(self, event, function):
        self.__events.add_event(event, function)

    def get_all_commands(self):
        return self.__executor.get_all_commands()

    def get_allowed_languages(self):
        return self.__allowed_languages

    def remove_command(self, command):
        user_commands = self.__user_config.get_user_commands()
        user_commands.pop(command)
        self.__update_user_commands(user_commands)

    def set_command(self, command, terminal_cmd, info, exec_msg, success_msg, error_msg):
        user_commands = self.__user_config.get_user_commands()
        user_commands[command] = {
            "command": "#user_command",
            "terminal_cmd": terminal_cmd,
            "info": info,
            "exec_msg": exec_msg,
            "success_msg": success_msg,
            "error_msg": error_msg
        }
        self.__update_user_commands(user_commands)

    def set_name(self, name):
        self.__assistant_name = name.capitalize() if name and not name.isspace() else self.__assistant_name

    def talk(self):
        voice_command = self.__speech.speech_to_text(language = self.__assistant_language)

        if voice_command:
            self.__executor.execute(voice_command, self.__send_message, self.__send_error)
        else:
            self.__events.on_recognition_error()
            self.__send_message(self.__recognition_error_message)
