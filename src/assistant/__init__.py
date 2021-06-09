from .core.errors import LanguageNotSupportedError
from .core.events import Events
from .core.userConfig import UserConfig
from .exec import Executor
from .speech import Speech

__all__ = ("Assistant",)

class Assistant(object):

    __allowed_languages = ["en-us", "pt-br"]

    __recognition_error_message = {
        "en-us": "I'm sorry, but I didn't understand what you said",
        "pt-br": "Desculpe, mas eu não entendi o que você falou"
    }

    def __init__(self, name = "", language = "en-us"):
        if language.lower() in self.__allowed_languages: self.__language = language.lower()
        else: raise LanguageNotSupportedError(language, self.__allowed_languages)

        self.__name = name.capitalize()
        self.__events, self.__speech = Events(), Speech()
        self.__executor = Executor(self.__language)
        self.__user_config = UserConfig(self.__language)
        self.__executor.set_user_commands(self.get_user_commands())

    def __send_execution_error(self, text):
        self.__events.on_execution_error()
        self.__send_message(text)

    def __send_recognition_error(self):
        self.__events.on_recognition_error()
        self.__send_message(self.__recognition_error_message[self.__language])

    def __send_message(self, text):
        if not text: return
        speech = self.__speech.text_to_speech(text, self.__language)
        if speech: self.__events.on_speak(speech)
        self.__events.on_chat(text)

    def __update_user_commands(self, user_commands):
        self.__user_config.set_user_commands(user_commands)
        self.__executor.set_user_commands(user_commands)

    def set_event(self, event, function):
        self.__events.set_event(event, function)

    def get_all_commands(self):
        return self.__executor.get_all_commands()

    def get_allowed_languages(self):
        return self.__allowed_languages

    def get_language(self):
        return self.__language

    def get_name(self):
        return self.__name

    def get_user_commands(self):
        return self.__user_config.get_user_commands()

    def remove_user_command(self, command):
        user_commands = self.get_user_commands()
        user_commands.pop(command)
        self.__update_user_commands(user_commands)

    def set_user_command(self, command, terminal_cmd, info, exec_msg, success_msg, error_msg, error_code):
        user_commands = self.get_user_commands()
        user_commands[command] = {
            "command": "#user_command",
            "terminal_command": terminal_cmd,
            "info": info,
            "exec_message": exec_msg,
            "success_message": success_msg,
            "error_message": error_msg,
            "error_code": error_code
        }
        self.__update_user_commands(user_commands)

    def talk(self):
        voice_command = self.__speech.speech_to_text(
            language = self.__language,
            on_listen = self.__events.on_listen,
            on_recognition = self.__events.on_recognition
        )
        self.__events.on_recognition_end()

        if voice_command:
            self.__events.on_execution()
            self.__executor.execute(voice_command, self.__send_message, self.__send_execution_error)
            self.__events.on_execution_end()
        else:
            self.__send_recognition_error()
