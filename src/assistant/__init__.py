from .events import Events
from .exec import Executor
from .exec.commandList import CommandList
from .speech import Speech
from .storage import UserCommandStorage

__all__ = ("Assistant", "LanguageNotSupportedError")

class LanguageNotSupportedError(Exception):

    def __init__(self, language, allowed_languages):
        self.__language = language
        self.__allowed_languages = allowed_languages

    def __str__(self):
        return "'{}' is not supported. Choose one of these languages {}".format(self.__language, self.__allowed_languages)

class Assistant(object):

    __allowed_languages = ["en-us", "pt-br"]

    __recognition_error_message = {
        "en-us": "I'm sorry, but I didn't understand what you said",
        "pt-br": "Desculpe, mas eu não entendi o que você falou"
    }

    def __init__(self, name = "", language = "en-us"):
        self.__language = self.validate_language(language)
        self.__name = name.capitalize()

        self.__events, self.__speech = Events(), Speech()
        
        self.__user_command_storage = UserCommandStorage(self.__language)
        self.__command_list = self.__user_command_storage.get_command_list()

        self.__executor = Executor(self.__command_list)

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

    def set_event(self, event, function):
        self.__events.set_event(event, function)

    def get_command_list(self):
        return self.__command_list

    def get_allowed_languages(self):
        return self.__allowed_languages

    def get_language(self):
        return self.__language

    def get_name(self):
        return self.__name

    def get_user_commands(self):
        return self.__user_command_storage.get_user_commands()

    def remove_user_command(self, command):
        self.__command_list.remove_user_command(command)
        self.__user_command_storage.save_user_commands(self.__command_list)

    def set_user_command(self, voice_command, terminal_cmd, info, exec_msg, success_msg, error_msg, error_code):
        command_data = {
            "terminal_command": terminal_cmd,
            "info": info,
            "exec_message": exec_msg,
            "success_message": success_msg,
            "error_message": error_msg,
            "error_code": error_code
        }
        self.__command_list.set_user_command(voice_command, command_data)
        self.__user_command_storage.save_user_commands(self.__command_list)

    def talk(self, audio_filename = None):
        if audio_filename:
            voice_command = self.__speech.get_text_from_audio(
                filename = audio_filename,
                language = self.__language,
                on_listen = self.__events.on_listen,
                on_recognition = self.__events.on_recognition
            )
        else:
            voice_command = self.__speech.speech_to_text(
                language = self.__language,
                on_listen = self.__events.on_listen,
                on_recognition = self.__events.on_recognition
            )
        self.__events.on_recognition_end(voice_command)

        if voice_command:
            self.__events.on_execution()
            self.__executor.execute(voice_command, self.__send_message, self.__send_execution_error)
            self.__events.on_execution_end()
        else:
            self.__send_recognition_error()

    def validate_language(self, language):
        if not language.lower() in self.__allowed_languages:
            raise LanguageNotSupportedError(language, self.__allowed_languages)
        return language.lower()
